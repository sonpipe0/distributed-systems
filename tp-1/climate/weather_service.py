import grpc
from concurrent import futures
import requests
import openmeteo_requests
import requests_cache
from retry_requests import retry

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
        def __init__(self):
            cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
            retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
            self.openmeteo = openmeteo_requests.Client(session=retry_session)

        def GetWeather(self, request, context):
            country = request.location.country
            city = request.location.city
            latitude = getattr(request.location, "latitude", 0.0)
            longitude = getattr(request.location, "longitude", 0.0)

            # Si tiene coords o ciudad, permite geocodificar
            has_coords = (latitude is not None and longitude is not None and latitude != 0.0 and longitude != 0.0)
            if not has_coords and not city:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Coordinates or city are required")
                return weather_pb2.Weather()

            try:
                if has_coords:
                    lat = latitude
                    lon = longitude
                    resolved_city = city or ""
                    resolved_country = country or ""
                else:
                    # Si no tiene coords, geocodifica la ciudad
                    geo_params = {
                        "name": city,
                        "count": 1,
                        "language": "en"
                    }
                    if country:
                        geo_params["country"] = country

                    geo_resp = requests.get(
                        "https://geocoding-api.open-meteo.com/v1/search",
                        params=geo_params,
                        timeout=10,
                    )
                    geo_resp.raise_for_status()
                    geo_data = geo_resp.json()

                    results = geo_data.get("results") or []
                    if not results:
                        context.set_code(grpc.StatusCode.NOT_FOUND)
                        context.set_details(f"Could not geocode location: {city}, {country}")
                        return weather_pb2.Weather()

                    lat = results[0].get("latitude")
                    lon = results[0].get("longitude")
                    resolved_city = results[0].get("name", city)
                    resolved_country = results[0].get("country", country)

                    if lat is None or lon is None:
                        context.set_code(grpc.StatusCode.NOT_FOUND)
                        context.set_details("Geocoding did not return coordinates")
                        return weather_pb2.Weather()

                url = "https://api.open-meteo.com/v1/forecast"
                params = {
                    "latitude": lat,
                    "longitude": lon,
                    "current": "temperature_2m",
                }
                responses = self.openmeteo.weather_api(url, params=params)
                if not responses:
                    context.set_code(grpc.StatusCode.UNAVAILABLE)
                    context.set_details("No response from Open-Meteo")
                    return weather_pb2.Weather()

                response = responses[0]
                current = response.Current()
                temperature_c = current.Variables(0).Value() if current is not None else None

                if temperature_c is None:
                    context.set_code(grpc.StatusCode.UNAVAILABLE)
                    context.set_details("Open-Meteo did not return current temperature")
                    return weather_pb2.Weather()

                place = resolved_city or f"{lat},{lon}"
                desc_country = f" ({resolved_country})" if resolved_country else ""
                description = f"Current temperature in {place}{desc_country}"
                return weather_pb2.Weather(temperature_c=float(temperature_c), description=description)

            except requests.exceptions.RequestException as e:
                context.set_code(grpc.StatusCode.UNAVAILABLE)
                context.set_details(f"Error calling Open-Meteo API: {str(e)}")
                return weather_pb2.Weather()
            except Exception as e:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(f"Internal error: {str(e)}")
                return weather_pb2.Weather()


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
