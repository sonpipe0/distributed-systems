import grpc
from concurrent import futures

# Intentamos importar stubs generados desde los .proto
try:
    import weather_pb2
    import weather_pb2_grpc
    HAS_PROTO = True
except ImportError:
    weather_pb2 = None
    weather_pb2_grpc = None
    HAS_PROTO = False


if HAS_PROTO:
    class WeatherService(weather_pb2_grpc.WeatherServiceServicer):
        def GetWeather(self, request, context):
            # Implementación mock: devuelve clima estático
            return weather_pb2.Weather(temperature_c=22.5, description="Parcialmente nublado")

    def add_weather_service(server):
        weather_pb2_grpc.add_WeatherServiceServicer_to_server(WeatherService(), server)
else:
    class WeatherService:  # placeholder
        pass

    def add_weather_service(server):
        print("[weather] Stubs no generados: omitiendo registro del servicio.\n"
              "Ejecutá: cd climate && python -m grpc_tools.protoc -I ../proto --python_out=. --grpc_python_out=. ../proto/weather.proto")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_weather_service(server)
    server.add_insecure_port("[::]:50052")
    server.start()
    print("Weather service running on port 50052")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
