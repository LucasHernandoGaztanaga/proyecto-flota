# Configuración del Sistema en Zoho CRM

## Configuración Inicial

### 1. Crear Módulo de Vehículos

1. Ir a Setup > Developer Space > Módulos Personalizados
2. Crear nuevo módulo "Vehículos"
3. Agregar campos:
   ```
   - ID_Vehiculo (Texto, Único)
   - Kilometraje_Actual (Número)
   - Fecha_Ultimo_Mantenimiento (Fecha)
   - Estado (Lista desplegable: Activo, Inactivo, En Mantenimiento)
   ```

### 2. Configurar Función Personalizada

1. Ir a Setup > Functions
2. Crear nueva función:
   ```
   Nombre: evaluarMantenimiento
   Parámetros: 
   - kilometros_recorridos (Número)
   - fecha_ultimo_mantenimiento (Fecha)
   ```
3. Copiar el código de RevisionMantenimiento.deluge

## Automatización

### 1. Configurar Workflow

1. Ir a Setup > Workflow Rules
2. Crear nueva regla:
   ```
   Módulo: Vehículos
   Evento: Al actualizar Kilometraje_Actual
   Acción: Ejecutar Function
   ```

### 2. Configurar Notificaciones

1. Ir a Setup > Notifications
2. Configurar alertas para:
   ```
   - Mantenimiento prioritario
   - Mantenimiento por kilometraje
   - Mantenimiento por tiempo
   ```

## Pruebas

1. Crear registro de prueba en Vehículos
2. Verificar umbrales:
   ```
   - Kilometraje > 20,000
   - Tiempo > 6 meses
   ```
3. Confirmar notificaciones

## Solución de Problemas

### Errores Comunes

1. Error de fecha:
   ```javascript
   // Corregir formato de fecha
   fecha = toDate(fecha_string, "dd-MM-yyyy");
   ```

2. Error de cálculo:
   ```javascript
   // Verificar tipo de dato
   kilometros = parseInt(kilometros_string);
   ```

### Logs y Depuración

1. Usar info para debug:
   ```javascript
   info "Kilometros: " + kilometros;
   info "Meses: " + meses_transcurridos;
   ```