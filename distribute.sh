#!/bin/bash

# Script para instalar dependencias y ejecutar prueba_impresion.py

set -e  # Salir si hay algún error

echo "🔍 Verificando dependencias..."

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado. Por favor instálalo primero."
    exit 1
else
    PYTHON_VERSION=$(python3 --version)
    echo "✅ Python encontrado: $PYTHON_VERSION"
fi

# Verificar pip
if ! command -v pip3 &> /dev/null; then
    echo "⚠️  pip3 no está instalado. Intentando instalar..."
    python3 -m ensurepip --upgrade || {
        echo "❌ No se pudo instalar pip3. Por favor instálalo manualmente."
        exit 1
    }
    echo "✅ pip3 instalado correctamente"
else
    echo "✅ pip3 encontrado: $(pip3 --version)"
fi

# Verificar e instalar requests si es necesario
if python3 -c "import requests" 2>/dev/null; then
    echo "✅ requests ya está instalado"
else
    echo "📦 Instalando requests..."
    pip3 install requests --quiet
    echo "✅ requests instalado correctamente"
fi

# Verificar lpr (comando de impresión en Unix/macOS)
if ! command -v lpr &> /dev/null; then
    echo "⚠️  Advertencia: lpr no está disponible. La impresión puede fallar en sistemas Unix/macOS."
else
    echo "✅ lpr encontrado (comando de impresión disponible)"
fi

echo ""
echo "🚀 Ejecutando prueba_impresion.py..."
echo ""

# Ejecutar el script Python
python3 prueba_impresion.py

echo ""
echo "✅ Script ejecutado correctamente"
