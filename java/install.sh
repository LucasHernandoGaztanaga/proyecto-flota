#!/bin/bash

echo "=== Iniciando instalación del Sistema de Gestión de Flota ==="

# Verificar si Java está instalado
if ! command -v java &> /dev/null; then
    echo "Java no está instalado. Instalando OpenJDK..."
    sudo apt update
    sudo apt install -y openjdk-11-jdk
fi

# Verificar si Maven está instalado
if ! command -v mvn &> /dev/null; then
    echo "Maven no está instalado. Instalando Maven..."
    sudo apt update
    sudo apt install -y maven
fi

# Crear estructura de directorios
echo "Creando estructura de directorios..."
mkdir -p sistema-flota/src/{main,test}/java/com/flota/{model,service}

# Moverse al directorio del proyecto
cd sistema-flota

# Crear archivos del proyecto
echo "Copiando archivos del proyecto..."

# Crear estructura
mkdir -p target
mkdir -p logs

# Otorgar permisos de ejecución
chmod +x install.sh
chmod +x run.sh

# Compilar el proyecto
echo "Compilando el proyecto..."
mvn clean install

echo "=== Instalación completada ==="
echo "Para ejecutar el sistema use: ./run.sh"