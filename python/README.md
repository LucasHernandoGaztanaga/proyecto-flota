# Sistema de Análisis de Flota Vehicular

Este sistema permite analizar datos de una flota de vehículos para identificar necesidades de mantenimiento y generar estadísticas relevantes.

## Características

- Identificación de vehículos que requieren mantenimiento
- Análisis de kilometraje por estado de vehículo
- Generación de reportes detallados
- Manejo automático de fechas y cálculos de períodos

## Requisitos

- Python 3.8 o superior
- Dependencias listadas en `requirements.txt`

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd sistema-flota
```

2. Crear y activar entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Unix/MacOS
# o
venv\Scripts\activate  # En Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Uso

1. Preparar el archivo CSV de entrada en la carpeta `data/` con el nombre `flota.csv`

2. Ejecutar el análisis:
```bash
python src/analisis_flota.py
```

3. Verificar los resultados en:
   - Consola: Estadísticas generales
   - `data/mantenimiento_requerido.csv`: Reporte detallado

## Estructura de Archivos CSV

### Archivo de entrada (flota.csv):
```csv
ID_Vehículo,Kilometraje,Último_Mantenimiento,Estado
V001,25000,2024-01-15,activo
```

### Archivo de salida (mantenimiento_requerido.csv):
```csv
ID_Vehículo,Kilometraje,Último_Mantenimiento,Estado,Motivo_Mantenimiento
V001,25000,2024-01-15,activo,kilometraje_excedido
```

## Pruebas

Ejecutar las pruebas unitarias:
```bash
pytest tests/
```
