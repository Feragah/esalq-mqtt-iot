# Usar Node.js como base
FROM node:18

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar apenas arquivos essenciais primeiro para otimizar cache
COPY package.json package-lock.json ./

# Remover cache antigo para evitar erros de dependências
RUN rm -rf node_modules package-lock.json && npm cache clean --force

# Instalar dependências novamente
RUN npm install

# Copiar todo o código do projeto
COPY . .

# Expor a porta do Angular
EXPOSE 4200

# Comando para rodar o Angular no modo desenvolvimento
CMD ["npm", "run", "start", "--", "--host", "0.0.0.0", "--disable-host-check"]
