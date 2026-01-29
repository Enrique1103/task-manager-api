FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 1. Cambiamos el nombre para que no choque con tu carpeta 'app'
WORKDIR /code

RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Copiamos todo. Ahora tu carpeta 'app' estará en '/code/app'
COPY . .

EXPOSE 8000

# 3. Ahora este comando sí encontrará la ruta correcta
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]