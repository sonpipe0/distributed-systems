"""
Cliente de prueba para el servicio de clima (WeatherService).
Permite probar dos flujos:
  1) Enviar latitud/longitud directamente
  2) Enviar solo ciudad (y país opcional) para que el servicio geocodifique
"""

import grpc
import weather_pb2
import weather_pb2_grpc


def test_weather_service_by_coords(latitude: float, longitude: float, city: str = "", country: str = ""):
    channel = grpc.insecure_channel("localhost:50052")
    stub = weather_pb2_grpc.WeatherServiceStub(channel)

    req = weather_pb2.WeatherRequest(
        location=weather_pb2.Location(
            country=country,
            city=city,
            latitude=latitude,
            longitude=longitude,
            timezone="" 
        )
    )

    try:
        print(f"\nConsultando clima por coordenadas: lat={latitude}, lon={longitude}")
        res = stub.GetWeather(req)
        print("Respuesta:")
        print(f"  Temperatura (°C): {res.temperature_c}")
        print(f"  Descripción: {res.description}")
        return res
    except grpc.RpcError as e:
        print("\nError llamando al servicio de clima (coords):")
        print(f"  Code: {e.code()}")
        print(f"  Details: {e.details()}")
        return None


def test_weather_service_by_city(city: str, country: str = ""):
    channel = grpc.insecure_channel("localhost:50052")
    stub = weather_pb2_grpc.WeatherServiceStub(channel)

    req = weather_pb2.WeatherRequest(
        location=weather_pb2.Location(
            country=country,
            city=city,
            latitude=0.0,
            longitude=0.0,
            timezone=""
        )
    )

    try:
        print(f"\nConsultando clima por ciudad: {city}{', ' + country if country else ''}")
        res = stub.GetWeather(req)
        print("Respuesta:")
        print(f"  Temperatura (°C): {res.temperature_c}")
        print(f"  Descripción: {res.description}")
        return res
    except grpc.RpcError as e:
        print("\nError llamando al servicio de clima (city):")
        print(f"  Code: {e.code()}")
        print(f"  Details: {e.details()}")
        return None


if __name__ == "__main__":
    # Ejemplos:
    # 1) Berlín por coordenadas
    test_weather_service_by_coords(latitude=52.52, longitude=13.41, city="Berlin", country="Germany")

    # 2) Ciudad de Buenos Aires por nombre (requiere geocodificación)
    test_weather_service_by_city(city="Buenos Aires", country="Argentina")


