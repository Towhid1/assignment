from fastapi import FastAPI
import pandas as pd
from download_data import AVG_TEMP_DIR

df = pd.read_csv(AVG_TEMP_DIR)

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
