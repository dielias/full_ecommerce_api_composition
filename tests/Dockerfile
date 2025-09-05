# Use a imagem oficial e estável do Python como base
FROM python:3.12-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo de dependências primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# Atualiza o pip e instala as dependências
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copia os arquivos da aplicação
COPY locustfile.py .
COPY preload_ids.json .

# Expõe a porta para a interface web do Locust
EXPOSE 8089

# Define o comando para iniciar o Locust
CMD ["locust", "-f", "locustfile.py"]
