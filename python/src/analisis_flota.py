#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import logging
from datetime import datetime, timedelta
from pathlib import Path
from utils import configurar_logging, validar_datos, generar_reporte_excel

# Configuración de logging
logger = logging.getLogger(__name__)

class AnalizadorFlota:
    """Clase principal para el análisis de datos de la flota."""
    
    def __init__(self, archivo_entrada="data/flota.csv", archivo_salida="data/mantenimiento_requerido.csv"):
        """
        Inicializa el analizador de flota.
        
        Args:
            archivo_entrada (str): Ruta al archivo CSV de entrada
            archivo_salida (str): Ruta donde se guardará el archivo de salida
        """
        self.archivo_entrada = Path(archivo_entrada)
        self.archivo_salida = Path(archivo_salida)
        self.fecha_actual = datetime.now()
        
    def cargar_datos(self):
        """Carga y valida los datos del archivo CSV."""
        try:
            df = pd.read_csv(self.archivo_entrada)
            df['Último_Mantenimiento'] = pd.to_datetime(df['Último_Mantenimiento'])
            validar_datos(df)
            return df
        except Exception as e:
            logger.error(f"Error al cargar datos: {str(e)}")
            raise
    
    def identificar_mantenimiento_requerido(self, df):
        """
        Identifica vehículos que necesitan mantenimiento.
        
        Args:
            df (pandas.DataFrame): DataFrame con datos de la flota
            
        Returns:
            pandas.DataFrame: Vehículos que necesitan mantenimiento
        """
        # Calcular días desde último mantenimiento
        dias_desde_mantenimiento = (self.fecha_actual - df['Último_Mantenimiento']).dt.days
        
        # Criterios de mantenimiento
        km_excedido = df['Kilometraje'] > 20000
        tiempo_excedido = dias_desde_mantenimiento > 180
        
        # Identificar vehículos que necesitan mantenimiento
        necesitan_mantenimiento = df[km_excedido | tiempo_excedido].copy()
        
        # Agregar motivo de mantenimiento
        necesitan_mantenimiento['Motivo_Mantenimiento'] = ''
        necesitan_mantenimiento.loc[km_excedido, 'Motivo_Mantenimiento'] += 'kilometraje_excedido'
        necesitan_mantenimiento.loc[tiempo_excedido, 'Motivo_Mantenimiento'] += '|tiempo_excedido'
        necesitan_mantenimiento['Motivo_Mantenimiento'] = necesitan_mantenimiento['Motivo_Mantenimiento'].str.strip('|')
        
        return necesitan_mantenimiento
    
    def calcular_estadisticas(self, df):
        """
        Calcula estadísticas agrupadas por estado.
        
        Args:
            df (pandas.DataFrame): DataFrame con datos de la flota
            
        Returns:
            pandas.DataFrame: Estadísticas por estado
        """
        return df.groupby('Estado').agg({
            'Kilometraje': ['sum', 'mean', 'count'],
            'ID_Vehículo': 'count'
        }).round(2)
    
    def ejecutar_analisis(self):
        """Ejecuta el análisis completo de la flota."""
        try:
            logger.info("Iniciando análisis de flota...")
            
            # Cargar y procesar datos
            df = self.cargar_datos()
            vehiculos_mantenimiento = self.identificar_mantenimiento_requerido(df)
            estadisticas = self.calcular_estadisticas(df)
            
            # Guardar resultados
            vehiculos_mantenimiento.to_csv(self.archivo_salida, index=False)
            
            # Generar reporte Excel (opcional)
            generar_reporte_excel(df, vehiculos_mantenimiento, estadisticas)
            
            logger.info(f"Análisis completado. Resultados guardados en {self.archivo_salida}")
            
            return vehiculos_mantenimiento, estadisticas
            
        except Exception as e:
            logger.error(f"Error durante el análisis: {str(e)}")
            raise

def main():
    """Función principal."""
    try:
        configurar_logging()
        analizador = AnalizadorFlota()
        vehiculos_mantenimiento, estadisticas = analizador.ejecutar_analisis()
        
        # Mostrar resultados
        print("\n=== Estadísticas por Estado ===")
        print(estadisticas)
        print(f"\nSe identificaron {len(vehiculos_mantenimiento)} vehículos que requieren mantenimiento.")
        print(f"Los detalles se han guardado en: {analizador.archivo_salida}")
        
    except Exception as e:
        logger.error(f"Error en la ejecución: {str(e)}")
        raise

if __name__ == "__main__":
    main()