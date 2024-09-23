import numpy as np
import matplotlib.pyplot as plt
import math

def chebyshevMap(initial,iteration):
    map_values = np.zeros(iteration)
       
    
    i = 1
    map_values[0] = initial
    x_previo = initial
    while i < iteration:
        
        x = math.cos( x_previo * ( 1 / math.cos( x_previo ) ) )
        
        map_values[i] = x
        
        x_previo = x
        
        i+=1
    return map_values

def gaussianAndGauss_mouseMap(initial,iteration):
    map_values = np.zeros(iteration)
       
    
    i = 1
    map_values[0] = initial
    x_previo = initial
    while i < iteration:
        
        if x_previo == 0:
            x = 0
        else:
            x = ( 1 / ( x_previo % 1.0 ) )
        
        map_values[i] = x
        
        x_previo = x
        
        i+=1
    return map_values

def circleMap(initial,iteration):
    map_values = np.zeros(iteration)
    a = 0.5
    b = 0.2    
    k = a / ( 2 * math.pi )
    
    
    i = 1
    map_values[0] = initial
    x_previo = initial
    while i < iteration:
        
        x = ( x_previo + b - k * math.sin( 2 * math.pi * x_previo ) ) % 1.0
        
        map_values[i] = x
        
        x_previo = x
        
        i+=1
    return map_values

def logisticMap(initial,iteration):
    map_values = np.zeros(iteration)
    a = 4
    i = 1
    map_values[0] = initial
    x_previo = initial
    while i < iteration:
        
        x = a * x_previo * (1 - x_previo)
        
        map_values[i] = x
        
        x_previo = x
        
        i+=1
    return map_values
    
def piecewiseMap(initial,iteration):
    map_values = np.zeros(iteration)
    P = 0.4
    i = 1
    map_values[0] = initial
    x_previo = initial
    while i < iteration:
        
        if P > x_previo and x_previo >= 0:
            x = x_previo / P
        if 1/2 > x_previo and x_previo >= P:
            x = ( x_previo - P ) / ( 0.5 - P )
        if (1-P) > x_previo and x_previo >= 1/2:
            x = ( 1 - P - x_previo ) / ( 0.5 - P )
        if 1 > x_previo and x_previo >= ( 1 - P ):
            x = ( 1 - x_previo ) / P
        
            
        
        map_values[i] = x
        
        x_previo = x
        
        i+=1
    return map_values

def sineMap(initial,iteration):
    map_values = np.zeros(iteration)
    a = 4
    i = 1
    map_values[0] = initial
    x_previo = initial
    while i < iteration:
        
        x = ( a / 4 ) * ( math.sin( math.pi * x_previo ) )
        
        map_values[i] = x
        
        x_previo = x
        
        i+=1
    return map_values

def singerMap(initial,iteration):
    map_values = np.zeros(iteration)
    a = 4
    u = 1.07
    i = 1
    map_values[0] = initial
    x_previo = initial
    while i < iteration:
        
        x = u * ( ( 7.86 * x_previo ) - ( 23.31 * pow(x_previo,2) ) + ( 28.75 * pow(x_previo,3) ) - ( 13.302875 * pow(x_previo,4) ) )
        
        map_values[i] = x
        
        x_previo = x
        
        i+=1
    return map_values

def sinusoidalMap(initial,iteration):
    map_values = np.zeros(iteration)
    a = 2.3
    i = 1
    map_values[0] = initial
    x_previo = initial
    while i < iteration:
        
        x = a * pow(x_previo,2) * math.sin( math.pi * x_previo )
        
        map_values[i] = x
        
        x_previo = x
        
        i+=1
    return map_values

def tentMap(initial,iteration):
    map_values = np.zeros(iteration)
    
    i = 1
    map_values[0] = initial
    x_previo = initial
    while i < iteration:
        
        if 0.7 > x_previo:
            x = x_previo / 0.7
        if x_previo >= 0.7:
            x = ( 10 / 3 ) * ( 1 - x_previo )
        
        map_values[i] = x
        
        x_previo = x
        
        i+=1
    return map_values

