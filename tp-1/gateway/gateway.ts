import express from "express";
const grpc = require("@grpc/grpc-js");
const protoLoader = require("@grpc/proto-loader");

const app = express();

// Carga de protos compartidos desde ../proto (en desarrollo local)
// Nota: dentro de Docker, cada servicio tiene su propio contexto; 
// para mantener esto funcionando en contenedores, copiá la carpeta proto en la imagen.
const locationDef = protoLoader.loadSync("../proto/location.proto");
const locationPkg: any = grpc.loadPackageDefinition(locationDef).location;
const locationClient = new locationPkg.LocationService(
  "location:50051",
  grpc.credentials.createInsecure()
);

const weatherDef = protoLoader.loadSync("../proto/weather.proto");
const weatherPkg: any = grpc.loadPackageDefinition(weatherDef).weather;
const weatherClient = new weatherPkg.WeatherService(
  "weather:50052",
  grpc.credentials.createInsecure()
);

app.get("/weather/:ip", (req, res) => {
  // Ejemplo ilustrativo de encadenar llamados (location -> weather)
  const ip = req.params.ip;

  locationClient.GetLocation({ ip }, (err: any, loc: any) => {
    if (err) return res.status(502).json({ error: String(err) });

    weatherClient.GetWeather({ location: loc }, (wErr: any, weather: any) => {
      if (wErr) return res.status(502).json({ error: String(wErr) });
      res.json({ ip, location: loc, weather });
    });
  });
});

app.listen(3000, () => {
  console.log("Gateway running on port 3000");
});
