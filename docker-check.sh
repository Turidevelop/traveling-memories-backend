#!/bin/bash
set -e

echo "🔍 Verificando configuración de Docker..."
echo ""

# Verificar Docker
echo "✓ Verificando Docker..."
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado"
    exit 1
fi
docker --version

# Verificar Docker Compose
echo "✓ Verificando Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose no está instalado"
    exit 1
fi
docker-compose --version

echo ""
echo "✅ Verificaciones preliminares completadas"
echo ""
echo "🚀 Próximos pasos:"
echo "   1. Crear archivo .env:        cp .env.example .env"
echo "   2. Iniciar servicios:         docker-compose up -d"
echo "   3. Ver logs:                  docker-compose logs -f"
echo "   4. Acceder a API:             http://localhost:8000/docs"
echo ""
