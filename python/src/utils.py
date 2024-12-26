import logging
import pandas as pd
from pathlib import Path
from datetime import datetime

def configurar_logging():
    """Configura el sistema de logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('flota_analisis.log'),
            logging.StreamHandler()
        ]
    )

def validar_datos(df):
    """
    Valida la integridad y formato de los datos.
    
    Args:
        df (pandas.DataFrame): DataFrame a validar
        
    Raises:
        ValueError: Si los datos no cumplen con los requisitos
    """
    # Verificar columnas requeridas
    columnas_requeridas = {'ID_Vehículo', 'Kilometraje', 'Último_Mantenimiento', 'Estado'}
    if not columnas_requeridas.issubset(df.columns):
        raise ValueError(f"Faltan columnas requeridas. Necesarias: {columnas_requeridas}")
    
    # Verificar tipos de datos
    if not pd.api.types.is_numeric_dtype(df['Kilometraje']):
        raise ValueError("La columna 'Kilometraje' debe ser numérica")
    
    # Verificar valores negativos en kilometraje
    if (df['Kilometraje'] < 0).any():
        raise ValueError("Se encontraron valores negativos en el kilometraje")
    
    if not pd.api.types.is_datetime64_dtype(df['Último_Mantenimiento']):
        raise ValueError("La columna 'Último_Mantenimiento' debe ser de tipo fecha")
    
    # Verificar fechas futuras
    if (df['Último_Mantenimiento'] > datetime.now()).any():
        raise ValueError("Se encontraron fechas de mantenimiento futuras")
    
    # Verificar valores válidos
    estados_validos = {'activo', 'inactivo', 'en_reparación'}
    estados_invalidos = set(df['Estado'].unique()) - estados_validos
    if estados_invalidos:
        raise ValueError(f"Estados inválidos encontrados: {estados_invalidos}")

def generar_reporte_excel(df_original, df_mantenimiento, df_estadisticas, 
                         archivo_salida="data/reporte_flota.xlsx"):
    """
    Genera un reporte detallado en Excel.
    
    Args:
        df_original (pandas.DataFrame): Datos originales de la flota
        df_mantenimiento (pandas.DataFrame): Vehículos que necesitan mantenimiento
        df_estadisticas (pandas.DataFrame): Estadísticas por estado
        archivo_salida (str): Ruta del archivo Excel de salida
    """
    try:
        with pd.ExcelWriter(archivo_salida, engine='openpyxl') as writer:
            # Datos originales
            df_original.to_excel(writer, sheet_name='Datos_Completos', index=False)
            
            # Vehículos que necesitan mantenimiento
            df_mantenimiento.to_excel(writer, sheet_name='Mantenimiento_Requerido', index=False)
            
            # Estadísticas
            df_estadisticas.to_excel(writer, sheet_name='Estadísticas')
            
        logging.info(f"Reporte Excel generado exitosamente en: {archivo_salida}")
        
    except Exception as e:
        logging.error(f"Error al generar reporte Excel: {str(e)}")
        raise

def crear_estructura_directorios():
    """Crea la estructura de directorios necesaria para el proyecto."""
    directorios = ['data', 'logs']
    for directorio in directorios:
        Path(directorio).mkdir(parents=True, exist_ok=True)