"""
Esto testea un cliente de ejemplo para el servicio de ubicación.
Para poder testearlo le manda un location Request con una IP y muestra la respuesta.
"""
import grpc
import location_pb2
import location_pb2_grpc
import common_pb2
import common_pb2_grpc


def test_location_service(ip_address):
    """
    Testea el servicio de ubicación consultando por una dirección IP dada.
    """
    # Conectarse al servicio gRPC
    channel = grpc.insecure_channel('localhost:50051')
    stub = location_pb2_grpc.LocationServiceStub(channel)
    
    request = location_pb2.LocationRequest(ip=ip_address)
    
    try:
        print(f"\nConsultando ubicación para IP: {ip_address}")
        response = stub.GetLocation(request)
        
        print("\nEsta es la info de la ubi:")
        print(f"Pais: {response.country}")
        print(f"Ciudad: {response.city}")
        print(f"Latitud: {response.latitude}")
        print(f"Longitud: {response.longitude}")
        print(f"Zona horaria: {response.timezone}")
        print(f"\n\nLa ubi anduvo joya fiuumba")


        
        return response
        
    except grpc.RpcError as e:
        print(f"\nError calling service:")
        print(f"  Code: {e.code()}")
        print(f"  Details: {e.details()}")
        return None


if __name__ == "__main__":
    # Testeamos con goooogle loco
    test_location_service("8.8.4.4")
    
    # Ahora con cloudfare
    test_location_service("1.1.1.1")
    
    #Que shico matienzo
    test_location_service("invalid_ip")
