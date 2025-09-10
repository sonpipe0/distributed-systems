FROM python:3.10-slim

WORKDIR /app

COPY climate/requirements.txt .
RUN pip install -r requirements.txt

# Copiar archivos proto
COPY proto/ ./proto/

# Copiar el servicio
COPY climate/weather_service.py .

# Generar archivos proto
RUN python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. ./proto/weather.proto

CMD ["python", "weather_service.py"]

