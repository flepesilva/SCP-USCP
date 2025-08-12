# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository implements metaheuristic optimization algorithms to solve two variants of the Set Cover Problem (SCP):
- **SCP (Set Cover Problem)**: Minimizes the cost of covering all elements
- **USCP (Unicost Set Cover Problem)**: Minimizes the number of sets (uniform cost of 1 per set)

The framework supports multiple metaheuristic algorithms including DOA (Dream Optimization Algorithm), WSO (Water Strider Optimization), GWO (Grey Wolf Optimizer), SCA (Sine Cosine Algorithm), WOA (Whale Optimization Algorithm), and PSO (Particle Swarm Optimization).

## Core Architecture

### Problem Structure
- `Problem/SCP/`: Contains SCP implementation and test instances
  - `problem.py`: SCP class with fitness evaluation, repair mechanisms, and instance loading
  - `Instances/`: Standard SCP benchmark instances (scp41.txt to scpnrh5.txt)
- `Problem/USCP/`: Contains USCP implementation and test instances
  - `problem.py`: USCP class (similar to SCP but with uniform costs)
  - `Instances/`: USCP benchmark instances including cyclic (scpcyc*) and color (scpclr*) variants

### Metaheuristic Implementations
- `Metaheuristics/`: Each algorithm implements an `iterarX()` function following the framework pattern
  - Takes parameters: `(maxIter, iter, dimension, poblacion, fitness, typeProblem)`
  - Returns updated population for the next iteration
  - All algorithms operate on binary solutions (0/1 values)

### Solver Framework
- `Solver/solverSCP.py`: Main optimization loop for SCP problems
- `Solver/solverUSCP.py`: Main optimization loop for USCP problems  
- `Solver/solverSCP_ChaoticMaps.py`: SCP solver with chaotic map integration
- `Solver/solverUSCP_ChaoticMaps.py`: USCP solver with chaotic map integration

### Supporting Components
- `Discretization/discretization.py`: Binary discretization schemes for continuous metaheuristics
- `ChaoticMaps/chaoticMaps.py`: Chaotic map implementations for enhanced exploration
- `Diversity/`: Population diversity measurement tools
  - `hussainDiversity.py`: Hussain diversity metric
  - `XPLXTP.py`: Exploration vs exploitation percentage calculations

## Database System

The framework uses SQLite for experiment management:
- `BD/sqlite.py`: Database interface with tables for experiments, instances, results, and iterations
- `BD/resultados.db`: SQLite database storing all experimental data
- Supports concurrent experiment execution with proper locking mechanisms

## Key Development Commands

### Setup and Execution
```bash
# Initialize database (run once)
python crearBD.py

# Run single experiment execution
python main.py

# Run multiple parallel experiments
python levantarCMD.py  # Opens 3 parallel command windows

# Analyze results
python analisisSCP.py
```

### Dependencies
The project requires:
- `numpy` for numerical operations
- `scipy.sparse` for sparse matrix operations (used in repair mechanisms)
- `sqlite3` (built-in) for database operations
- `matplotlib/pandas` (likely for analysis scripts)

## Important Implementation Details

### Matrix Operations
Both SCP and USCP classes use optimized block-wise matrix operations (`matrix_dot_1`, `matrix_dot_2`) for efficient constraint evaluation on large instances.

### Repair Mechanisms
- **Simple Repair**: Randomly selects cheapest column to cover unsatisfied constraints
- **Complex Repair**: Uses sparse matrix operations and cost-to-coverage trade-off for efficient repair

### Experiment Configuration
Experiments are configured through the database with parameters stored as comma-separated strings:
- Format: `"iter:500,pop:50,DS:V4-STD,repair:simple,param:additional"`
- Supports chaotic map variants indicated by underscore in discretization scheme

### File Output
- Results stored in `Resultados/` directory as CSV files
- Format: `{MH}_{instance}_{experiment_id}.csv`
- Contains iteration-wise fitness, time, XPL, XPT, and diversity metrics

## Testing

No formal test framework is present. Validation occurs through:
- Comparison with known optimal solutions (stored in problem classes)
- Feasibility testing via constraint satisfaction checks
- Cross-validation between different metaheuristic results