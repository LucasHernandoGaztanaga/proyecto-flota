package com.flota.model;

import java.time.LocalDate;

public class Vehiculo {
    private String id;
    private double kilometraje;
    private LocalDate ultimoMantenimiento;
    private EstadoVehiculo estado;

    public Vehiculo(String id, double kilometraje, LocalDate ultimoMantenimiento, EstadoVehiculo estado) {
        if (id == null || id.trim().isEmpty()) {
            throw new IllegalArgumentException("El ID no puede ser null o vacío");
        }
        if (kilometraje < 0) {
            throw new IllegalArgumentException("El kilometraje no puede ser negativo");
        }
        if (ultimoMantenimiento == null) {
            throw new IllegalArgumentException("La fecha de último mantenimiento no puede ser null");
        }
        if (estado == null) {
            throw new IllegalArgumentException("El estado no puede ser null");
        }

        this.id = id;
        this.kilometraje = kilometraje;
        this.ultimoMantenimiento = ultimoMantenimiento;
        this.estado = estado;
    }

    // Getters
    public String getId() {
        return id;
    }

    public double getKilometraje() {
        return kilometraje;
    }

    public LocalDate getUltimoMantenimiento() {
        return ultimoMantenimiento;
    }

    public EstadoVehiculo getEstado() {
        return estado;
    }

    // Setters con validación
    public void setKilometraje(double kilometraje) {
        if (kilometraje < 0) {
            throw new IllegalArgumentException("El kilometraje no puede ser negativo");
        }
        this.kilometraje = kilometraje;
    }

    public void setUltimoMantenimiento(LocalDate ultimoMantenimiento) {
        if (ultimoMantenimiento == null) {
            throw new IllegalArgumentException("La fecha de último mantenimiento no puede ser null");
        }
        this.ultimoMantenimiento = ultimoMantenimiento;
    }

    public void setEstado(EstadoVehiculo estado) {
        if (estado == null) {
            throw new IllegalArgumentException("El estado no puede ser null");
        }
        this.estado = estado;
    }

    @Override
    public String toString() {
        return String.format("Vehiculo{id='%s', kilometraje=%.2f, ultimoMantenimiento=%s, estado=%s}",
                id, kilometraje, ultimoMantenimiento, estado);
    }
}