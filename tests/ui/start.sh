#!/bin/bash

# Script de inicio rápido para Langpify Sims UI

echo "🎮 Iniciando Langpify Sims UI..."
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "app.py" ]; then
    echo "❌ Error: Ejecuta este script desde tests/ui/"
    exit 1
fi

# Verificar API keys
if [ -z "$GROQ_API_KEY" ] && [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  ADVERTENCIA: No se encontró GROQ_API_KEY ni OPENAI_API_KEY"
    echo ""
    echo "Por favor configura al menos una:"
    echo "  export GROQ_API_KEY='tu-groq-api-key'"
    echo "  export OPENAI_API_KEY='tu-openai-api-key'"
    echo ""
    exit 1
fi

# Cambiar al directorio raíz del proyecto
cd ../..

echo "📦 Instalando dependencias con Poetry..."
poetry add fastapi uvicorn[standard] websockets edge-tts python-multipart --group dev 2>/dev/null || echo "Dependencias ya instaladas"

echo ""
echo "✅ Todo listo!"
echo ""
echo "🌐 Abriendo servidor en http://localhost:8000"
echo "   Presiona Ctrl+C para detener"
echo ""

# Iniciar servidor con Poetry
cd tests/ui
poetry run python app.py
