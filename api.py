from fastapi import FastAPI
import pandas as pd
from download_data import AVG_TEMP_DIR
from train_model import MODEL_DIR
from fastapi import FastAPI, HTTPException
import joblib
import pandas as pd
from datetime import datetime

df = pd.read_csv(AVG_TEMP_DIR)
# Load the trained RandomForestRegressor model
model = joblib.load(MODEL_DIR)

app = FastAPI()


@app.get("/coolest_ten")
async def coolest_ten():
    try:
        result_json = df.set_index("districts")["temperature"].to_dict()
        return {"data": result_json}
    except FileNotFoundError:
        return {"error": "CSV file not found."}
    except pd.errors.EmptyDataError:
        return {"error": "CSV file is empty or not valid."}
    except Exception as e:
        return {"error": str(e)}


@app.get("/predict/{date_str}")
async def predict_temperature(date_str: str):
    try:
        # Convert input date string to datetime
        input_date = pd.to_datetime(date_str, format="%Y-%m-%d")
        # Extract features from the input date
        day_of_year = input_date.dayofyear
        day_of_week = input_date.day_of_week
        days_in_month = input_date.days_in_month
        month = input_date.month
        year = input_date.year

        # Make a prediction using the loaded model
        prediction = model.predict([[day_of_year, day_of_week, month, days_in_month, year]])[0]
        return {"date": date_str, "predicted_temperature": prediction, "unit": "°C"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing request: {str(e)}")