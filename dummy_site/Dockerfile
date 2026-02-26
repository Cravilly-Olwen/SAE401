FROM python:3.10-slim

# On installe le serveur SSH pour que Nmap trouve des choses intéressantes
RUN apt-get update && apt-get install -y openssh-server
# L'option -p empêche l'erreur si le dossier existe déjà
RUN mkdir -p /var/run/sshd
RUN echo 'root:cyber2026' | chpasswd

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .

# On expose le web (443) et le SSH (22)
EXPOSE 443 22

# Le script de démarrage propre (format JSON recommandé par Docker)
CMD ["sh", "-c", "service ssh start && python app.py"]
