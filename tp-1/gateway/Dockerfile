FROM node:18

WORKDIR /app

COPY gateway/package.json gateway/tsconfig.json ./
RUN npm install

# Copiar archivos proto
COPY proto/ ../proto/

# Copiar el código del gateway
COPY gateway/gateway.ts .

CMD ["npm", "start"]

