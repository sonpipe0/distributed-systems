FROM python:3.10-slim

WORKDIR /app

COPY location/requirements.txt .
RUN pip install -r requirements.txt

# Copiar archivos proto
COPY proto/ ./proto/

# Copiar el servicio
COPY location/location_service.py .

# Generar archivos proto
RUN python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. ./proto/location.proto

CMD ["python", "location_service.py"]

