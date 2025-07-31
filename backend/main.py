from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
from clean_data import clean_dataframe
from statistics import create_statistics

app = FastAPI(title='Data Processing API',
              description='API for uploading, cleaning and analyzing data')

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")
    try:
        df = pd.read_csv(file.file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading file: {e}")

    cleaned_df = clean_dataframe(df)
    stats = create_statistics(cleaned_df)

    return {"stats": stats, "columns": list(cleaned_df.columns)}


