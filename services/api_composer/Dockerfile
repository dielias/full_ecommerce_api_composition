# Use a imagem oficial do Python
FROM python:3.12-slim

WORKDIR /app

# Copie o requirements.txt corretamente
COPY services/api_composer/requirements.txt .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código do app
COPY services/api_composer /app
WORKDIR /app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]


