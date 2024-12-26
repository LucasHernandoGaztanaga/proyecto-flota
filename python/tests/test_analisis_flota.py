import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import sys
import tempfile
import os

sys.path.append(str(Path(__file__).parent.parent / 'src'))

from analisis_flota import AnalizadorFlota
from utils import validar_datos, generar_reporte_excel

@pytest.fixture
def datos_prueba():
    """Fixture que proporciona datos de prueba básicos."""
    return pd.DataFrame({
        'ID_Vehículo': ['V001', 'V002', 'V003', 'V004', 'V005'],
        'Kilometraje': [25000, 15000, 18000, 22000, 12000],
        'Último_Mantenimiento': [
            datetime.now() - timedelta(days=30),   # Reciente
            datetime.now() - timedelta(days=200),  # Antiguo
            datetime.now() - timedelta(days=10),   # Muy reciente
            datetime.now() - timedelta(days=190),  # Casi 6 meses
            datetime.now() - timedelta(days=185)   # Límite
        ],
        'Estado': ['activo', 'inactivo', 'en_reparación', 'activo', 'inactivo']
    })

@pytest.fixture
def analizador(tmp_path):
    """Fixture que proporciona una instancia del analizador con archivos temporales."""
    archivo_entrada = tmp_path / "test_flota.csv"
    archivo_salida = tmp_path / "test_mantenimiento.csv"
    return AnalizadorFlota(str(archivo_entrada), str(archivo_salida))

def test_validacion_datos_kilometraje_negativo():
    """Prueba la validación de kilometraje negativo."""
    datos = pd.DataFrame({
        'ID_Vehículo': ['V001'],
        'Kilometraje': [-1000],
        'Último_Mantenimiento': [datetime.now()],
        'Estado': ['activo']
    })
    
    with pytest.raises(ValueError, match="valores negativos"):
        validar_datos(datos)

def test_validacion_datos_estado_invalido():
    """Prueba la validación de estado inválido."""
    datos = pd.DataFrame({
        'ID_Vehículo': ['V001'],
        'Kilometraje': [1000],
        'Último_Mantenimiento': [datetime.now()],
        'Estado': ['estado_invalido']
    })
    
    with pytest.raises(ValueError, match="Estados inválidos"):
        validar_datos(datos)

def test_validacion_datos_fecha_futura():
    """Prueba la validación de fecha futura."""
    datos = pd.DataFrame({
        'ID_Vehículo': ['V001'],
        'Kilometraje': [1000],
        'Último_Mantenimiento': [datetime.now() + timedelta(days=1)],
        'Estado': ['activo']
    })
    
    with pytest.raises(ValueError, match="fechas de mantenimiento futuras"):
        validar_datos(datos)

def test_identificar_mantenimiento_requerido(analizador, datos_prueba):
    """Prueba la identificación correcta de vehículos que necesitan mantenimiento."""
    resultados = analizador.identificar_mantenimiento_requerido(datos_prueba)
    
    # Verificar vehículos que necesitan mantenimiento por kilometraje
    assert 'V001' in resultados['ID_Vehículo'].values  # > 20000 km
    assert 'V004' in resultados['ID_Vehículo'].values  # > 20000 km
    
    # Verificar vehículos que necesitan mantenimiento por tiempo
    assert 'V002' in resultados['ID_Vehículo'].values  # > 180 días
    
    # Verificar motivos correctos
    v001_motivo = resultados[resultados['ID_Vehículo'] == 'V001']['Motivo_Mantenimiento'].iloc[0]
    assert 'kilometraje_excedido' in v001_motivo
    
    v002_motivo = resultados[resultados['ID_Vehículo'] == 'V002']['Motivo_Mantenimiento'].iloc[0]
    assert 'tiempo_excedido' in v002_motivo

def test_calcular_estadisticas(analizador, datos_prueba):
    """Prueba el cálculo correcto de estadísticas por estado."""
    estadisticas = analizador.calcular_estadisticas(datos_prueba)
    
    # Verificar que todos los estados están presentes
    assert set(estadisticas.index) == {'activo', 'inactivo', 'en_reparación'}
    
    # Verificar cálculos para estado 'activo'
    activo_stats = estadisticas.loc['activo']
    assert activo_stats[('Kilometraje', 'count')] == 2  # Dos vehículos activos
    assert activo_stats[('ID_Vehículo', 'count')] == 2
    
    # Verificar suma total de kilometraje
    total_km = estadisticas[('Kilometraje', 'sum')].sum()
    assert total_km == datos_prueba['Kilometraje'].sum()

