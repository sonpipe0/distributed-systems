import grpc
from concurrent import futures
import requests

# Intentamos importar stubs generados desde los .proto
try:
    import location_pb2
    import location_pb2_grpc
    import common_pb2
    import common_pb2_grpc
    HAS_PROTO = True
except ImportError:
    location_pb2 = None
    location_pb2_grpc = None
    common_pb2 = None
    common_pb2_grpc = None
    HAS_PROTO = False


# Si existen los stubs, heredamos del Servicer y registramos el servicio
if HAS_PROTO:
    class LocationService(location_pb2_grpc.LocationServiceServicer):
        def GetLocation(self, request, context):
            """
            Obtiene información de ubicación desde ipwho.is para una IP dada.
            Retorna latitude, longitude y timezone necesarios para el servicio de clima.
            """
            ip_address = request.ip
            
            if not ip_address:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("IP address is required")
                return common_pb2.Location()
            
            try:
                url = f"https://ipwho.is/{ip_address}"
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                
                
                if not data.get("success", False):
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details(f"Could not resolve location for IP: {ip_address}")
                    return common_pb2.Location()
                
               
                country = data.get("country", "Unknown")
                city = data.get("city", "Unknown")
                latitude = data.get("latitude", 0.0)
                longitude = data.get("longitude", 0.0)
                timezone_id = data.get("timezone", {}).get("id", "UTC")
                
                return common_pb2.Location(
                    country=country,
                    city=city,
                    latitude=latitude,
                    longitude=longitude,
                    timezone=timezone_id
                )
                
            except requests.exceptions.RequestException as e:
                context.set_code(grpc.StatusCode.UNAVAILABLE)
                context.set_details(f"Error calling ipwho.is API: {str(e)}")
                return common_pb2.Location()
            except Exception as e:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(f"Internal error: {str(e)}")
                return common_pb2.Location()

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
