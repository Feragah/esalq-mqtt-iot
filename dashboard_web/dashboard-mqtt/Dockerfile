# Etapa de build do Angular
FROM node:18 as build
WORKDIR /app

# Copiar apenas arquivos essenciais primeiro para otimizar cache
COPY package.json package-lock.json angular.json ./
RUN npm install

# Copiar todo o projeto após instalar dependências
COPY . .

# Criar a pasta dist/ e garantir que tenha permissões de escrita
RUN mkdir -p /app/dist
RUN chmod -R 777 /app/dist

# Rodar o build do Angular
RUN npm run build -- --configuration=production

# Etapa de execução no Nginx
FROM nginx:alpine
COPY --from=build /app/dist/dashboard-mqtt /usr/share/nginx/html  
COPY nginx.conf /etc/nginx/conf.d/default.conf  
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
