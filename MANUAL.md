# Manual de Experimentos SCP-USCP

Este manual explica cómo configurar y ejecutar experimentos con metaheurísticas para resolver problemas SCP (Set Cover Problem) y USCP (Unicost Set Cover Problem).

## 🚀 Inicio Rápido

### 1. Preparación del Entorno
```bash
# Verificar que Python esté instalado
python --version  # o python3 --version

# Instalar dependencias (si es necesario)
pip install numpy scipy matplotlib pandas
```

### 2. Configuración Inicial
```bash
# Limpiar y preparar base de datos
python crearBD.py

# Verificar que las instancias se cargaron correctamente
python -c "from BD.sqlite import BD; bd = BD(); print('Instancias USCP:', len(bd.obtenerInstancias('\"cyc06\"')))"
```

## 📊 Configuración de Experimentos

### Archivo Principal: `poblarDB.py`

Edita este archivo para configurar tus experimentos:

```python
# Activar/desactivar tipos de problema
scp  = False  # Set Cover Problem
uscp = True   # Unicost Set Cover Problem

# Metaheurísticas disponibles
mhs = ['DOA', 'GWO', 'SCA', 'WOA', 'PSO', 'WSO']

# Instancias a probar (línea 46-49)
instancias = bd.obtenerInstancias(f'''
    "clr10", "clr11", "clr12", "clr13",
    "cyc06", "cyc07", "cyc08", "cyc09", "cyc10", "cyc11"
''')

# Parámetros de experimento
iteraciones = 100   # Número de iteraciones
experimentos = 30   # Corridas por configuración  
poblacion = 50      # Tamaño de población

# Configuraciones de binarización
binarizaciones = [
    'V3-STD',           # DOA estándar
    'V3-STD_LOG',       # DOA + mapa logístico
    'V3-ELIT_LOG',      # DOA + mapa logístico + elitista
    'V3-ELIT_CIRCLE'    # DOA + mapa circular + elitista
]
```

### Instancias Disponibles

**USCP (Beasley):**
- `clr10, clr11, clr12, clr13` - Color instances
- `cyc06, cyc07, cyc08, cyc09, cyc10, cyc11` - Cycle instances
- `u41-u410, u51-u510, u61-u65` - Standard instances
- `ua1-ua5, ub1-ub5, uc1-uc5, ud1-ud5` - Additional sets

**SCP:**
- `41-410, 51-510, 61-65` - Standard instances
- `a1-a5, b1-b5, c1-c5, d1-d5` - Additional sets
- `nre1-nre5, nrf1-nrf5, nrg1-nrg5, nrh1-nrh5` - OR-Library instances

## 🔧 Ejecución de Experimentos

### Método 1: Ejecución Secuencial
```bash
# 1. Cargar experimentos en la base de datos
python poblarDB.py

# 2. Ejecutar todos los experimentos
python main.py

# 3. Analizar resultados
python analisisSCP.py
```

### Método 2: Ejecución Paralela (macOS/Linux)
```bash
# 1. Cargar experimentos
python poblarDB.py

# 2. Ejecutar en paralelo (3 procesos)
python levantarCLI.py

# 3. Monitorear progreso
# Los procesos se ejecutan en terminales separadas
# Puedes ver el progreso en cada terminal
```

### Método 3: Test Rápido
```bash
# Para pruebas rápidas, modifica poblarDB.py:
iteraciones = 20
poblacion = 5
experimentos = 1
binarizaciones = ['V3-STD', 'V3-STD_LOG']

# Luego ejecuta normalmente
python crearBD.py && python poblarDB.py && python main.py
```

## 📈 Monitoreo y Resultados

### Durante la Ejecución
- **Archivos CSV**: Se crean en `Resultados/` con formato `{MH}_{instancia}_{id}.csv`
- **Progreso**: Se muestra en consola cada 25% de las iteraciones
- **Base de datos**: Estados se actualizan en tiempo real

### Análisis de Resultados
```bash
# Análisis completo
python analisisSCP.py

# Consultas manuales a la base de datos
sqlite3 BD/resultados.db "SELECT estado, COUNT(*) FROM experimentos GROUP BY estado;"
sqlite3 BD/resultados.db "SELECT AVG(fitness) FROM resultados WHERE fk_id_experimento IN (SELECT id_experimento FROM experimentos WHERE MH='DOA');"
```

### Archivos de Resultados
- **CSV**: Datos iteración por iteración (fitness, tiempo, diversidad)
- **Base de datos**: Metadatos de experimentos y resultados finales
- **Análisis**: Estadísticas comparativas entre algoritmos

## 🔄 Configuraciones Avanzadas

### Mapas Caóticos Disponibles
- `LOG` - Logistic Map
- `CIRCLE` - Circle Map  
- `PIECE` - Piecewise Map
- `SINE` - Sine Map
- `SINGER` - Singer Map
- `SINU` - Sinusoidal Map
- `TENT` - Tent Map

### Funciones de Transferencia
- `V1-V4` - V-shaped functions
- `S1-S4` - S-shaped functions

### Métodos de Binarización
- `STD` - Standard
- `COM` - Complement
- `PS` - Probability Strategy
- `ELIT` - Elitist

### Tipos de Reparación
- `simple` - Reparación greedy básica
- `complex` - Reparación con análisis costo-beneficio

## 🛠️ Solución de Problemas

### Error: "No such table: experimentos"
```bash
python crearBD.py  # Reconstruir base de datos
```

### Error: "IndexError: index X is out of bounds"
- Verificar que la población sea >= 5
- Verificar que las instancias existan en la carpeta correspondiente

### Experimentos muy lentos
- Reducir `iteraciones` y `poblacion` en `poblarDB.py`
- Usar menos instancias para pruebas

### Sin resultados en análisis
- Verificar que los experimentos terminaron (`estado = 'terminado'`)
- Ejecutar `python main.py` hasta completar todos los experimentos

## 📝 Estructura de Archivos

```
SCP-USCP/
├── BD/                     # Base de datos
├── Metaheuristics/         # Algoritmos (DOA, GWO, etc.)
├── Problem/               # Definiciones SCP/USCP
├── Solver/                # Loops de optimización
├── ChaoticMaps/           # Mapas caóticos
├── Discretization/        # Funciones de binarización
├── Resultados/            # Archivos CSV de resultados
├── crearBD.py            # Inicializar base de datos
├── poblarDB.py           # Configurar experimentos
├── main.py               # Ejecutar experimentos
├── analisisSCP.py        # Analizar resultados
└── levantarCLI.py        # Ejecución paralela (macOS)
```

## 🎯 Ejemplos de Uso

### Comparar DOA vs DOA Caótico
```python
# En poblarDB.py
mhs = ['DOA']
binarizaciones = ['V3-STD', 'V3-STD_LOG', 'V3-ELIT_CIRCLE']
```

### Experimentar con todas las metaheurísticas
```python
# En poblarDB.py  
mhs = ['DOA', 'GWO', 'SCA', 'WOA', 'PSO']
binarizaciones = ['V3-STD']
```

### Test en instancia específica
```python
# En poblarDB.py
instancias = bd.obtenerInstancias(f'''
    "cyc06"
''')
```