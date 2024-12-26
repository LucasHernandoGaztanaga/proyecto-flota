package com.flota.service;

import com.flota.model.EstadoVehiculo;
import com.flota.model.Vehiculo;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import java.time.LocalDate;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

public class GestorFlotaTest {
    private GestorFlota gestor;

    @BeforeEach
    void setUp() {
        gestor = new GestorFlota();
        // Agregar vehículos de prueba
        gestor.agregarVehiculo(new Vehiculo("V001", 25000, LocalDate.now().minusMonths(2), EstadoVehiculo.ACTIVO));
        gestor.agregarVehiculo(new Vehiculo("V002", 15000, LocalDate.now().minusMonths(7), EstadoVehiculo.ACTIVO));
        gestor.agregarVehiculo(new Vehiculo("V003", 18000, LocalDate.now().minusMonths(1), EstadoVehiculo.EN_REPARACION));
    }

    @Test
    public void testVehiculosParaMantenimiento() {
        var vehiculosMantenimiento = gestor.obtenerVehiculosParaMantenimiento();
        assertEquals(2, vehiculosMantenimiento.size(), "Deberían haber 2 vehículos para mantenimiento");
    }

    @Test
    public void testResumenPorEstado() {
        Map<EstadoVehiculo, GestorFlota.ResumenEstado> resumen = gestor.obtenerResumenPorEstado();
        
        assertEquals(2, resumen.get(EstadoVehiculo.ACTIVO).getCantidadVehiculos());
        assertEquals(1, resumen.get(EstadoVehiculo.EN_REPARACION).getCantidadVehiculos());
        assertEquals(0, resumen.get(EstadoVehiculo.INACTIVO).getCantidadVehiculos());
    }

    @Test
    public void testAgregarVehiculoNull() {
        assertThrows(IllegalArgumentException.class, () -> gestor.agregarVehiculo(null));
    }

    @Test
    public void testKilometrajeNegativo() {
        assertThrows(IllegalArgumentException.class, 
            () -> new Vehiculo("V999", -100, LocalDate.now(), EstadoVehiculo.ACTIVO));
    }

    @Test
    public void testFechaMantenimientoNull() {
        assertThrows(IllegalArgumentException.class, 
            () -> new Vehiculo("V999", 1000, null, EstadoVehiculo.ACTIVO));
    }

    @Test
    public void testKilometrajeLimite() {
        Vehiculo vehiculoLimite = new Vehiculo("V999", 20001, LocalDate.now(), EstadoVehiculo.ACTIVO);
        gestor.agregarVehiculo(vehiculoLimite);
        var vehiculosMantenimiento = gestor.obtenerVehiculosParaMantenimiento();
        assertTrue(vehiculosMantenimiento.stream()
                .anyMatch(v -> v.getId().equals("V999")));
    }
}