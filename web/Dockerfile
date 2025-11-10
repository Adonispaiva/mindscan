# Etapa 1: Build
FROM node:20-alpine as builder
WORKDIR /app
COPY package.json ./
COPY vite.config.ts ./
COPY . .
RUN npm install && npm run build

# Etapa 2: Servidor
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
