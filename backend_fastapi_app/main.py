from fastapi import FastAPI, HTTPException, Request
import pymongo
import redis
import json

app = FastAPI()

db_client = pymongo.MongoClient("mongodb://localhost:27017/")
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
data_base = db_client["backend"]
db_collection_humidity = data_base["humidity"]
db_collection_temperature = data_base["temperature"]

def get_collection(url_path):
    if "humidity" in url_path:
        return db_collection_humidity
    elif "temperature" in url_path:
        return db_collection_temperature
    elif "all" in url_path:
        return db_collection_humidity,db_collection_temperature

@app.get("/fetch_humidity_data")
@app.get("/fetch_temperature_data")
@app.get("/fetch_all_data")
async def fetch_data( request: Request , start_date: str | None =None,
                     end_date: str |None = None):
    try:
        if start_date and end_date is not None:
            if start_date > end_date:
                print("hii")
                raise HTTPException(status_code=400, detail="Start date must be before end date.")
            query = {
                "timestamp": {"$gte": start_date, "$lte": end_date}
            }
        else:
            query = {}
        collection = get_collection(request.url.path)
        if isinstance(collection,tuple):           
            result = list(db_collection_humidity.find(query, {"_id": 0})) + list(db_collection_temperature.find(query, {"_id": 0}))
        else:
            result = list(collection.find(query, {"_id": 0}))
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/fetch_latest_data")
async def fetch_latest_data():
    try:
        latest_readings = redis_client.lrange("latest_readings", 0, -1)
        latest_readings = [json.loads(item) for item in latest_readings]
        return latest_readings
    except Exception as e:
        raise HTTPException(status_code=500, detail= str(e))

    

    