def graficarLogisticMap(iteration):
    iterationes = np.zeros(iteration)
    
    for i in range(iteration):
        iterationes[i] = i + 1
        
    plt.plot(iterationes, logisticMap(0.7,iteration), label="logistic Map")
    plt.title("logistic Map")
    plt.xlim(0,iteration)
    plt.ylim(0,1)
    
    plt.xlabel('$iterations (k)$')
    plt.ylabel('$Value (x_{k})$')
    plt.savefig(f"logistic Map.pdf")
    plt.close()
    
def graficarpiecewiseMap(iteration):
    iterationes = np.zeros(iteration)
    
    for i in range(iteration):
        iterationes[i] = i + 1
        
    plt.plot(iterationes, piecewiseMap(0.7,iteration), label="piecewise Map")
    plt.title("piecewise Map")
    plt.xlim(0,iteration)
    plt.ylim(0,1)
    
    plt.xlabel('$iterations (k)$')
    plt.ylabel('$Value (x_{k})$')
    plt.savefig(f"piecewise Map.pdf")
    plt.close()
    
def graficarsineMap(iteration):
    iterationes = np.zeros(iteration)
    
    for i in range(iteration):
        iterationes[i] = i + 1
        
    plt.plot(iterationes, sineMap(0.7,iteration), label="sine Map")
    plt.title("sine Map")
    plt.xlim(0,iteration)
    plt.ylim(0,1)
    
    plt.xlabel('$iterations (k)$')
    plt.ylabel('$Value (x_{k})$')
    plt.savefig(f"sine Map.pdf")
    plt.close()
    
def graficarsingerMap(iteration):
    iterationes = np.zeros(iteration)
    
    for i in range(iteration):
        iterationes[i] = i + 1
        
    plt.plot(iterationes, singerMap(0.7,iteration), label="singer Map")
    plt.title("singer Map")
    plt.xlim(0,iteration)
    plt.ylim(0,1)
    
    plt.xlabel('$iterations (k)$')
    plt.ylabel('$Value (x_{k})$')
    plt.savefig(f"singer Map.pdf")
    plt.close()
    
def graficarsinusoidalMap(iteration):
    iterationes = np.zeros(iteration)
    
    for i in range(iteration):
        iterationes[i] = i + 1
        
    plt.plot(iterationes, sinusoidalMap(0.7,iteration), label="sinusoidal Map")
    plt.title("sinusoidal Map")
    plt.xlim(0,iteration)
    plt.ylim(0,1)
    
    plt.xlabel('$iterations (k)$')
    plt.ylabel('$Value (x_{k})$')
    plt.savefig(f"sinusoidal Map.pdf")
    plt.close()
    
def graficartentMap(iteration):
    iterationes = np.zeros(iteration)
    
    for i in range(iteration):
        iterationes[i] = i + 1
        
    plt.plot(iterationes, tentMap(0.6,iteration), label="tent Map")
    plt.title("tent Map")
    plt.xlim(0,iteration)
    plt.ylim(0,1)
    
    plt.xlabel('$iterations (k)$')
    plt.ylabel('$Value (x_{k})$')
    plt.savefig(f"tent Map.pdf")
    plt.close()

def graficarcircleMap(iteration):
    iterationes = np.zeros(iteration)
    
    for i in range(iteration):
        iterationes[i] = i + 1
        
    plt.plot(iterationes, circleMap(0.7,iteration), label="circle Map")
    plt.title("circle Map")
    plt.xlim(0,iteration)
    plt.ylim(0,1)
    
    plt.xlabel('$iterations (k)$')
    plt.ylabel('$Value (x_{k})$')
    plt.savefig(f"circle Map.pdf")
    
    plt.close()




# graficar(100)

iteraciones = 100

graficarLogisticMap(iteraciones)
graficarcircleMap(iteraciones)
graficarpiecewiseMap(iteraciones)
graficarsineMap(iteraciones)
graficarsingerMap(iteraciones)
graficarsinusoidalMap(iteraciones)
graficartentMap(iteraciones)