# CONTEXT.md

## Propósito del Repositorio

Este repositorio implementa un **framework completo de investigación** para el análisis comparativo de **metaheurísticas** aplicadas a dos variantes del **Set Cover Problem (SCP)**:

- **SCP (Set Cover Problem)**: Minimiza el costo total de cubrir todos los elementos
- **USCP (Unicost Set Cover Problem)**: Minimiza el número de conjuntos (costo uniforme de 1 por conjunto)

El framework está diseñado para **investigación académica** y permite evaluar sistemáticamente el rendimiento de diferentes algoritmos metaheurísticos con y sin **mapas caóticos**.

## Estructura del Framework

### 🔬 Algoritmos Metaheurísticos Implementados
- **DOA (Dream Optimization Algorithm)** - ✅ Recién agregado
- **WSO (Water Strider Optimization)**
- **GWO (Grey Wolf Optimizer)**
- **SCA (Sine Cosine Algorithm)**
- **WOA (Whale Optimization Algorithm)**
- **PSO (Particle Swarm Optimization)**

### 🌪️ Mapas Caóticos Disponibles
El framework integra 7 tipos de mapas caóticos para mejorar la exploración:
- **LOG (Logistic Map)**
- **PIECE (Piecewise Map)**
- **SINE (Sine Map)**
- **SINGER (Singer Map)**
- **SINU (Sinusoidal Map)**
- **TENT (Tent Map)**
- **CIRCLE (Circle Map)**

### 🧬 Esquemas de Discretización
- **Funciones de Transferencia**: S1-S4, V1-V4
- **Operadores Binarios**: STD, COM, PS, ELIT
- **Integración con Mapas Caóticos**: Formato `{Función}-{Operador}_{Mapa}`

### 📊 Sistema de Gestión de Experimentos
- **Base de datos SQLite**: Almacena configuraciones, resultados e iteraciones
- **Ejecución paralela**: Soporte para múltiples experimentos concurrentes
- **Métricas integradas**: Fitness, tiempo, diversidad, XPL/XPT

## Trabajo Actual: Análisis Comparativo DOA con Mapas Caóticos

### 🎯 Objetivo Principal
Realizar un **análisis comparativo exhaustivo** del algoritmo **DOA (Dream Optimization Algorithm)** evaluando:

1. **DOA estándar** vs **DOA con mapas caóticos (BCDOA)**
2. **Efectividad de diferentes mapas caóticos** en el rendimiento del DOA
3. **Comparación con otras metaheurísticas** del framework

### 📋 Estado Actual del DOA

#### ✅ Completado:
- ✅ Implementación del algoritmo DOA en `/Metaheuristics/DOA.py`
- ✅ Integración con el framework de experimentos
- ✅ Configuración de experimentos en `poblarDB.py`
- ✅ Resultados parciales generados (archivos DOA_*.csv en `/Resultados/`)

#### ⚠️ Problemas Identificados:
- 🐛 **Bug crítico**: Variable `population` no definida en solvers con mapas caóticos (líneas 138 y 143)
- 🔧 **Inconsistencia de parámetros**: `iterarDOA` espera `fitness` pero recibe otras variables
- 📊 **Necesidad de análisis**: Falta análisis estadístico de resultados existentes

#### 🔄 Pendiente:
- 🔧 Corrección de bugs en solvers
- 📊 Análisis estadístico completo de resultados
- 📈 Generación de gráficos comparativos
- 📝 Documentación de findings

## Comandos Clave del Framework

### 🚀 Ejecución de Experimentos
```bash
# Configurar base de datos (una vez)
python crearBD.py

# Poblar experimentos DOA
python poblarDB.py

# Ejecutar experimentos individualmente
python main.py

# Ejecutar experimentos en paralelo
python levantarCMD.py  # Abre 3 ventanas CMD paralelas
```

### 📊 Análisis de Resultados
```bash
# Análisis estadístico y visualización
python analisisSCP.py
```

## Configuración de Experimentos DOA

### 📋 Configuración Actual en `poblarDB.py`:
- **Instancias USCP**: clr10-13, cyc06-11
- **Iteraciones**: 20
- **Población**: 5
- **Binarizaciones**: 
  - `V3-STD` (DOA estándar)
  - `V3-STD_LOG` (DOA con mapa logístico)

### 🔄 Expansión Planificada:
- Incluir todos los mapas caóticos disponibles
- Aumentar número de experimentos para significancia estadística
- Probar con instancias SCP adicionales

## Arquitectura de Datos

### 🗃️ Base de Datos SQLite (`BD/resultados.db`):
- **Tabla experimentos**: Configuraciones de pruebas
- **Tabla instancias**: Información de problemas
- **Tabla resultados**: Fitness final y tiempos
- **Tabla iteraciones**: Evolución detallada por iteración

### 📁 Estructura de Resultados:
```
Resultados/
├── DOA_scpcyc06_*.csv    # Resultados DOA existentes
├── {MH}_{instancia}_{id}.csv  # Formato general
```

### 📊 Métricas Capturadas:
- **Fitness por iteración**
- **Tiempo de ejecución**
- **Diversidad de población (Hussain)**
- **XPL/XPT (Exploración vs Explotación)**

## Flujo de Trabajo de Investigación

1. **📝 Configuración**: Definir experimentos en `poblarDB.py`
2. **🚀 Ejecución**: Ejecutar experimentos con `main.py` o en paralelo
3. **📊 Análisis**: Procesar resultados con `analisisSCP.py`
4. **📈 Visualización**: Generar gráficos y tablas comparativas
5. **📋 Documentación**: Interpretar y documentar findings

## Próximos Pasos

### 🔧 Correcciones Inmediatas:
1. Arreglar bugs en solvers con mapas caóticos
2. Validar consistencia de parámetros en `iterarDOA`

### 📊 Análisis Completo:
1. Ejecutar experimentos DOA con todos los mapas caóticos
2. Realizar análisis estadístico (Mann-Whitney U, etc.)
3. Generar visualizaciones comparativas
4. Documentar efectividad de cada mapa caótico

### 📈 Extensiones Futuras:
1. Implementar BCDOA como algoritmo separado
2. Comparar con estado del arte
3. Análisis de convergencia detallado
4. Optimización de parámetros