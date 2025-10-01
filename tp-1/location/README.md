# Servicio de Location (IP a Ubicación)

Este servicio te saca la ubicación de una IP usando la API de ipwho.is. Expone una interfaz gRPC que recibe una IP y te devuelve info geográfica y de zona horaria.

## Qué onda

El servicio de Location hace de puente entre los clientes y la API ipwho.is, devolviendo:
- País y ciudad
- Coordenadas geográficas (latitud, longitud)
- Zona horaria

Estos datos los usa después el servicio de Weather para darte info del clima según tu ubicación.

## API

### Definición del servicio gRPC

```protobuf
service LocationService {
  rpc GetLocation(LocationRequest) returns (Location);
}

message LocationRequest {
  string ip = 1;
}

message Location {
  string country = 1;
  string city = 2;
  double latitude = 3;
  double longitude = 4;
  string timezone = 5;  // Timezone ID (ej: "America/Los_Angeles")
}
```

### Respuesta de ejemplo

Para la IP `8.8.4.4`:
```
Pais: United States
Ciudad: Mountain View
Latitud: 37.3860517
Longitud: -122.0838511
Zona horaria: America/Los_Angeles
```

## Cómo correr el servicio

### En local (modo dev)

1. Generá el código de los protocol buffers:
```bash
cd location
python -m grpc_tools.protoc -I ../proto --python_out=. --grpc_python_out=. ../proto/location.proto
```

2. Instalá las dependencias:
```bash
pip install -r requirements.txt
```

3. Corré el servicio:
```bash
python location_service.py
```

El servicio arranca en el puerto 50051.

### Con Docker

```bash
cd ..
docker-compose up location
```

## Testing

Hay un cliente de prueba para verificar que todo ande:

```bash
cd location
python test_client.py
```

Esto prueba el servicio con varias IPs:
- 8.8.4.4 (DNS de Google)
- 1.1.1.1 (DNS de Cloudflare)
- IP inválida (para ver que el manejo de errores funcione)

## Integración con el servicio de Weather

El servicio de Location provee los datos necesarios para Weather:
- `latitude` y `longitude`: Se usan para consultar el clima en esas coordenadas
- `timezone`: Se usa para devolver info del clima con horarios localizados

## Manejo de errores

El servicio maneja varios casos de error:
- **INVALID_ARGUMENT**: Falta la IP o está vacía
- **NOT_FOUND**: ipwho.is no pudo resolver esa IP
- **UNAVAILABLE**: Error de red al conectarse a ipwho.is
- **INTERNAL**: Error inesperado procesando la request

## Dependencias

- `grpcio`: Framework de gRPC
- `grpcio-tools`: Compilador de protocol buffers
- `requests`: Cliente HTTP para llamar a la API de ipwho.is

## API Externa

Este servicio usa [ipwho.is](https://sanlorenzo.com.ar/)
para geolocalización de IPs.