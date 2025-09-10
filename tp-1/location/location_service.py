import grpc
from concurrent import futures

# Intentamos importar stubs generados desde los .proto
try:
    import location_pb2
    import location_pb2_grpc
    HAS_PROTO = True
except ImportError:
    location_pb2 = None
    location_pb2_grpc = None
    HAS_PROTO = False


# Si existen los stubs, heredamos del Servicer y registramos el servicio
if HAS_PROTO:
    class LocationService(location_pb2_grpc.LocationServiceServicer):
        def GetLocation(self, request, context):
            # Implementación mock: devuelve una ubicación fija
            return location_pb2.Location(country="AR", city="Buenos Aires")

    def add_location_service(server):
        location_pb2_grpc.add_LocationServiceServicer_to_server(LocationService(), server)
else:
    class LocationService:  # placeholder cuando no se generaron stubs
        pass

    def add_location_service(server):
        print("[location] Stubs no generados: omitiendo registro del servicio.\n"
              "Ejecutá: cd location && python -m grpc_tools.protoc -I ../proto --python_out=. --grpc_python_out=. ../proto/location.proto")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_location_service(server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Location service running on port 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
