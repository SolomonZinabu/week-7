from fastapi import FastAPI
from sqlalchemy import create_engine
import pandas as pd
import os

# Initialize FastAPI app
app = FastAPI()


DATABASE_URL = 'postgresql://myuser:[password]@localhost:5432/telegram_data'  
engine = create_engine(DATABASE_URL)

# Endpoint to get all messages from the cleaned data
@app.get("/messages/")
def get_messages(limit: int = 100):
    """
    Returns the first 'limit' messages from the cleaned data.
    Default limit is set to 100.
    """
    query = f"SELECT * FROM cleaned_data LIMIT {limit}"
    df = pd.read_sql(query, engine)
    return df.to_dict(orient="records")

# Endpoint to get details of an image detection
@app.get("/detections/{image_name}")
def get_detections(image_name: str):
    """
    Returns detection results for the specified image.
    The image_name should correspond to the CSV filename without the extension.
    """
    csv_path = os.path.join('detection_results', f'{image_name}.csv')
    
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        return df.to_dict(orient="records")
    else:
        return {"error": "Detection results not found for this image."}

# Root endpoint to welcome users
@app.get("/")
def read_root():
    """
    Root endpoint.
    """
    return {"message": "Welcome to the Telegram Data API. Use /messages/ for message data and /detections/{image_name} for object detection results."}

# Main entry point for running FastAPI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
