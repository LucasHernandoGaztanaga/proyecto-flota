# Sistema de Gestión de Flota Vehicular

Este repositorio contiene tres implementaciones de un sistema de gestión de flota vehicular utilizando diferentes tecnologías y enfoques: Python, Java y Zoho CRM con Deluge Script.

## Estructura del Repositorio

```
.
├── proyecto-flota-python/     # Implementación en Python
│   ├── data/                  # Datos de entrada y salida
│   ├── src/                   # Código fuente
│   ├── tests/                 # Pruebas unitarias
│   └── requirements.txt       # Dependencias
│
├── proyecto-flota-java/       # Implementación en Java
│   ├── sistema-flota/         # Proyecto Maven
│   ├── src/                   # Código fuente
│   └── pom.xml               # Configuración Maven
│
└── zoho-crm/                 # Implementación en Zoho CRM
    ├── scripts/              # Scripts de Deluge
    └── docs/                 # Documentación de configuración
```

## Requerimientos Funcionales

- Gestión de vehículos (ID, kilometraje, último mantenimiento, estado)
- Identificación de vehículos que necesitan mantenimiento:
  - Kilometraje > 20,000
  - Más de 6 meses desde el último mantenimiento
- Agrupación de vehículos por estado con resumen de kilometraje

## Tecnologías Utilizadas

### Python
- Python 3.8+
- pandas
- pytest
- python-dateutil

### Java
- Java 11
- Maven
- JUnit 5

### Zoho CRM
- Deluge Script
- Zoho CRM Modules
- Zoho Workflows

## Comparación de Implementaciones

| Característica           | Python        | Java         | Zoho CRM      |
|-------------------------|---------------|--------------|---------------|
| Tipo                    | Script        | OOP         | Low-Code      |
| Manejo de Datos         | pandas        | Collections | CRM Module    |
| Testing                 | pytest        | JUnit       | Manual        |
| Deployment             | Local/Server  | Local/Server| Cloud         |

## Cómo Empezar

Cada proyecto tiene su propio README con instrucciones detalladas de instalación y uso:

- [Instrucciones Python](./proyecto-flota-python/README.md)
- [Instrucciones Java](./proyecto-flota-java/sistema-flota/README.md)
- [Instrucciones Zoho CRM](./zoho-crm/README.md)

## Ejemplos de Uso

### Python
```python
from analisis_flota import AnalizadorFlota
analizador = AnalizadorFlota()
resultados = analizador.obtener_vehiculos_mantenimiento()
```

### Java
```java
GestorFlota gestor = new GestorFlota();
List<Vehiculo> mantenimiento = gestor.obtenerVehiculosParaMantenimiento();
```

### Zoho CRM
```javascript
resultado = evaluarMantenimiento(kilometros, fecha_ultimo_mantenimiento);
```
