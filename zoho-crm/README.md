# Sistema de Gestión de Flota - Zoho CRM

Implementación del sistema de gestión de flota utilizando Zoho CRM y Deluge Script.

## Estructura del Proyecto

```
zoho-crm/
├── scripts/
│   └── RevisionMantenimiento.deluge
├── docs/
│   └── configuracion.md
└── README.md
```

## Descripción

Este módulo implementa la lógica de mantenimiento de vehículos en Zoho CRM utilizando Deluge Script. La función principal evalúa dos condiciones para determinar si un vehículo necesita mantenimiento:
- Kilometraje superior a 20,000 km desde el último servicio
- Más de 6 meses desde el último mantenimiento

## Funcionalidades

- Evaluación de condiciones de mantenimiento
- Generación de alertas prioritarias
- Mensajes específicos según la condición

## Uso en Zoho CRM

1. **Configuración Inicial**:
   ```
   1. Acceder a Zoho CRM
   2. Ir a Setup > Functions > Create New Function
   3. Copiar el contenido de RevisionMantenimiento.deluge
   ```

2. **Parámetros de Entrada**:
   ```javascript
   kilometros_recorridos: Número
   fecha_ultimo_mantenimiento: Fecha
   ```

3. **Valores de Retorno**:
   - "ALERTA PRIORITARIA: Requiere mantenimiento inmediato..."
   - "Mantenimiento requerido: Excede kilometraje..."
   - "Mantenimiento requerido: Excede tiempo..."
   - "No requiere mantenimiento"

## Ejemplos de Uso

```javascript
// Caso 1: Excede ambos límites
evaluarMantenimiento(25000, addMonths(today, -7));

// Caso 2: Solo excede kilometraje
evaluarMantenimiento(21000, addMonths(today, -3));
```

## Documentación Adicional

- [Documentación oficial de Deluge](https://deluge.zoho.com/learndeluge#Welcome!)
- [Configuración detallada](./docs/configuracion.md)

## Mantenimiento

Para actualizar la lógica de mantenimiento:
1. Modificar los umbrales en RevisionMantenimiento.deluge
2. Actualizar la función en Zoho CRM
3. Realizar pruebas con diferentes escenarios