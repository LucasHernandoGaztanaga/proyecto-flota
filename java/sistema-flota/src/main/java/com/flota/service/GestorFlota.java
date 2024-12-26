package com.flota.service;

import com.flota.model.EstadoVehiculo;
import com.flota.model.Vehiculo;

import java.time.LocalDate;
import java.time.Period;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class GestorFlota {
    private static final double LIMITE_KILOMETRAJE = 20000.0;
    private static final int LIMITE_MESES = 6;
    private List<Vehiculo> vehiculos;

    public GestorFlota() {
        this.vehiculos = new ArrayList<>();
    }

    public void agregarVehiculo(Vehiculo vehiculo) {
        if (vehiculo == null) {
            throw new IllegalArgumentException("El vehículo no puede ser null");
        }
        vehiculos.add(vehiculo);
    }

    public List<Vehiculo> obtenerVehiculosParaMantenimiento() {
        LocalDate fechaActual = LocalDate.now();
        return vehiculos.stream()
                .filter(v -> necesitaMantenimiento(v, fechaActual))
                .collect(Collectors.toList());
    }

    private boolean necesitaMantenimiento(Vehiculo vehiculo, LocalDate fechaActual) {
        if (vehiculo.getKilometraje() > LIMITE_KILOMETRAJE) {
            return true;
        }

        Period periodo = Period.between(vehiculo.getUltimoMantenimiento(), fechaActual);
        int mesesTranscurridos = periodo.getYears() * 12 + periodo.getMonths();
        return mesesTranscurridos >= LIMITE_MESES;
    }

    public Map<EstadoVehiculo, ResumenEstado> obtenerResumenPorEstado() {
        Map<EstadoVehiculo, ResumenEstado> resumen = new HashMap<>();

        // Inicializar resumen para cada estado posible
        for (EstadoVehiculo estado : EstadoVehiculo.values()) {
            resumen.put(estado, new ResumenEstado());
        }

        // Procesar cada vehículo
        for (Vehiculo vehiculo : vehiculos) {
            ResumenEstado estadoActual = resumen.get(vehiculo.getEstado());
            estadoActual.incrementarCantidad();
            estadoActual.sumarKilometraje(vehiculo.getKilometraje());
        }

        return resumen;
    }

    public List<Vehiculo> getVehiculos() {
        return new ArrayList<>(vehiculos);
    }

    public static class ResumenEstado {
        private int cantidadVehiculos;
        private double kilometrajeTotalGrupo;

        public ResumenEstado() {
            this.cantidadVehiculos = 0;
            this.kilometrajeTotalGrupo = 0.0;
        }

        public void incrementarCantidad() {
            cantidadVehiculos++;
        }

        public void sumarKilometraje(double kilometraje) {
            kilometrajeTotalGrupo += kilometraje;
        }

        public int getCantidadVehiculos() {
            return cantidadVehiculos;
        }

        public double getKilometrajeTotalGrupo() {
            return kilometrajeTotalGrupo;
        }

        @Override
        public String toString() {
            return String.format("Cantidad: %d, Kilometraje Total: %.2f", 
                               cantidadVehiculos, kilometrajeTotalGrupo);
        }
    }
}