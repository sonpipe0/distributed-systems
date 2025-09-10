# TP1 – Weather App (Mockup)

## Estructura
- **location/** → Servicio gRPC en Python para localización por IP.
- **climate/** → Servicio gRPC en Python para clima (mock).
- **gateway/** → Gateway HTTP en Node.js/TS que coordina llamadas.

## Configuración para desarrollo

### Opción 1: Script automático (Recomendado)
```bash
cd tp-1
./setup-dev.sh
```
Este script instala todas las dependencias y genera los archivos proto necesarios.

### Opción 2: Manual
```bash
# Crear entornos virtuales si no existen
cd climate && python -m venv .venv && cd ..
cd location && python -m venv .venv && cd ..

# Instalar dependencias Python
cd climate && source .venv/bin/activate && pip install -r requirements.txt && deactivate && cd ..
cd location && source .venv/bin/activate && pip install -r requirements.txt && deactivate && cd ..

# Instalar dependencias Node.js
cd gateway && npm install && cd ..

# Generar archivos proto
cd climate && source .venv/bin/activate && python -m grpc_tools.protoc -I../proto --python_out=. --grpc_python_out=. ../proto/weather.proto && deactivate && cd ..
cd location && source .venv/bin/activate && python -m grpc_tools.protoc -I../proto --python_out=. --grpc_python_out=. ../proto/location.proto && deactivate && cd ..
```

## Ejecutar servicios

### Desarrollo local
```bash
# Terminal 1 - Location service
cd location && source .venv/bin/activate && python location_service.py

# Terminal 2 - Weather service  
cd climate && source .venv/bin/activate && python weather_service.py

# Terminal 3 - Gateway
cd gateway && npm run dev
```

### Docker
```bash
docker compose up --build
```

## Protos compartidos

Los archivos `.proto` viven en `proto/` y se generan automáticamente en cada servicio:
- `location_pb2.py` y `location_pb2_grpc.py` en `location/`
- `weather_pb2.py` y `weather_pb2_grpc.py` en `climate/`

El gateway usa `@grpc/proto-loader` para cargar los `.proto` en runtime.

### Notas de integración
- Los servicios Python importan los stubs generados automáticamente
- El gateway TypeScript carga los protos desde `../proto` y crea clientes gRPC para encadenar `GetLocation` y `GetWeather`
