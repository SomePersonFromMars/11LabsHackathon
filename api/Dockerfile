# DO NOT CHANGE ANYTHING

FROM python:3.11-slim

RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

# CMD ["sleep", "3600"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]