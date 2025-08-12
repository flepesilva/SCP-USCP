import numpy as np
import random
from util import util

def iterarDOA(maxIter, iter, dimension, poblacion, fitness, typeProblem):
    """
    Dream Optimization Algorithm adaptado al framework.

    Parameters:
    - maxIter: Número total de iteraciones
    - iter: Iteración actual
    - dimension: Dimensión del problema
    - poblacion: Población actual (lista/array)
    - fitness: Fitness de cada individuo
    - typeProblem: "MIN" o "MAX"

    Returns:
    - poblacion_nueva: Nueva población actualizada
    """

    pop_size = len(poblacion)
    poblacion_nueva = [ind.copy() for ind in poblacion]

    # Límites del espacio de búsqueda
    lb, ub = 0.0, 1.0

    # Obtener mejor solución
    posicionesOrdenadas = util.selectionSort(fitness.copy())
    if typeProblem == "MIN":
        best_idx = posicionesOrdenadas[0]
    else:
        best_idx = posicionesOrdenadas[pop_size - 1]

    best_solution = poblacion[best_idx].copy()

    # Fase exploración vs explotación
    if iter < int(0.9 * maxIter):  # Exploración (90%)
        # Dividir población en 5 grupos
        group_size = pop_size // 5
        if group_size == 0:
            group_size = 1

        for m in range(min(5, pop_size)):
            start_idx = m * group_size
            end_idx = min((m + 1) * group_size, pop_size) if m < 4 else pop_size
            
            if start_idx >= pop_size:
                break

            # Mejor del grupo
            group_fitness = fitness[start_idx:end_idx]
            if typeProblem == "MIN":
                best_in_group_idx = start_idx + np.argmin(group_fitness)
            else:
                best_in_group_idx = start_idx + np.argmax(group_fitness)

            # Procesar cada individuo del grupo
            for j in range(start_idx, end_idx):
                individual = poblacion[j].copy()

                # Número de dimensiones a modificar
                k = np.random.randint(
                    max(1, dimension // (8 * (m + 1))),
                    max(1, dimension // (3 * (m + 1))) + 1
                )
                indices = np.random.permutation(dimension)[:k]

                # Perturbación principal (90% probabilidad)
                if np.random.rand() < 0.9:
                    for h in indices:
                        # Factor de decaimiento coseno
                        factor = (np.cos((iter + maxIter / 10) * np.pi / maxIter) + 1) / 2

                        # Perturbación aleatoria
                        delta = np.random.rand() * (ub - lb) + lb
                        individual[h] += delta * factor

                        # Manejo de límites
                        if individual[h] > ub or individual[h] < lb:
                            if dimension > 15:
                                others = list(range(pop_size))
                                others.remove(j)
                                if others:
                                    sel = np.random.choice(others)
                                    individual[h] = poblacion[sel][h]
                                else:
                                    individual[h] = np.random.rand() * (ub - lb) + lb
                            else:
                                individual[h] = np.random.rand() * (ub - lb) + lb
                else:
                    # Intercambio con individuo aleatorio
                    for h in indices:
                        sel = np.random.randint(pop_size)
                        individual[h] = poblacion[sel][h]

                poblacion_nueva[j] = individual

    else:  # Explotación (últimos 10%)
        for j in range(pop_size):
            individual = best_solution.copy()

            k = np.random.randint(2, max(2, dimension // 3) + 1)
            indices = np.random.permutation(dimension)[:k]

            for h in indices:
                factor = (np.cos(iter * np.pi / maxIter) + 1) / 2
                delta = np.random.rand() * (ub - lb) + lb
                individual[h] += delta * factor * 0.1  # Factor menor en explotación

                # Manejo de límites
                if individual[h] > ub or individual[h] < lb:
                    if dimension > 15:
                        others = list(range(pop_size))
                        if j in others:
                            others.remove(j)
                        if others:
                            sel = np.random.choice(others)
                            individual[h] = poblacion[sel][h]
                        else:
                            individual[h] = np.random.rand() * (ub - lb) + lb
                    else:
                        individual[h] = np.random.rand() * (ub - lb) + lb

            poblacion_nueva[j] = individual

    return poblacion_nueva