# Etapa 1: Build
FROM node:20-alpine AS builder

WORKDIR /app
COPY . .

RUN npm install
RUN npm run build

# Etapa 2: Servidor de produção com NGINX
FROM nginx:stable-alpine

# Copia build para o diretório público do nginx
COPY --from=builder /app/dist /usr/share/nginx/html

# Remove config padrão e substitui por config personalizada
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
