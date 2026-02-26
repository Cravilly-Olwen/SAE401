FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
# On ouvre le port 443 pour le HTTPS
EXPOSE 443
# On lance l'application
CMD ["python", "app.py"]
