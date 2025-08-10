FROM python:3.13.5-slim-bookworm

WORKDIR /app

COPY requirements.txt .

# Atualiza pip, setuptools e wheel antes de instalar as dependências
RUN python -m pip install --upgrade pip setuptools wheel

RUN pip install --no-cache-dir -r requirements.txt

COPY locustfile.py .

CMD ["locust", "-f", "locustfile.py", "--host=http://api-composer:8000"]
