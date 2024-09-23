import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import seaborn as sns
from scipy.stats import mannwhitneyu
from util import util
from BD.sqlite import BD
from Problem.USCP.problem import USCP
i       = ''
tablas                  = False
boxplot                 = False
graficos                = False
graficos_mejor          = True
outlier                 = False
testEstadistico         = False
dirResultado = './Resultados/'

# Función para obtener el mejor valor de fitness (el menor) y su ID
def obtener_mejor_fitness(vector):
    # Encontrar la tupla con el menor valor de fitness (índice 1 de cada tupla)
    mejor_tupla = min(vector, key=lambda t: t[1])
    
    # Extraer el ID y el mejor valor de fitness
    mejor_id = mejor_tupla[0]
    mejor_fitness = mejor_tupla[1]
    
    return mejor_id, mejor_fitness

# Función para eliminar outliers y obtener la mediana con el id correspondiente
def eliminar_outliers_y_obtener_mediana(vector):
    # Extraemos los valores de fitness
    fitness_values = [t[1] for t in vector]
    
    # Calcular el rango intercuartil (IQR) para detectar outliers
    q1 = np.percentile(fitness_values, 25)  # Primer cuartil (Q1)
    q3 = np.percentile(fitness_values, 75)  # Tercer cuartil (Q3)
    iqr = q3 - q1  # Rango intercuartil (IQR)
    
    # Definimos los límites para detectar outliers
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    
    # Filtramos las tuplas eliminando los outliers
    vector_filtrado = [t for t in vector if lower_bound <= t[1] <= upper_bound]
    
    # Extraemos los valores de fitness de las tuplas filtradas
    fitness_filtrado = [t[1] for t in vector_filtrado]
    
    # Si no hay valores de fitness después del filtrado, retornamos None
    if not fitness_filtrado:
        return None, None
    
    # Ordenamos las tuplas filtradas por su valor de fitness
    vector_filtrado.sort(key=lambda t: t[1])
    
    # Encontramos el valor central (sin promediar)
    n = len(vector_filtrado)
    if n % 2 == 1:  # Si es impar, tomamos el valor central
        tupla_mediana = vector_filtrado[n // 2]
    else:  # Si es par, elegimos el valor central inferior
        tupla_mediana = vector_filtrado[n // 2 - 1]
    
    # El id de la tupla con el valor de fitness más cercano a la mediana
    id_mediana = tupla_mediana[0]
    
    return vector_filtrado, id_mediana, tupla_mediana[1]

def graficos_convergencia(ids, instancia):
    if not os.path.exists(f'{dirResultado}/Graficos/Convergence'):
        os.makedirs(f'{dirResultado}/Graficos/Convergence')
    # Crear la figura del gráfico
    plt.figure(figsize=(6, 4))
    # Usamos un colormap con 16 colores distintos (ajustar si hay más archivos)
    colores = plt.cm.get_cmap('tab20', len(ids))  # 'tab20' tiene hasta 20 colores diferentes
    i = 0
    for id in ids:
        experimento = bd.obtenerArchivoID(id)
        for datos in experimento:
            nombre_archivo      = datos[0]
            archivo             = datos[1]
            nombre_experimento  = datos[2]
            direccionDestiono = './Resultados/Transitorio/'+nombre_archivo+'.csv'
            util.writeTofile(archivo,direccionDestiono)                        
            data = pd.read_csv(direccionDestiono, on_bad_lines='skip')
            # Graficar el número de iteración vs fitness
            plt.plot(data.iloc[:, 0], data.iloc[:, 1], label=nombre_experimento.split("-")[1], color=colores(i))  # Usamos el nombre del archivo como etiqueta
            os.remove('./Resultados/Transitorio/'+nombre_archivo+'.csv')
        i+=1
    # Añadir etiquetas y título
    plt.xlabel('Iteration')
    plt.ylabel('Fitness')
    # Ajustar el tamaño de las etiquetas de los ejes X e Y
    plt.xticks(fontsize=7)  # Reducir tamaño de las etiquetas en el eje X
    plt.yticks(fontsize=7)  # Reducir tamaño de las etiquetas en el eje Y
    # plt.title(f'Convergence for {nombre_experimento.split(" ")[0]} instance {instancia[0]}')
    # Añadir leyenda
    plt.legend(loc="best", fontsize="xx-small", ncol=5)  # Ajustar según el número de archivos
    # Mostrar el gráfico
    plt.tight_layout()
    # plt.show()
    plt.savefig(f'{dirResultado}/Graficos/Convergence/fitness_{instancia}_{nombre_experimento.split(" ")[0]}.pdf')
    plt.close('all')
    print(f'Grafico de fitness realizado {instancia} - {mh[0]}') 
    
def graficos_porcentaje(ids, instancia):
    if not os.path.exists(f'{dirResultado}/Graficos/Exploracion-Explotacion/'):
        os.makedirs(f'{dirResultado}/Graficos/Exploracion-Explotacion/')
    for id in ids:
        experimento = bd.obtenerArchivoID(id)
        for datos in experimento:
            nombre_archivo      = datos[0]
            archivo             = datos[1]
            nombre_experimento  = datos[2]
            direccionDestiono = './Resultados/Transitorio/'+nombre_archivo+'.csv'
            util.writeTofile(archivo,direccionDestiono)                        
            data = pd.read_csv(direccionDestiono, on_bad_lines='skip')
            
            # Crear la figura del gráfico
            plt.figure(figsize=(6, 4))
            
            # Graficar el número de iteración vs fitness
            plt.plot(data.iloc[:, 0], data.iloc[:, 3], color="r", label=r"$\overline{XPL}$"+": "+str(np.round(np.mean(data.iloc[:, 3]), decimals=2))+"%")
            plt.plot(data.iloc[:, 0], data.iloc[:, 4], color="b", label=r"$\overline{XPT}$"+": "+str(np.round(np.mean(data.iloc[:, 4]), decimals=2))+"%")
            # Añadir etiquetas y título
            plt.xlabel('Iteration')
            plt.ylabel('Percentage')
            plt.xticks(fontsize=7)  # Reducir tamaño de las etiquetas en el eje X
            plt.yticks(fontsize=7)  # Reducir tamaño de las etiquetas en el eje Y
            # Añadir leyenda
            plt.legend(loc="best", fontsize="x-small", ncol=2)  # Ajustar según el número de archivos
            # Mostrar el gráfico
            plt.tight_layout()
            # plt.show()
            plt.savefig(f'{dirResultado}/Graficos/Exploracion-Explotacion/percentage_{instancia}_{nombre_experimento.split(" ")[0]}_{nombre_experimento.split("-")[1]}.pdf')
            print(f'Grafico de exploracion-explotacion realizado {instancia} - {mh[0]}')
            plt.close('all')
            os.remove('./Resultados/Transitorio/'+nombre_archivo+'.csv')
    
def graficos_diversidad(ids, instancia):
    if not os.path.exists(f'{dirResultado}/Graficos/Diversidad'):
        os.makedirs(f'{dirResultado}/Graficos/Diversidad')
    # Crear la figura del gráfico
    plt.figure(figsize=(10, 5))
    # Usamos un colormap con 16 colores distintos (ajustar si hay más archivos)
    colores = plt.cm.get_cmap('tab20', len(ids))  # 'tab20' tiene hasta 20 colores diferentes
    i = 0
    for id in ids:
        experimento = bd.obtenerArchivoID(id)
        for datos in experimento:
            nombre_archivo      = datos[0]
            archivo             = datos[1]
            nombre_experimento  = datos[2]
            direccionDestiono = './Resultados/Transitorio/'+nombre_archivo+'.csv'
            util.writeTofile(archivo,direccionDestiono)                        
            data = pd.read_csv(direccionDestiono, on_bad_lines='skip')
            # Graficar el número de iteración vs fitness
            plt.plot(data.iloc[:, 0], data.iloc[:, 5], label=nombre_experimento.split("-")[1], color=colores(i))  # Usamos el nombre del archivo como etiqueta
            os.remove('./Resultados/Transitorio/'+nombre_archivo+'.csv')
        i+=1
    # Añadir etiquetas y título
    plt.xlabel('Iteration')
    plt.ylabel('Diversity')
    # plt.title(f'Convergence for {nombre_experimento.split(" ")[0]} instance {instancia[0]}')
    # Añadir leyenda
    plt.legend(loc="best", fontsize="x-small", ncol=8)  # Ajustar según el número de archivos
    # Mostrar el gráfico
    plt.tight_layout()
    # plt.show()
    plt.savefig(f'{dirResultado}/Graficos/Diversidad/fitness_{instancia}_{nombre_experimento.split(" ")[0]}.pdf')
    plt.close('all')
    print(f'Grafico de diversidad realizado {instancia} - {mh[0]}') 

def graficos_convergencia_mejor(ids, instancia):
    if not os.path.exists(f'{dirResultado}/Graficos_Mejor/Convergence'):
        os.makedirs(f'{dirResultado}/Graficos_Mejor/Convergence')
    # Crear la figura del gráfico
    plt.figure(figsize=(6, 4))
    # Usamos un colormap con 16 colores distintos (ajustar si hay más archivos)
    colores = plt.cm.get_cmap('tab20', len(ids))  # 'tab20' tiene hasta 20 colores diferentes
    i = 0
    for id in ids:
        experimento = bd.obtenerArchivoID(id)
        for datos in experimento:
            nombre_archivo      = datos[0]
            archivo             = datos[1]
            nombre_experimento  = datos[2]
            direccionDestiono = './Resultados/Transitorio/'+nombre_archivo+'.csv'
            util.writeTofile(archivo,direccionDestiono)                        
            data = pd.read_csv(direccionDestiono, on_bad_lines='skip')
            # Graficar el número de iteración vs fitness
            plt.plot(data.iloc[:, 0], data.iloc[:, 1], label=nombre_experimento.split("-")[1], color=colores(i))  # Usamos el nombre del archivo como etiqueta
            os.remove('./Resultados/Transitorio/'+nombre_archivo+'.csv')
        i+=1
    # Añadir etiquetas y título
    plt.xlabel('Iteration')
    plt.ylabel('Fitness')
    # Ajustar el tamaño de las etiquetas de los ejes X e Y
    plt.xticks(fontsize=7)  # Reducir tamaño de las etiquetas en el eje X
    plt.yticks(fontsize=7)  # Reducir tamaño de las etiquetas en el eje Y
    # plt.title(f'Convergence for {nombre_experimento.split(" ")[0]} instance {instancia[0]}')
    # Añadir leyenda
    plt.legend(loc="best", fontsize="xx-small", ncol=5)  # Ajustar según el número de archivos
    # Mostrar el gráfico
    plt.tight_layout()
    # plt.show()
    plt.savefig(f'{dirResultado}/Graficos_Mejor/Convergence/fitness_{instancia}_{nombre_experimento.split(" ")[0]}.pdf')
    plt.close('all')
    print(f'Grafico de fitness realizado {instancia} - {mh[0]}') 
    
def graficos_porcentaje_mejor(ids, instancia):
    if not os.path.exists(f'{dirResultado}/Graficos_Mejor/Exploracion-Explotacion/'):
        os.makedirs(f'{dirResultado}/Graficos_Mejor/Exploracion-Explotacion/')
    for id in ids:
        experimento = bd.obtenerArchivoID(id)
        for datos in experimento:
            nombre_archivo      = datos[0]
            archivo             = datos[1]
            nombre_experimento  = datos[2]
            direccionDestiono = './Resultados/Transitorio/'+nombre_archivo+'.csv'
            util.writeTofile(archivo,direccionDestiono)                        
            data = pd.read_csv(direccionDestiono, on_bad_lines='skip')
            
            # Crear la figura del gráfico
            plt.figure(figsize=(6, 4))
            
            # Graficar el número de iteración vs fitness
            plt.plot(data.iloc[:, 0], data.iloc[:, 3], color="r", label=r"$\overline{XPL}$"+": "+str(np.round(np.mean(data.iloc[:, 3]), decimals=2))+"%")
            plt.plot(data.iloc[:, 0], data.iloc[:, 4], color="b", label=r"$\overline{XPT}$"+": "+str(np.round(np.mean(data.iloc[:, 4]), decimals=2))+"%")
            # Añadir etiquetas y título
            plt.xlabel('Iteration')
            plt.ylabel('Percentage')
            plt.xticks(fontsize=7)  # Reducir tamaño de las etiquetas en el eje X
            plt.yticks(fontsize=7)  # Reducir tamaño de las etiquetas en el eje Y
            # Añadir leyenda
            plt.legend(loc="best", fontsize="x-small", ncol=2)  # Ajustar según el número de archivos
            # Mostrar el gráfico
            plt.tight_layout()
            # plt.show()
            plt.savefig(f'{dirResultado}/Graficos_Mejor/Exploracion-Explotacion/percentage_{instancia}_{nombre_experimento.split(" ")[0]}_{nombre_experimento.split("-")[1]}.pdf')
            print(f'Grafico de exploracion-explotacion realizado {instancia} - {mh[0]}')
            plt.close('all')
            os.remove('./Resultados/Transitorio/'+nombre_archivo+'.csv')
    
def graficos_diversidad_mejor(ids, instancia):
    if not os.path.exists(f'{dirResultado}/Graficos_Mejor/Diversidad'):
        os.makedirs(f'{dirResultado}/Graficos_Mejor/Diversidad')
    # Crear la figura del gráfico
    plt.figure(figsize=(10, 5))
    # Usamos un colormap con 16 colores distintos (ajustar si hay más archivos)
    colores = plt.cm.get_cmap('tab20', len(ids))  # 'tab20' tiene hasta 20 colores diferentes
    i = 0
    for id in ids:
        experimento = bd.obtenerArchivoID(id)
        for datos in experimento:
            nombre_archivo      = datos[0]
            archivo             = datos[1]
            nombre_experimento  = datos[2]
            direccionDestiono = './Resultados/Transitorio/'+nombre_archivo+'.csv'
            util.writeTofile(archivo,direccionDestiono)                        
            data = pd.read_csv(direccionDestiono, on_bad_lines='skip')
            # Graficar el número de iteración vs fitness
            plt.plot(data.iloc[:, 0], data.iloc[:, 5], label=nombre_experimento.split("-")[1], color=colores(i))  # Usamos el nombre del archivo como etiqueta
            os.remove('./Resultados/Transitorio/'+nombre_archivo+'.csv')
        i+=1
    # Añadir etiquetas y título
    plt.xlabel('Iteration')
    plt.ylabel('Diversity')
    # plt.title(f'Convergence for {nombre_experimento.split(" ")[0]} instance {instancia[0]}')
    # Añadir leyenda
    plt.legend(loc="best", fontsize="x-small", ncol=8)  # Ajustar según el número de archivos
    # Mostrar el gráfico
    plt.tight_layout()
    # plt.show()
    plt.savefig(f'{dirResultado}/Graficos_Mejor/Diversidad/fitness_{instancia}_{nombre_experimento.split(" ")[0]}.pdf')
    plt.close('all')
    print(f'Grafico de diversidad realizado {instancia} - {mh[0]}') 


def graficos_boxplot(df, instancia):
    if not os.path.exists(f'{dirResultado}/Graficos/boxplot/'):
        os.makedirs(f'{dirResultado}/Graficos/boxplot/')
    # Crear el gráfico boxplot
    plt.figure(figsize=(8, 6))
    sns.boxplot(x='experiment', y='fitness', data=df)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(f'{dirResultado}/Graficos/boxplot/boxplot_{instancia}.pdf')
    print(f'Grafico boxplot realizado {instancia}')
    plt.close('all')
    


databases = ['resultados_gwo.db','resultados_pso.db']

bd = BD('resultados_pso.db')
instancias = bd.obtenerInstanciasEjecutadas('USCP')
mhs = bd.obtenerTecnicas()
print(instancias)

if graficos:
    for instancia in instancias:
        ids = []
        for mh in mhs:
            experimentos = bd.obtenerExperimentos('USCP', mh[0])
            for experimento in experimentos:
                ejecuciones = bd.obtenerEjecuciones(instancia[0], mh[0], experimento[0])                
                mejor_id, mejor_fitness = obtener_mejor_fitness(ejecuciones)
                ids.append(mejor_id)
        graficos_convergencia(ids, instancia[0])
        graficos_porcentaje(ids, instancia[0])
        graficos_diversidad(ids, instancia[0])
        
if graficos_mejor:
    for instancia in instancias:
        ids = []
        for mh in mhs:
            experimentos = bd.obtenerExperimentos('USCP', mh[0])
            for experimento in experimentos:
                ejecuciones = bd.obtenerEjecuciones(instancia[0], mh[0], experimento[0])                
                vector_filtrado, id_mediana, mediana_fitness = eliminar_outliers_y_obtener_mediana(ejecuciones)
                ids.append(id_mediana)
        graficos_convergencia_mejor(ids, instancia[0])
        graficos_porcentaje_mejor(ids, instancia[0])
        graficos_diversidad_mejor(ids, instancia[0])
        
if boxplot:
    for instancia in instancias:
        ids = []
        df = pd.DataFrame(columns=['experiment','fitness'])
        j = 0
        for database in databases:
            bd = BD(database)
            mhs = bd.obtenerTecnicas()
            for mh in mhs:
                experimentos = bd.obtenerExperimentos('USCP', mh[0])
                for experimento in experimentos:
                    ejecuciones = bd.obtenerEjecuciones(instancia[0], mh[0], experimento[0])                
                    vector_filtrado, id_mediana, mediana_fitness = eliminar_outliers_y_obtener_mediana(ejecuciones)
                    ids.append(id_mediana)
                    for f in vector_filtrado:
                        nombre_experimento = experimento[0].split(" ")[0] + "_" + experimento[0].split("-")[1]
                        df.loc[j] = [nombre_experimento, f[1]]
                        j+=1
        graficos_boxplot(df, instancia[0])
        
if outlier:
    for instancia in instancias:
        total       = 0
        suma_out    = 0
        for database in databases:
            bd = BD(database)
            mhs = bd.obtenerTecnicas()
            print(mhs)
            for mh in mhs:
                experimentos = bd.obtenerExperimentos('USCP', mh[0])
                for experimento in experimentos:
                    ejecuciones = bd.obtenerEjecuciones(instancia[0], mh[0], experimento[0])      
                    total += len(ejecuciones)          
                    vector_filtrado, id_mediana, mediana_fitness = eliminar_outliers_y_obtener_mediana(ejecuciones)
                    suma_out += (len(ejecuciones)-len(vector_filtrado))
        print(f'instancia {instancia[0]} total experimentos: {total} - total outlier: {suma_out}')


if tablas:
    archivoResumenFitness = open(f'{dirResultado}resumen_fitness_{mhs[0][0]}.csv', 'w')
    archivoResumenRPD = open(f'{dirResultado}resumen_rpd_{mhs[0][0]}.csv', 'w')
    
    archivoResumenRPD.write(f'mh,experimento')
    archivoResumenFitness.write(f'mh,experimento')
    for instancia in instancias:
        archivoResumenRPD.write(f',{instancia[0]}')
        
        if 'cyc' not in instancia[0] and 'clr' not in instancia[0]:
            i = f'scp{instancia[0][1:]}'
        else:
            i = f'scp{instancia[0]}'
            
        instance = USCP(i)
        
        archivoResumenFitness.write(f',{instancia[0]} ({instance.getOptimum()}),,')
        
    archivoResumenFitness.write('\n')
    archivoResumenFitness.write(f',')
    for instancia in instancias:
        archivoResumenFitness.write(f',best,avg,std-dev')
    archivoResumenFitness.write('\n')
    archivoResumenRPD.write(f',average\n')
    
    for mh in mhs:
        
        experimentos = bd.obtenerExperimentos('USCP', mh[0])
        
        print(len(experimentos))
        
        for experimento in experimentos:
            
            archivoResumenRPD.write(f'{mh[0]},{experimento[0].split(" ")[1].split("-")[1]}')
            archivoResumenFitness.write(f'{mh[0]},{experimento[0].split(" ")[1].split("-")[1]}')
            rpd_promedio = []
            for instancia in instancias:
                
                if 'cyc' not in instancia[0] and 'clr' not in instancia[0]:
                    i = f'scp{instancia[0][1:]}'
                else:
                    i = f'scp{instancia[0]}'
                    
                instance = USCP(i)
                
                ejecuciones = bd.obtenerEjecuciones(instancia[0], mh[0], experimento[0])    
                
                fitness = []
                
                for ejecucion in ejecuciones:
                    f = ejecucion[1]
                    t = ejecucion[2]
                    
                    fitness.append(f)
                    
                    # print(f'fitness obtenido para el experimento {experimento[0]} instancia {instancia[0]} mh {mh[0]}: {fitness}')
        
                rpd = np.round(( 100 * ( np.average(fitness) - instance.getOptimum() ) / instance.getOptimum() ),2)
                archivoResumenRPD.write(f',{rpd}')
                archivoResumenFitness.write(f',{np.min(fitness)},{np.round(np.average(fitness),2)},{np.round(np.std(fitness),2)}')
                rpd_promedio.append(rpd)
                
            archivoResumenRPD.write(f',{np.round(np.average(rpd_promedio),2)}\n')
            archivoResumenFitness.write(f'\n')
    
    archivoResumenFitness.close()
    archivoResumenRPD.close()

# if diversidad: 
#     esquemas = ['STD','COM','ELIT']
#     for esquema in esquemas:
#         for mh in mhs:
#             experimentos = bd.obtenerExperimentosEspecial('SCP', mh[0], esquema)
#             for instancia in instancias:
#                 if not os.path.exists(f'{dirResultado}/Graficos/SCP/{instancia[0]}/{mh[0]}'):
#                     os.makedirs(f'{dirResultado}/Graficos/SCP/{instancia[0]}/{mh[0]}')
#                 figSTD, axSTD = plt.subplots()
#                 noGraficar = False
#                 for experimento in experimentos:
#                     mejor = bd.obtenerMejoresEjecucionesSCP(instancia[0], mh[0], experimento[0])
#                     print(f'Analizando experimento {experimento[0]} asociado a la instancia {instancia[0]} metaheuristica {mh[0]}')
#                     for m in mejor:
#                         id                  = m[0]
#                         nombre_archivo      = m[2]
#                         archivo             = m[3]
#                         direccionDestiono = './Resultados/Transitorio/'+nombre_archivo+'.csv'
#                         # print("-------------------------------------------------------------------------------")
#                         util.writeTofile(archivo,direccionDestiono)                        
#                         data = pd.read_csv(direccionDestiono, on_bad_lines='skip')
#                         if len(data['iter']) == 501:
#                             iteraciones = data['iter']
#                             fitness     = data['fitness']
#                             time        = data['time']
#                             xpl         = data['XPL']
#                             xpt         = data['XPT']

#                             figPER, axPER = plt.subplots()
#                             axPER.plot(iteraciones, xpl, color="r", label=r"$\overline{XPL}$"+": "+str(np.round(np.mean(xpl), decimals=2))+"%")
#                             axPER.plot(iteraciones, xpt, color="b", label=r"$\overline{XPT}$"+": "+str(np.round(np.mean(xpt), decimals=2))+"%")
#                             axPER.set_title(f'XPL% - XPT% {mh[0]} {experimento[0].split("-")[1]} {instancia[0]}')
#                             axPER.set_ylabel("Percentage")
#                             axPER.set_xlabel("Iteration")
#                             axPER.legend(loc = 'upper right')
#                             plt.savefig(f'{dirResultado}/Graficos/SCP/{instancia[0]}/{mh[0]}/Percentage_{experimento[0]}.pdf')
#                             plt.close('all')
#                             print(f'Grafico de exploracion y explotacion realizado para {experimento[0]}, id: {id}, instancia: {instancia[0]}')
                            
#                         os.remove('./Resultados/Transitorio/'+nombre_archivo+'.csv')

# if graficos:
#     iteraciones     = []
#     rendimientos    = dict()   
#     if not os.path.exists(f'{dirResultado}/Best'):
#         os.makedirs(f'{dirResultado}/Best')
        
#     for mh in mhs:
#         experimentos = bd.obtenerExperimentos('USCP', mh[0])
#         for instancia in instancias:
            
#             archivoInstancia = open(f'{dirResultado}/Best/{instancia[0]}.csv', 'w')
#             i = 0
#             for experimento in experimentos:
#                 ejecuciones = bd.obtenerMejoresEjecucionesSCP(instancia[0], mh[0], experimento[0])
                
#                 for ejecucion in ejecuciones:
#                     id                  = ejecucion[0]
#                     nombre_archivo      = ejecucion[2]
#                     archivo             = ejecucion[3]
#                     direccionDestiono = './Resultados/Transitorio/'+nombre_archivo+'.csv'
#                     # print("-------------------------------------------------------------------------------")
#                     util.writeTofile(archivo,direccionDestiono)                        
#                     data = pd.read_csv(direccionDestiono, on_bad_lines='skip')
#                     print(f'Analizando {experimento} - {instancia}')
#                     # print(data.shape)
#                     fitness     = data['fitness']
#                     iteraciones = data['iter']
#                     print(fitness)
#                     if i == 0:
#                         archivoInstancia.write(f'iter')
#                         for iter in iteraciones:                        
#                             archivoInstancia.write(f',{iter}')
#                         archivoInstancia.write(f'\n')
#                         i+=1
                        
#                     archivoInstancia.write(f'{experimento[0].split("-")[1]}')
#                     for f in fitness:                        
#                         archivoInstancia.write(f',{f}')
#                     archivoInstancia.write(f'\n')
            
            
            
            
            
        # for instancia in instancias:
        #     figSTD, axSTD = plt.subplots()
        #     noGraficar = False
        #     for experimento in experimentos:
        #         mejor = bd.obtenerMejoresEjecucionesSCP(instancia[0], mh[0], experimento[0])
        #         print(f'Analizando experimento {experimento[0]} asociado a la instancia {instancia[0]} metaheuristica {mh[0]}')
        #         for m in mejor:
        #             id                  = m[0]
        #             nombre_archivo      = m[2]
        #             archivo             = m[3]
        #             direccionDestiono = './Resultados/Transitorio/'+nombre_archivo+'.csv'
        #             # print("-------------------------------------------------------------------------------")
        #             util.writeTofile(archivo,direccionDestiono)                        
        #             data = pd.read_csv(direccionDestiono, on_bad_lines='skip')
        #             if len(data['iter']) == 501:
        #                 iteraciones = data['iter']
        #             fitness     = data['fitness']
        #             rendimientos[f'{experimento[0]} - {instancia[0]}'] = fitness
                        
        #             os.remove('./Resultados/Transitorio/'+nombre_archivo+'.csv')
        #     for clave in rendimientos:
        #         etiqueta = f'{clave.split("-")[1]}'
        #         if mh[0] in clave and instancia[0] in clave and esquema in clave:        
        #             if len(rendimientos[clave]) == 501:
        #                 axSTD.plot(iteraciones, rendimientos[clave], label=etiqueta)
        #             else: 
        #                 noGraficar = True
        #     if not noGraficar:
        #         axSTD.set_title(f'Coverage {instancia[0]} - {mh[0]} - {esquema}')
        #         axSTD.set_ylabel("Fitness")
        #         axSTD.set_xlabel("Iteration")
        #         axSTD.legend(loc = 'upper right')
        #         plt.savefig(f'{dirResultado}/Best/SCP/{mh[0]}/{esquema}/fitness_{instancia[0]}_{mh[0]}_{esquema}.pdf')
        #         plt.close('all')
        #         print(f'Grafico de fitness realizado {instancia[0]} - {mh[0]} - {esquema}')     
                
    
if testEstadistico:
    for instancia in instancias:
        for mh in mhs:
            if not os.path.exists(f'{dirResultado}/Test_Estadistico/SCP/{mh[0]}/instancias'):
                os.makedirs(f'{dirResultado}/Test_Estadistico/SCP/{mh[0]}/instancias')
            archivoTransitorio = open(f'{dirResultado}/Test_Estadistico/SCP/{mh[0]}/instancias/{instancia[0]}.csv', 'w')
            archivoTransitorio.write('MH,FITNESS\n')
            experimentos = bd.obtenerExperimentos('SCP', mh[0])
            for experimento in experimentos:
                
                ejecuciones = bd.obtenerEjecuciones(instancia[0], mh[0], experimento[0])
                rendimiento     = []
                
                print(f'Analizando experimento {experimento[0]} asociado a la instancia {instancia[0]} metaheuristica {mh[0]}')
                
                for ejecucion in ejecuciones:
                    id                  = ejecucion[0]
                    nombre_archivo      = ejecucion[2]
                    archivo             = ejecucion[3]
                    tiempo_ejecucion    = ejecucion[5]
                    
                    direccionDestiono = './Resultados/Transitorio/'+nombre_archivo+'.csv'
                    # print("-------------------------------------------------------------------------------")
                    util.writeTofile(archivo,direccionDestiono)
                    
                    data = pd.read_csv(direccionDestiono, on_bad_lines='skip')
                    
                    iteraciones = data['iter']
                    fitness     = data['fitness']
                    time        = data['time']
                    xpl         = data['XPL']
                    xpt         = data['XPT']
                    
                    ultimo = len(iteraciones) - 1
                    
                    rendimiento.append(fitness[ultimo])
                    archivoTransitorio.write(f'{experimento[0].split("-")[1]},{fitness[ultimo]}\n')

                    os.remove('./Resultados/Transitorio/'+nombre_archivo+'.csv')
            archivoTransitorio.close()
    
    for instancia in instancias:
        for mh in mhs:
            if not os.path.exists(f'{dirResultado}/Test_Estadistico/SCP/{mh[0]}/Test_instancias'):
                os.makedirs(f'{dirResultado}/Test_Estadistico/SCP/{mh[0]}/Test_instancias')
            test_estadistico = open(f'{dirResultado}Test_Estadistico/SCP/{mh[0]}/Test_instancias/test_estadistico_{mh[0]}_{instancia[0]}.csv', 'w')
            test_estadistico.write(f' , ')
            experimentos = bd.obtenerExperimentos('SCP', mh[0])
            i = 1
            for tecnica in experimentos:
                test_estadistico.write(f' {tecnica[0].split("-")[1]} ')
                if i < len(experimentos):
                    test_estadistico.write(f' , ')
                else:
                    test_estadistico.write(f' \n ')
                i += 1

            datos = pd.read_csv(f'{dirResultado}Test_Estadistico/SCP/{mh[0]}/instancias/{instancia[0]}.csv')
            for tecnica in experimentos:
                data_x = datos[datos['MH'].isin([tecnica[0].split("-")[1]])]
                x = data_x['FITNESS']
                test_estadistico.write(f' {tecnica[0].split("-")[1]} ')
                for t in experimentos:
                    if t[0] != tecnica[0]:
                        data_y = datos[datos['MH'].isin([t[0].split("-")[1]])]
                        y = data_y['FITNESS']
                        p_value = mannwhitneyu(x,y, alternative='less')
                        print(f'Comparando', f'{tecnica[0]}', f'contra', f'{t[0]}', f'en la instancia', f'{instancia[0]}:', f'{np.round(p_value[1],3)}',)
                        if not os.path.exists(f'{dirResultado}/Test_Estadistico/SCP/{mh[0]}/Transitorio'):
                            os.makedirs(f'{dirResultado}/Test_Estadistico/SCP/{mh[0]}/Transitorio')
                        archivo = open(f'{dirResultado}Test_Estadistico/SCP/{mh[0]}/Transitorio/{tecnica[0]}_contra_{t[0]}.csv', 'a')
                        archivo.write(f'{np.round(p_value[1],3)}\n')
                        test_estadistico.write(f' , {np.round(p_value[1],3)} ')
                    else:
                        test_estadistico.write(f' , X ')
                test_estadistico.write(f' \n ')
            test_estadistico.close()
    
    for mh in mhs:
        if not os.path.exists(f'{dirResultado}/Test_Estadistico/SCP/{mh[0]}/Test'):
            os.makedirs(f'{dirResultado}/Test_Estadistico/SCP/{mh[0]}/Test')
        test = open(f'{dirResultado}Test_Estadistico/SCP/{mh[0]}/Test/test_estadistico_{mh[0]}.csv', 'w')
        test.write(f' , ')
        experimentos = bd.obtenerExperimentos('SCP', mh[0])
        i = 1
        for tecnica in experimentos:
            test.write(f' {tecnica[0].split("-")[1]} ')
            if i < len(experimentos):
                test.write(f' , ')
            else:
                test.write(f' \n ')
            i += 1
            
        for tecnica in experimentos:
            test.write(f' {tecnica[0].split("-")[1]} ')
            print(f'Analizando experimento {tecnica[0]} mh: {mh[0]}')
            for t in experimentos:
                if t[0] != tecnica[0]:
                    archivo = pd.read_csv(f'./Resultados/Test_Estadistico/SCP/{mh[0]}/Transitorio/{tecnica[0]}_contra_{t[0]}.csv')
                    test.write(f' , {np.round(np.average(archivo.iloc[:, 0 ]),3)} ')
                    os.remove(f'./Resultados/Test_Estadistico/SCP/{mh[0]}/Transitorio/{tecnica[0]}_contra_{t[0]}.csv')
                else:
                    test.write(f' , X ')
            test.write(f' \n ')
        test.close()