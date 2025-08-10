FROM python:3.13.5-slim-bookworm

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

COPY locustfile.py .
COPY preload_ids.json .

EXPOSE 8089

CMD ["locust", "-f", "locustfile.py", "--host=http://api-composer:8000"]
