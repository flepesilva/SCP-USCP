from Solver.solverSCP import solverSCP
from Solver.solverSCP_ChaoticMaps import solverSCP_ChaoticMaps
from Solver.solverUSCP import solverUSCP
from Solver.solverUSCP_ChaoticMaps import solverUSCP_ChaoticMaps

from BD.sqlite import BD
import json
bd = BD()

data = bd.obtenerExperimento()

id              = 0
experimento     = ''
instancia       = ''
problema        = ''
mh              = ''
parametrosMH    = ''
maxIter         = 0
pop             = 0
ds              = []
clasificador    = ''
parametrosC     = '' 


while data != None: 
    id = int(data[0][0])
    id_instancia = int(data[0][9])
    datosInstancia = bd.obtenerInstancia(id_instancia)
    
    problema = datosInstancia[0][1]
    parametrosInstancia = datosInstancia[0][4]
    experimento = data[0][1]
    mh = data[0][2]
    parametrosMH = data[0][3]
    ml = data[0][4]

    
    maxIter = int(parametrosMH.split(",")[0].split(":")[1])
    pop = int(parametrosMH.split(",")[1].split(":")[1])
    ds = []
    
    if problema == 'SCP':
        bd.actualizarExperimento(id, 'ejecutando')
        instancia = f'scp{datosInstancia[0][2]}'
        repair = parametrosMH.split(",")[3].split(":")[1]
        ds.append(parametrosMH.split(",")[2].split(":")[1].split("-")[0])
        ds.append(parametrosMH.split(",")[2].split(":")[1].split("-")[1])
        
        parMH = parametrosMH.split(",")[4]
        
        separacion = ds[1].split("_")
        
        if len(separacion) > 1:
            solverSCP_ChaoticMaps(id, mh, maxIter, pop, instancia, ds, repair, parMH)
        else:
            solverSCP(id, mh, maxIter, pop, instancia, ds, repair, parMH)
            
    if problema == 'USCP':
        bd.actualizarExperimento(id, 'ejecutando')
        if 'cyc' not in datosInstancia[0][2] and 'clr' not in datosInstancia[0][2]:
            instancia = f'scp{datosInstancia[0][2][1:]}'
        else:
            instancia = f'scp{datosInstancia[0][2]}'
        repair = parametrosMH.split(",")[3].split(":")[1]
        ds.append(parametrosMH.split(",")[2].split(":")[1].split("-")[0])
        ds.append(parametrosMH.split(",")[2].split(":")[1].split("-")[1])
        
        parMH = parametrosMH.split(",")[4]
        
        separacion = ds[1].split("_")
        
        if len(separacion) > 1:
            solverUSCP_ChaoticMaps(id, mh, maxIter, pop, instancia, ds, repair, parMH)
        else:
            solverUSCP(id, mh, maxIter, pop, instancia, ds, repair, parMH)
        
    data = bd.obtenerExperimento()
    

print("------------------------------------------------------------------------------------------------------")
print("Se han ejecutado todos los experimentos pendientes.")
print("------------------------------------------------------------------------------------------------------")

