import numpy as np
import os
from Problem.SCP.problem import SCP
from Metaheuristics.GWO import iterarGWO
from Metaheuristics.SCA import iterarSCA
from Metaheuristics.WOA import iterarWOA
from Metaheuristics.PSO import iterarPSO
from Diversity.hussainDiversity import diversidadHussain
from Diversity.XPLXTP import porcentajesXLPXPT
import time
from Discretization import discretization as b
from util import util
from BD.sqlite import BD

from ChaoticMaps.chaoticMaps import logisticMap,piecewiseMap,sineMap,singerMap,sinusoidalMap,tentMap,circleMap

def solverSCP_ChaoticMaps(id, mh, maxIter, pop, instancia, DS, repairType, param):
    
    dirResult = './Resultados/'
    instance = SCP(instancia)
    
    chaotic_map = None
    
    chaotic = DS[1].split("_")[1]
    
    if chaotic == 'LOG':
        cantidad_elementos = maxIter * pop * instance.getColumns()
        chaotic_map = logisticMap(0.7,cantidad_elementos)
    if chaotic == 'PIECE':
        cantidad_elementos = maxIter * pop * instance.getColumns()
        chaotic_map = piecewiseMap(0.7,cantidad_elementos)
    if chaotic == 'SINE':
        cantidad_elementos = maxIter * pop * instance.getColumns()
        chaotic_map = sineMap(0.7,cantidad_elementos)
    if chaotic == 'SINGER':
        cantidad_elementos = maxIter * pop * instance.getColumns()
        chaotic_map = singerMap(0.7,cantidad_elementos)
    if chaotic == 'SINU':
        cantidad_elementos = maxIter * pop * instance.getColumns()
        chaotic_map = sinusoidalMap(0.7,cantidad_elementos)
    if chaotic == 'TENT':
        cantidad_elementos = maxIter * pop * instance.getColumns()
        chaotic_map = tentMap(0.6,cantidad_elementos)
    if chaotic == 'CIRCLE':
        cantidad_elementos = maxIter * pop * instance.getColumns()
        chaotic_map = circleMap(0.7,cantidad_elementos)
    
    # tomo el tiempo inicial de la ejecucion
    initialTime = time.time()
    
    tiempoInicializacion1 = time.time()
    
    results = open(dirResult+mh+"_"+instancia.split(".")[0]+"_"+str(id)+".csv", "w")
    results.write(
        f'iter,fitness,time,XPL,XPT,DIV\n'
    )
    
    vel = None
    pBestScore = None
    pBest = None
    
    if mh == 'PSO':
        vel = np.zeros((pop, instance.getColumns()))
        pBestScore = np.zeros(pop)
        pBestScore.fill(float("inf"))
        pBest = np.zeros((pop, instance.getColumns()))
    
    # Genero una población inicial binaria, esto ya que nuestro problema es binario
    poblacion = np.random.randint(low=0, high=2, size = (pop, instance.getColumns()))

    maxDiversidad = diversidadHussain(poblacion)
    XPL , XPT, state = porcentajesXLPXPT(maxDiversidad, maxDiversidad)
    
    # Genero un vector donde almacenaré los fitness de cada individuo
    fitness = np.zeros(pop)

    # Genero un vetor dedonde tendré mis soluciones rankeadas
    solutionsRanking = np.zeros(pop)
    
    # calculo de factibilidad de cada individuo y calculo del fitness inicial
    for i in range(poblacion.__len__()):
        flag, aux = instance.factibilityTest(poblacion[i])
        if not flag: #solucion infactible
            poblacion[i] = instance.repair(poblacion[i], repairType)
            
        fitness[i] = instance.fitness(poblacion[i])
        if mh == 'PSO':
            if pBestScore[i] > fitness[i]:
                pBestScore[i] = fitness[i]
                pBest[i, :] = poblacion[i, :].copy()
        
    solutionsRanking = np.argsort(fitness) # rankings de los mejores fitnes
    bestRowAux = solutionsRanking[0]
    # DETERMINO MI MEJOR SOLUCION Y LA GUARDO 
    Best = poblacion[bestRowAux].copy()
    BestFitness = fitness[bestRowAux]
    
    matrixBin = poblacion.copy()
    
    tiempoInicializacion2 = time.time()
    
    # mostramos nuestro fitness iniciales
    print("------------------------------------------------------------------------------------------------------")
    print(f"{mh} - {instancia} - {DS} - {instance.getBlockSizes()} - best fitness inicial: {str(BestFitness)}")
    print("------------------------------------------------------------------------------------------------------")
    print("iteracion: "+
            str(0)+
            ", best: "+str(BestFitness)+
            ", optimo: "+str(instance.getOptimum())+
            ", time (s): "+str(round(tiempoInicializacion2-tiempoInicializacion1,3))+
            ", XPT: "+str(XPT)+
            ", XPL: "+str(XPL)+
            ", DIV: "+str(maxDiversidad))
    results.write(
        f'0,{str(BestFitness)},{str(round(tiempoInicializacion2-tiempoInicializacion1,3))},{str(XPL)},{str(XPT)},{maxDiversidad}\n'
    )
    
    for iter in range(0, maxIter):
        # obtengo mi tiempo inicial
        timerStart = time.time()
        
        # perturbo la poblacion con la metaheuristica, pueden usar SCA y GWO
        # en las funciones internas tenemos los otros dos for, for de individuos y for de dimensiones
        # print(poblacion)
        if mh == "SCA":
            poblacion = iterarSCA(maxIter, iter, instance.getColumns(), poblacion.tolist(), Best.tolist())
        if mh == "GWO":
            poblacion = iterarGWO(maxIter, iter, instance.getColumns(), poblacion.tolist(), fitness.tolist(), 'MIN')
        if mh == 'WOA':
            poblacion = iterarWOA(maxIter, iter, instance.getColumns(), poblacion.tolist(), Best.tolist())
        if mh == 'PSO':
            poblacion, vel = iterarPSO(maxIter, iter, instance.getColumns(), poblacion.tolist(), Best.tolist(), pBest.tolist(), vel, 1)
        
        # Binarizo, calculo de factibilidad de cada individuo y calculo del fitness
        for i in range(poblacion.__len__()):

            if mh != "GA":
                poblacion[i] = b.aplicarBinarizacion(poblacion[i].tolist(), DS[0], DS[1], Best, matrixBin[i].tolist(), iter, pop, maxIter, i, chaotic_map)

            flag, aux = instance.factibilityTest(poblacion[i])
            # print(aux)
            if not flag: #solucion infactible
                poblacion[i] = instance.repair(poblacion[i], repairType)
                

            fitness[i] = instance.fitness(poblacion[i])
            
            if mh == 'PSO':
                if fitness[i] < pBestScore[i]:
                    pBest[i] = np.copy(poblacion[i])


        solutionsRanking = np.argsort(fitness) # rankings de los mejores fitness
        
        #Conservo el Best
        if fitness[solutionsRanking[0]] < BestFitness:
            BestFitness = fitness[solutionsRanking[0]]
            Best = poblacion[solutionsRanking[0]]
        matrixBin = poblacion.copy()

        div_t = diversidadHussain(poblacion)

        if maxDiversidad < div_t:
            maxDiversidad = div_t
            
        XPL , XPT, state = porcentajesXLPXPT(div_t, maxDiversidad)

        timerFinal = time.time()
        # calculo mi tiempo para la iteracion t
        timeEjecuted = timerFinal - timerStart
        if (iter+1) % (maxIter//4) == 0:
        # if (iter+1) % 10 == 0:
            print("iteracion: "+
                str(iter+1)+
                ", best: "+str(BestFitness)+
                ", optimo: "+str(instance.getOptimum())+
                ", time (s): "+str(round(timeEjecuted,3))+
                ", XPT: "+str(XPT)+
                ", XPL: "+str(XPL)+
                ", DIV: "+str(div_t))
        
        results.write(
            f'{iter+1},{str(BestFitness)},{str(round(timeEjecuted,3))},{str(XPL)},{str(XPT)},{str(div_t)}\n'
        )
    finalTime = time.time()
    tiempoEjecucion = finalTime - initialTime
    print("------------------------------------------------------------------------------------------------------")
    print("best fitness: "+str(BestFitness))
    print("Cantidad de columnas seleccionadas: "+str(sum(Best)))
    print("Tiempo de ejecucion (s): "+str(tiempoEjecucion))
    print("------------------------------------------------------------------------------------------------------")
    results.close()
    
    binary = util.convert_into_binary(dirResult+mh+"_"+instancia.split(".")[0]+"_"+str(id)+".csv")

    nombre_archivo = mh+"_"+instancia.split(".")[0]

    bd = BD()
    bd.insertarIteraciones(nombre_archivo, binary, id)
    bd.insertarResultados(BestFitness, tiempoEjecucion, Best, id)
    bd.actualizarExperimento(id, 'terminado')
    
    os.remove(dirResult+mh+"_"+instancia.split(".")[0]+"_"+str(id)+".csv")