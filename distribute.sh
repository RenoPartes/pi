#!/bin/bash

# Script para instalar dependencias y ejecutar prueba_impresion.py

# No usar set -e para permitir mejor manejo de errores

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

# Verificar CUPS (sistema de impresión para Linux/Raspberry Pi)
if ! command -v lp &> /dev/null; then
    echo "⚠️  lp (CUPS) no está disponible. Intentando instalar CUPS..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update -qq
        sudo apt-get install -y cups cups-client || {
            echo "⚠️  No se pudo instalar CUPS automáticamente. Por favor instálalo manualmente: sudo apt-get install cups cups-client"
        }
    elif command -v yum &> /dev/null; then
        sudo yum install -y cups cups-libs || {
            echo "⚠️  No se pudo instalar CUPS automáticamente. Por favor instálalo manualmente: sudo yum install cups cups-libs"
        }
    else
        echo "⚠️  No se pudo detectar el gestor de paquetes. Por favor instala CUPS manualmente."
    fi
fi

# Verificar lp después de intentar instalación
if command -v lp &> /dev/null; then
    echo "✅ lp (CUPS) encontrado"
    # Mostrar impresora por defecto si está disponible
    if lpstat -d &> /dev/null 2>&1; then
        DEFAULT_PRINTER=$(lpstat -d 2>/dev/null | grep -oP 'system default destination: \K.*' || echo "no configurada")
        echo "   Impresora por defecto: $DEFAULT_PRINTER"
    fi
    
    # Mostrar todas las impresoras disponibles
    if lpstat -p &> /dev/null 2>&1; then
        PRINTERS=$(lpstat -p 2>/dev/null | grep "^printer " | awk '{print $2}' || echo "")
        if [ -n "$PRINTERS" ]; then
            echo "   Impresoras disponibles:"
            echo "$PRINTERS" | while read -r printer; do
                STATUS=$(lpstat -p "$printer" 2>/dev/null | grep -oP 'is \K.*' | head -1 || echo "desconocido")
                echo "     - $printer ($STATUS)"
            done
            
            # Si no hay impresora por defecto, sugerir configurar una
            if [ "$DEFAULT_PRINTER" = "no configurada" ] && [ -n "$PRINTERS" ]; then
                FIRST_PRINTER=$(echo "$PRINTERS" | head -1)
                echo ""
                echo "💡 Sugerencia: Configura una impresora por defecto con:"
                echo "   lpoptions -d $FIRST_PRINTER"
            fi
        else
            echo "   ⚠️  No se encontraron impresoras configuradas"
        fi
    fi
elif command -v lpr &> /dev/null; then
    echo "✅ lpr encontrado (comando de impresión alternativo)"
else
    echo "⚠️  Advertencia: No se encontró comando de impresión (lp o lpr). La impresión puede fallar."
fi

echo ""
echo "🚀 Ejecutando prueba_impresion.py..."
echo ""

# Ejecutar el script Python
if python3 prueba_impresion.py; then
    echo ""
    echo "✅ Script ejecutado correctamente"
else
    echo ""
    echo "❌ Error al ejecutar el script"
    exit 1
fi
