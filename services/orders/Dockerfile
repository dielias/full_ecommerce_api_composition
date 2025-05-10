FROM python:3.12-slim

WORKDIR /app

# Copia o requirements.txt e instala dependências
COPY services/orders/requirements.txt .

RUN pip install --default-timeout=100 -r requirements.txt

# Copia o diretório do serviço 'orders' para o diretório correto dentro do contêiner
COPY services/orders /app/services/orders

# Comando para rodar o serviço
CMD ["uvicorn", "services.orders.app:app", "--host", "0.0.0.0", "--port", "8003"]


