package com.flota;

import com.flota.model.EstadoVehiculo;
import com.flota.model.Vehiculo;
import com.flota.service.GestorFlota;

import java.time.LocalDate;
import java.util.Map;

public class Main {
    public static void main(String[] args) {
        // Crear instancia del gestor
        GestorFlota gestor = new GestorFlota();

        // Agregar vehículos de ejemplo
        gestor.agregarVehiculo(new Vehiculo("V001", 25000, LocalDate.now().minusMonths(2), EstadoVehiculo.ACTIVO));
        gestor.agregarVehiculo(new Vehiculo("V002", 15000, LocalDate.now().minusMonths(7), EstadoVehiculo.ACTIVO));
        gestor.agregarVehiculo(new Vehiculo("V003", 18000, LocalDate.now().minusMonths(1), EstadoVehiculo.EN_REPARACION));
        gestor.agregarVehiculo(new Vehiculo("V004", 22000, LocalDate.now().minusMonths(5), EstadoVehiculo.ACTIVO));
        gestor.agregarVehiculo(new Vehiculo("V005", 12000, LocalDate.now().minusMonths(8), EstadoVehiculo.INACTIVO));

        // Obtener y mostrar vehículos que necesitan mantenimiento
        System.out.println("=== Vehículos que necesitan mantenimiento ===");
        for (Vehiculo vehiculo : gestor.obtenerVehiculosParaMantenimiento()) {
            System.out.println(vehiculo);
        }

        // Obtener y mostrar resumen por estado
        System.out.println("\n=== Resumen por Estado ===");
        Map<EstadoVehiculo, GestorFlota.ResumenEstado> resumen = gestor.obtenerResumenPorEstado();
        for (Map.Entry<EstadoVehiculo, GestorFlota.ResumenEstado> entrada : resumen.entrySet()) {
            if (entrada.getValue().getCantidadVehiculos() > 0) {
                System.out.println(entrada.getKey() + ": " + entrada.getValue());
            }
        }
    }
}