FROM mcr.microsoft.com/playwright/python:v1.57.0-noble

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "server:app", "-c", "gunicorn.conf.py"]
