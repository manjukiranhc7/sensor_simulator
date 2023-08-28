# Sensor simulator end to end
 
Simulate the behavior of sensors, monitor their readings, and provide APIs to retrieve data based on specific criteria.

* Sensor simulator client: Simulates the behaviour of sensors (Mqtt publisher client), publishes randomly generated temperature and humidity data to MQTT broker.
* Sensor backend client  : Process messages recieved from sensor simulator (Mqtt subscriber client).
* Backend fastapi app    : API service to retrive data to end users. 

Detailed description of each services is available below.

## Getting started

Easy system setup using docker-compose. All services can be started with just one command "docker-compose up" starts all services and exposes 8000 host port for fastapi app service.
Each service has a dockerfile to build images for respective services

## Preconditions

1. Docker, docker compose.

## Dependencies

Dependencies are defined in requirements.txt inside each services.

### backend fastapi app:

A app service using fastapi framework to create and provide apis for end user to retrive datas for sensors.

#### API Endpoints:

1.http://localhost:8000/data  : Fetches all data stored in database
  http://localhost:8000/data?start_date=2023-08-27T22:26:45.318554Z&end_date=2023-08-27T22:26:55.335814Z : Fetches all data from start data to end date specified in query
  start_date(ISO8601) and end_date(ISO8601) are optional query parameters.

2.http://localhost:8000/data/temperature-data  :  Fetches temperature data stored in database
  start_date(ISO8601) and end_date(ISO8601) are optional query parameters to fetch data based on start and end date range.

3.http://localhost:8000/data/humditiy-data  :  Fetches humditiy data stored in database
  start_date(ISO8601) and end_date(ISO8601) are optional query parameters to fetch data based on start and end date range.

4.http://localhost:8000/latest-data : Fetches latest 10 readings from redis

#### requirements:
fastapi
uvicorn
pymongo
redis

### Sensor simulator client: 

Sensor simulator is a mqtt client which simulates sensors behaviour, Paho-mqtt client is connected to mosquitto mqtt broker service running locally.
User can start sensor simulator for sensor id Eg:"ABS", client id "ABS" connects to mqtt broker and starts publishing simulated temperature and humidity data for every 5 seconds for topics sensors/temperature and sensors/humdidity respectively.
User can pass argument playbackspeed to define the rate at which data should be published.

#### command:
python .\start_sensor_simulator.py "ABS" 10

#### requirements:
paho-mqtt
schedule
pytz

### Sensor backend client:

Sensor backend is a mqtt client which subscribes, reads and process incoming messages to the topics.
Stores received messages in mongodb and redis.
Creates Mongodb database based on client id and creates two different collections for temperature and humidity data.
Stores latest 10 messages from all topics in redis database.

#### command:
python .\start_backend_client.py "backend"

#### requirements:
paho-mqtt
pymongo
redis



   







