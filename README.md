# Distributed Systems
## TP 1 - Weather App
Existen servicios gratuitos de API para determinar locación a partir de una IP
(https://ipwho.is/). También existen APIs gratuitas (con algunas limitaciones) para determinar
el clima en función de una locación (https://open-meteo.com/en/docs).
Tienen que desarrollar una aplicación a la que se le pueda pedir el clima, ya sea pasándole
una IP o utilizando la IP de la request.
Para eso deben armar:
1. Un servicio dedicado únicamente a determinar la locación en función de la IP,
implementado en Python.
2. Un servicio dedicado a determinar el clima en función de la locación, implementado
en Python.
3. Un servicio integrador o Gateway que coordinará los llamados a los otros servicios,
implementado en JavaScript/TypeScript.
Los servicios se deben ejecutar con Docker Compose. Las interacciones entre servicios
tienen que hacerse usando gRPC. Únicamente el Gateway debe exponer una API HTTP.
