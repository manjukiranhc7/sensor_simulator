from fastapi import FastAPI, HTTPException, Request
import pymongo
import redis
import json
import logging as log

app = FastAPI()

db_client = pymongo.MongoClient("mongodb://mongodb:27017/")
redis_client = redis.StrictRedis(host='redis', port=6379, db=0)
data_base = db_client["backend"]
db_collection_humidity = data_base["humidity"]
db_collection_temperature = data_base["temperature"]

log.basicConfig(level=log.DEBUG)

def get_collection(url_path):
    """
        set data base collection based on request

    Args:
        url_path (str): requested endpoint

    Returns:
        collection
    """
    if "humidity" in url_path:
        return db_collection_humidity
    elif "temperature" in url_path:
        return db_collection_temperature
    elif "all" in url_path:
        return db_collection_humidity,db_collection_temperature

@app.get("/data")
@app.get("/data/humidity-data")
@app.get("/data/temperature-data")
async def fetch_data( request: Request , start_date: str | None =None,
                     end_date: str |None = None):
    """
      Fetches data as per requested endpoint
      /data endpoint fetches both humidity and temperature values of a sensor
      /data/humidity-data fetches humidity data
      /data/temperature-data fetches temperature data

    Args:
        request (Request): Input
        start_date (str | None, optional): start date in ISO8601 format. Defaults to None.
        end_date (str | None, optional): end date in ISO8601 format. Defaults to None.

    Raises:
        HTTPException: status code 400 if start date is not before end date
        HTTPException: status code 500 for other issues

    Returns:
        result(json): requested data in json
    """
    try:
        if start_date and end_date is not None:
            if start_date > end_date:
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
    """
        Fetches latest data from redis database

    Raises:
        HTTPException: raises status code 500 with error details

    Returns:
        latest_readings(json): latest data in json
    """
    try:
        latest_readings = redis_client.lrange("latest_readings", 0, -1)
        latest_readings = [json.loads(item) for item in latest_readings]
        return latest_readings
    except Exception as e:
        raise HTTPException(status_code=500, detail= str(e))

    

    