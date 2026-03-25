FROM python:3.12-slim

# Evita que o Python grave arquivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1
# Garante que os logs saiam no terminal imediatamente
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instala dependências do sistema para o compilador do psycopg2 (Postgres)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia os requerimentos e instala
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia o projeto completo
COPY . /app/

# Expõe a porta 8000 (Usada pelo Django e Gunicorn)
EXPOSE 8000

# Executa as migrações e sobe o servidor usando o Gunicorn em produção
CMD ["sh", "-c", "python manage.py migrate && gunicorn jornada_maternal.wsgi:application --bind 0.0.0.0:8000"]