def test_generar_reporte_excel(tmp_path, datos_prueba, analizador):
    """Prueba la generación correcta del reporte Excel."""
    archivo_reporte = tmp_path / "reporte_test.xlsx"
    
    # Generar reporte
    estadisticas = analizador.calcular_estadisticas(datos_prueba)
    mantenimiento = analizador.identificar_mantenimiento_requerido(datos_prueba)
    generar_reporte_excel(datos_prueba, mantenimiento, estadisticas, str(archivo_reporte))
    
    # Verificar que el archivo existe
    assert archivo_reporte.exists()
    
    # Verificar contenido del Excel
    with pd.ExcelFile(archivo_reporte) as excel:
        assert set(excel.sheet_names) == {'Datos_Completos', 'Mantenimiento_Requerido', 'Estadísticas'}
        
        # Verificar datos en cada hoja
        df_completos = pd.read_excel(excel, 'Datos_Completos')
        assert len(df_completos) == len(datos_prueba)
        
        df_mantenimiento = pd.read_excel(excel, 'Mantenimiento_Requerido')
        assert len(df_mantenimiento) > 0

def test_ejecutar_analisis_completo(tmp_path, datos_prueba):
    """Prueba la ejecución completa del análisis."""
    # Crear archivos temporales
    archivo_entrada = tmp_path / "test_flota.csv"
    archivo_salida = tmp_path / "test_mantenimiento.csv"
    
    # Guardar datos de prueba
    datos_prueba.to_csv(archivo_entrada, index=False)
    
    # Crear analizador y ejecutar
    analizador = AnalizadorFlota(str(archivo_entrada), str(archivo_salida))
    vehiculos_mantenimiento, estadisticas = analizador.ejecutar_analisis()
    
    # Verificar resultados
    assert archivo_salida.exists()
    assert len(vehiculos_mantenimiento) > 0
    assert not estadisticas.empty

def test_error_archivo_no_existe():
    """Prueba el manejo de error cuando el archivo de entrada no existe."""
    analizador = AnalizadorFlota("archivo_no_existe.csv")
    with pytest.raises(FileNotFoundError):
        analizador.cargar_datos()

def test_fechas_limite():
    """Prueba casos límite con fechas de mantenimiento."""
    datos_limite = pd.DataFrame({
        'ID_Vehículo': ['V001', 'V002'],
        'Kilometraje': [19999, 20001],  # Límite de kilometraje
        'Último_Mantenimiento': [
            datetime.now() - timedelta(days=180),  # Exactamente 6 meses
            datetime.now() - timedelta(days=181)   # Justo después de 6 meses
        ],
        'Estado': ['activo', 'activo']
    })
    
    analizador = AnalizadorFlota()
    resultados = analizador.identificar_mantenimiento_requerido(datos_limite)
    
    # Solo V002 debería necesitar mantenimiento
    assert len(resultados) == 1
    assert 'V002' in resultados['ID_Vehículo'].values

def test_columnas_requeridas():
    """Prueba que se validen las columnas requeridas."""
    datos_incompletos = pd.DataFrame({
        'ID_Vehículo': ['V001'],
        'Kilometraje': [1000]  # Faltan columnas requeridas
    })
    
    with pytest.raises(ValueError, match="Faltan columnas requeridas"):
        validar_datos(datos_incompletos)

def test_tipo_datos_kilometraje():
    """Prueba la validación del tipo de datos para kilometraje."""
    datos = pd.DataFrame({
        'ID_Vehículo': ['V001'],
        'Kilometraje': ['no_numerico'],  # Tipo de dato incorrecto
        'Último_Mantenimiento': [datetime.now()],
        'Estado': ['activo']
    })
    
    with pytest.raises(ValueError, match="debe ser numérica"):
        validar_datos(datos)

if __name__ == '__main__':
    pytest.main(['-v'])