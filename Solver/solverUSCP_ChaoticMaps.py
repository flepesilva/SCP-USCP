from Metaheuristics.DOA import iterarDOA
from Metaheuristics.WSO import iterarWSO
import numpy as np
import os
import time

from Problem.USCP.problem import USCP
from Metaheuristics.GWO import iterarGWO
from Metaheuristics.SCA import iterarSCA
from Metaheuristics.WOA import iterarWOA
from Metaheuristics.PSO import iterarPSO
from Diversity.hussainDiversity import diversidadHussain
from Diversity.XPLXTP import porcentajesXLPXPT
from Discretization import discretization as b
from util import util
from BD.sqlite import BD
from ChaoticMaps.chaoticMaps import logisticMap,piecewiseMap,sineMap,singerMap,sinusoidalMap,tentMap,circleMap

def solverUSCP_ChaoticMaps(id, mh, maxIter, pop, instances, DS, repairType, param):
    
    dirResult = './Resultados/'
    instance = USCP(instances)
    
    chaotic_map = None
    
    chaotic = DS[1].split("_")[1]
    
    if chaotic == 'LOG':
        quantityElements = maxIter * pop * instance.getColumns()
        chaotic_map = logisticMap(0.7,quantityElements)
    if chaotic == 'PIECE':
        quantityElements = maxIter * pop * instance.getColumns()
        chaotic_map = piecewiseMap(0.7,quantityElements)
    if chaotic == 'SINE':
        quantityElements = maxIter * pop * instance.getColumns()
        chaotic_map = sineMap(0.7,quantityElements)
    if chaotic == 'SINGER':
        quantityElements = maxIter * pop * instance.getColumns()
        chaotic_map = singerMap(0.7,quantityElements)
    if chaotic == 'SINU':
        quantityElements = maxIter * pop * instance.getColumns()
        chaotic_map = sinusoidalMap(0.7,quantityElements)
    if chaotic == 'TENT':
        quantityElements = maxIter * pop * instance.getColumns()
        chaotic_map = tentMap(0.6,quantityElements)
    if chaotic == 'CIRCLE':
        quantityElements = maxIter * pop * instance.getColumns()
        chaotic_map = circleMap(0.7,quantityElements)
    
    # tomo el tiempo inicial de la ejecucion
    initialTime = time.time()
    
    initializationTime1 = time.time()
    
    results = open(dirResult+mh+"_"+instances.split(".")[0]+"_"+str(id)+".csv", "w")
    results.write(
        f'iter,fitness,time,XPL,XPT,DIV\n'
    )
    
    vel = None
    pBestScore = None
    pBest = None
    
    if mh == 'PSO' or mh == 'WSO':
        vel = np.zeros((pop, instance.getColumns()))
        pBestScore = np.zeros(pop)
        pBestScore.fill(float("inf"))
        pBest = np.zeros((pop, instance.getColumns()))
    
    # Genero una población inicial binaria, esto ya que nuestro problema es binario
    population = np.random.randint(low=0, high=2, size = (pop, instance.getColumns()))

    maxDiversity = diversidadHussain(population)
    XPL , XPT, state = porcentajesXLPXPT(maxDiversity, maxDiversity)
    
    # Genero un vector donde almacenaré los fitness de cada individuo
    fitness = np.zeros(pop)

    # Genero un vetor dedonde tendré mis soluciones rankeadas
    solutionsRanking = np.zeros(pop)
    
    # calculo de factibilidad de cada individuo y calculo del fitness inicial
    for i in range(population.__len__()):
        flag, aux = instance.factibilityTest(population[i])
        if not flag: #solucion infactible
            population[i] = instance.repair(population[i], repairType)
            
        fitness[i] = instance.fitness(population[i])
        if mh == 'PSO' or mh == 'WSO':
            if pBestScore[i] > fitness[i]:
                pBestScore[i] = fitness[i]
                pBest[i, :] = population[i, :].copy()
        
    solutionsRanking = np.argsort(fitness) # rankings de los mejores fitnes
    bestRowAux = solutionsRanking[0]
    # DETERMINO MI MEJOR SOLUCION Y LA GUARDO 
    best = population[bestRowAux].copy()
    bestFitness = fitness[bestRowAux]
    
    matrixBin = population.copy()
    
    initializationTime2 = time.time()
    
    # mostramos nuestro fitness iniciales
    if 'cyc' in instances or 'clr' in instances:
        print("------------------------------------------------------------------------------------------------------")
        print(f"{mh} - {instances} - {DS} - {instance.getBlockSizes()} - best fitness inicial: {str(bestFitness)}")
        print("------------------------------------------------------------------------------------------------------")
    else:
        print("------------------------------------------------------------------------------------------------------")
        print(f"{mh} - u{instances} - {DS} - {instance.getBlockSizes()} - best fitness inicial: {str(bestFitness)}")
        print("------------------------------------------------------------------------------------------------------")
    print("iteracion: "+
            str(0)+
            ", best: "+str(bestFitness)+
            ", optimo: "+str(instance.getOptimum())+
            ", time (s): "+str(round(initializationTime2-initializationTime1,3))+
            ", XPT: "+str(XPT)+
            ", XPL: "+str(XPL)+
            ", DIV: "+str(maxDiversity))
    results.write(
        f'0,{str(bestFitness)},{str(round(initializationTime2-initializationTime1,3))},{str(XPL)},{str(XPT)},{maxDiversity}\n'
    )
    
    for iter in range(0, maxIter):
        # obtengo mi tiempo inicial
        timerStart = time.time()
        
        # perturbo la poblacion con la metaheuristica, pueden usar SCA y GWO
        # en las funciones internas tenemos los otros dos for, for de individuos y for de dimensiones
        # print(poblacion)
        if mh == "SCA":
            population = iterarSCA(maxIter, iter, instance.getColumns(), population.tolist(), best.tolist())
        if mh == "GWO":
            population = iterarGWO(maxIter, iter, instance.getColumns(), population.tolist(), fitness.tolist(), 'MIN')
        if mh == 'WOA':
            population = iterarWOA(maxIter, iter, instance.getColumns(), population.tolist(), best.tolist())
        if mh == 'PSO':
            population, vel = iterarPSO(maxIter, iter, instance.getColumns(), population.tolist(), best.tolist(), pBest.tolist(), vel, 1)
        if mh == 'WSO':
            population, vel = iterarWSO(maxIter, iter, instance.getColumns(), pop, population, best, None, None, vel, pBest)
        if mh == 'DOA':
            population = iterarDOA(maxIter, iter, instance.getColumns(), population, best, 'MIN')  
        # Binarizo, calculo de factibilidad de cada individuo y calculo del fitness
        for i in range(population.__len__()):

            if mh != "GA":
                population[i] = b.aplicarBinarizacion(population[i].tolist(), DS[0], DS[1], best, matrixBin[i].tolist(), iter, pop, maxIter, i, chaotic_map)

            flag, aux = instance.factibilityTest(population[i])
            # print(aux)
            if not flag: #solucion infactible
                population[i] = instance.repair(population[i], repairType)
                

            fitness[i] = instance.fitness(population[i])

            if mh == 'PSO' or mh == 'WSO':
                if fitness[i] < pBestScore[i]:
                    pBest[i] = np.copy(population[i])


        solutionsRanking = np.argsort(fitness) # rankings de los mejores fitness
        
        #Conservo el best
        if fitness[solutionsRanking[0]] < bestFitness:
            bestFitness = fitness[solutionsRanking[0]]
            best = population[solutionsRanking[0]]
        matrixBin = population.copy()

        divT = diversidadHussain(population)

        if maxDiversity < divT:
            maxDiversity = divT
            
        XPL , XPT, state = porcentajesXLPXPT(divT, maxDiversity)

        timerFinal = time.time()
        # calculo mi tiempo para la iteracion t
        timeEjecuted = timerFinal - timerStart
        if (iter+1) % (maxIter//4) == 0:
        # if (iter+1) % 10 == 0:
            print("iteracion: "+
                str(iter+1)+
                ", best: "+str(bestFitness)+
                ", optimo: "+str(instance.getOptimum())+
                ", time (s): "+str(round(timeEjecuted,3))+
                ", XPT: "+str(XPT)+
                ", XPL: "+str(XPL)+
                ", DIV: "+str(divT))
        
        results.write(
            f'{iter+1},{str(bestFitness)},{str(round(timeEjecuted,3))},{str(XPL)},{str(XPT)},{str(divT)}\n'
        )
    finalTime = time.time()
    tiempoEjecucion = finalTime - initialTime
    print("------------------------------------------------------------------------------------------------------")
    print("best fitness: "+str(bestFitness))
    print("Cantidad de columnas seleccionadas: "+str(sum(best)))
    print("Tiempo de ejecucion (s): "+str(tiempoEjecucion))
    print("------------------------------------------------------------------------------------------------------")
    results.close()
    
    binary = util.convert_into_binary(dirResult+mh+"_"+instances.split(".")[0]+"_"+str(id)+".csv")

    fileName = mh+"_"+instances.split(".")[0]

    bd = BD()
    bd.insertarIteraciones(fileName, binary, id)
    bd.insertarResultados(bestFitness, tiempoEjecucion, best, id)
    bd.actualizarExperimento(id, 'terminado')
    
    os.remove(dirResult+mh+"_"+instances.split(".")[0]+"_"+str(id)+".csv")