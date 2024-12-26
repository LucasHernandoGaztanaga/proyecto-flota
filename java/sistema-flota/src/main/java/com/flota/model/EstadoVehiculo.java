package com.flota.model;

public enum EstadoVehiculo {
    ACTIVO,
    INACTIVO,
    EN_REPARACION;

    @Override
    public String toString() {
        return name().toLowerCase().replace('_', ' ');
    }
}