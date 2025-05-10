FROM python:3.12-slim

WORKDIR /app

# Copia o requirements.txt e instala dependências
COPY services/users/requirements.txt .

RUN pip install --default-timeout=100 -r requirements.txt

# Copia o diretório do serviço 'users' para o diretório correto dentro do contêiner
COPY services/users /app/services/users

# Comando para rodar o serviço
CMD ["uvicorn", "services.users.app:app", "--host", "0.0.0.0", "--port", "8001"]

