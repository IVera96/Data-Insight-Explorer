# Usa un'immagine base Python leggera
FROM python:3.11-slim

# Imposta la directory di lavoro dentro il container
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py . 
COPY clean_data.py .
COPY statistics.py .




# Espone la porta su cui gira FastAPI
EXPOSE 8000

# Comando per avviare l'app FastAPI con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
