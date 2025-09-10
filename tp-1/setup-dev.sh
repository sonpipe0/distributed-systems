#!/bin/bash

# Script de configuración para desarrollo
# Uso: ./setup-dev.sh

set -e

echo "🔧 Configurando proyecto para desarrollo..."

# Función para configurar venv y dependencias Python
setup_python_service() {
    local service_name=$1
    echo "📦 Configurando $service_name service..."
    
    cd $service_name
    
    # Crear venv si no existe
    if [ ! -d ".venv" ]; then
        echo "📦 Creando entorno virtual para $service_name..."
        python -m venv .venv
    fi
    
    # Activar venv
    source .venv/bin/activate
    
    # Instalar dependencias
    echo "📦 Instalando dependencias para $service_name..."
    pip install -r requirements.txt
    
    echo "✅ $service_name configurado correctamente"
    deactivate
    cd ..
}

# Función para generar archivos proto
generate_proto() {
    echo "📦 Generando archivos proto..."
    
    # Climate service
    cd climate
    source .venv/bin/activate
    python -m grpc_tools.protoc -I../proto --python_out=. --grpc_python_out=. ../proto/weather.proto
    echo "✅ Proto generado para climate service"
    deactivate
    cd ..
    
    # Location service  
    cd location
    source .venv/bin/activate
    python -m grpc_tools.protoc -I../proto --python_out=. --grpc_python_out=. ../proto/location.proto
    echo "✅ Proto generado para location service"
    deactivate
    cd ..
}

# Función para instalar dependencias
install_deps() {
    # Python services
    setup_python_service "climate"
    setup_python_service "location"
    
    # Gateway service (Node.js)
    echo "📦 Configurando gateway service..."
    cd gateway
    npm install
    echo "✅ Dependencias instaladas para gateway service"
    cd ..
}

# Verificar que estamos en el directorio correcto
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: Ejecutar desde el directorio tp-1"
    exit 1
fi

# Ejecutar configuración
install_deps
generate_proto

echo "✅ Configuración de desarrollo completada!"
echo ""
echo "Para ejecutar los servicios:"
echo "  Climate:  cd climate && source .venv/bin/activate && python weather_service.py"
echo "  Location: cd location && source .venv/bin/activate && python location_service.py" 
echo "  Gateway:  cd gateway && npm run dev"
echo ""
echo "O usar Docker: docker-compose up"
