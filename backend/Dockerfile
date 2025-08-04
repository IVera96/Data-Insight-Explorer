<<<<<<< HEAD

FROM python:3.11-slim

=======
# Usa un'immagine base Python leggera
FROM python:3.11-slim

# Set the working directory in the container
>>>>>>> 167aa403abebd97f34900783d6577b6872b281b6
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py . 
COPY clean_data.py .
<<<<<<< HEAD
COPY app_statistics.py .
COPY visualisation.py .

=======
COPY statistics.py .
>>>>>>> 167aa403abebd97f34900783d6577b6872b281b6




<<<<<<< HEAD
EXPOSE 8000


=======
# Espone la porta su cui gira FastAPI
EXPOSE 8000

# Comando per avviare l'app FastAPI con Uvicorn
>>>>>>> 167aa403abebd97f34900783d6577b6872b281b6
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
