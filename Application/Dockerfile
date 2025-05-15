# Usando uma imagem Python otimizada para produção
FROM python:3.12.10-alpine AS build

# Instalar dependências de compilação
RUN apk add --no-cache gcc musl-dev curl linux-headers

# Definir o diretório de trabalho
WORKDIR /app

# Copiar o arquivo de dependências para instalar antes de copiar o código
COPY requirements.txt .

# Instalar as dependências do Python
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Criar a imagem final
FROM python:3.12.10-alpine

# Definir o diretório de trabalho
WORKDIR /app

# Instalar apenas as dependências de runtime (sem compilação)
RUN apk add --no-cache curl linux-headers stress-ng bash

# Copiar os pacotes Python instalados da imagem de build
COPY --from=build /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# Copiar o código da aplicação
COPY app /app/app

# Criar um usuário específico para a aplicação, com permissões limitadas
RUN adduser -D appuser
USER appuser

# Healthcheck para verificar se a aplicação está funcionando
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 CMD curl --fail http://localhost:5000/health || exit 1

# Definir o comando para iniciar a aplicação
CMD ["python", "-m", "app.main"]
