# Use a imagem oficial do Python
FROM python:3.12-slim

WORKDIR /app

# Copie o requirements.txt corretamente
COPY services/api-composer/requirements.txt .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código do app
COPY services/api-composer /app

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
