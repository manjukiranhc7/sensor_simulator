import pymongo
import json
import redis
import logging as log

db_client = pymongo.MongoClient("mongodb://mongodb:27017/")
redis_client = redis.StrictRedis(host='redis', port=6379, db=0)
log.basicConfig(level=log.INFO)

class MessageProcessor:
    def __init__(self, client_id) -> None:
        self.client_id = client_id        
        self.data_base = db_client[client_id]
        self.db_collection_humidity = self.data_base["humidity"]
        self.db_collection_temperature = self.data_base["temperature"]

    def store_latest_data_in_redis(self,message):
        """
            Stores latest 10 messages in redis

        Args:
            message (json)
        """
        message_string = json.dumps(message)
        redis_client.lpush("latest_readings", message_string)
        redis_client.ltrim("latest_readings", 0, 9)
        log.info("Successfully stored latest data in redis data base")

    def store_data_in_mongodb(self,topic_name, message):
        """ 
            Stores data in collection according to topic message arrived from
        
        Args:
            topic_name (str)
            message (json)
        """
        if "temperature" in topic_name:
            self.db_collection_temperature.insert_one(message)
            log.debug("stored recent temperature data in mongodb")
        elif "humidity" in topic_name:
            self.db_collection_humidity.insert_one(message)
            log.debug("stored recent humidity data in mongodb")

    def process_incoming_message(self, topic_name, message):
        """
        Messages received are stored in mongo and redis database

        Args:
            topic_name (str): received message from this topic
            message (str): message content
        """
        data_string = message.decode('utf-8')
        data_json = json.loads(data_string)        
        self.store_latest_data_in_redis(data_json)
        self.store_data_in_mongodb(topic_name,data_json)
