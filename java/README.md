# Sistema de Flota - Implementación Java

Sistema de gestión de flota vehicular implementado en Java utilizando programación orientada a objetos y Maven como gestor de dependencias.

## Requisitos Previos

- Java JDK 11 o superior
- Maven 3.6 o superior

## Estructura del Proyecto

```
sistema-flota/
├── src/
│   ├── main/
│   │   └── java/
│   │       └── com/
│   │           └── flota/
│   │               ├── model/
│   │               │   ├── Vehiculo.java
│   │               │   └── EstadoVehiculo.java
│   │               ├── service/
│   │               │   └── GestorFlota.java
│   │               └── Main.java
│   └── test/
│       └── java/
│           └── com/
│               └── flota/
│                   └── service/
│                       └── GestorFlotaTest.java
├── pom.xml
└── README.md
```

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-repositorio>
cd proyecto-flota-java/sistema-flota
```

2. Compilar el proyecto:
```bash
mvn clean install
```

## Uso

1. Ejecutar la aplicación:
```bash
mvn exec:java
```

2. Ejecutar pruebas:
```bash
mvn test
```

## Funcionalidades Principales

- `Vehiculo`: Clase que representa un vehículo con sus atributos
- `GestorFlota`: Clase principal que gestiona la lógica de negocio
  - Identificación de vehículos para mantenimiento
  - Agrupación y resumen por estado

## Ejemplos de Uso

```java
// Crear gestor de flota
GestorFlota gestor = new GestorFlota();

// Agregar vehículo
gestor.agregarVehiculo(new Vehiculo("V001", 25000, 
    LocalDate.now().minusMonths(2), EstadoVehiculo.ACTIVO));

// Obtener vehículos para mantenimiento
List<Vehiculo> mantenimiento = gestor.obtenerVehiculosParaMantenimiento();

// Obtener resumen por estado
Map<EstadoVehiculo, ResumenEstado> resumen = gestor.obtenerResumenPorEstado();
```

## Desarrollo

El proyecto utiliza:
- Maven para gestión de dependencias
- JUnit 5 para pruebas unitarias
- Java 11 features (var, métodos de String mejorados)

## Contribuir

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/nueva-caracteristica`)
3. Commit cambios (`git commit -m 'Agrega nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Crear Pull Request

## Licencia

Distribuido bajo la Licencia MIT. Ver `LICENSE` para más información.