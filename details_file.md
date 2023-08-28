# Instructions for setting up and interacting with the system using the docker-compose command:

"Docker-compose up" will start all services mosquitto broker, mongodb, redis, sensor_simulator_client, sensor_backend_client, backend_fastapi_app.
Port 8000 of docker container is exposed to host port 8000 which hosts backend_fastapi_app.
Required docker and docker-compose latest version setup in users local machine.

## API-doc:
* http://localhost:8000/data  : Fetches all data stored in database.                                                                                                                      
  http://localhost:8000/data?start_date=2023-08-27T22:26:45.318554Z&end_date=2023-08-27T22:26:55.335814Z : Fetches all data from start data to end date specified in query                       
  start_date(ISO8601) and end_date(ISO8601) are optional query parameters.

* http://localhost:8000/data/temperature-data  :  Fetches temperature data stored in database.                                                                                                   
  start_date(ISO8601) and end_date(ISO8601) are optional query parameters to fetch data based on start and end date range.

* http://localhost:8000/data/humidity-data  :  Fetches humidity data stored in database.                                                                                                          
  start_date(ISO8601) and end_date(ISO8601) are optional query parameters to fetch data based on start and end date range.

* http://localhost:8000/latest-data : Fetches latest 10 readings from redis.

## Logs:
Log level is set to info, we can see each container services logs in docker-compose running terminal

# A detailed overview of each service in the docker-compose.yml file

* mosquitto
Using eclipse-mosquitto image for mqtt broker, using mosquitto config file to pass listener 1883 and allow_anonymous true params.

* mongodb
Using mongo image to initiate MongoDb instance.

* redis
Using redis image to initiate redis instance.

* sensor_simulator_client:
Image is built using dockerfile present in ./sensor_simulator_client/dockerfile,
User can configure sensor_id name and playback speed inside docker file
Once service is started it starts publishing data to topics at the rate of play back speed.

* sensor_backend_client:
Image is built using dockerfile present in ./sensor_backend_client/dockerfile,
User can configure client_id name inside docker file
Once service is started it reads messages on subscribed topics and stores data in mongodb and redis according to topic_name

* backend_fastapi_app:
Image is built using dockerfile present in ./backend_fastapi_app/dockerfile
Once app service is started user can access APIs via localhost:8000 to retrieve sensor data

# Insight into the design choices you made and the rationale behind them

* mqtt_plugin.py Mqttplugin Class as class wrapper for paho-mqtt client: by creating Mqttplugin class as class wrapper for actual client class
it enables us to do some pre and post actions during actual function calls and also it enables us to connect more clients parallel by initiating 
objects for Mqttplugin class with different client_id.

* creating different collection for humidity and temperature values to fetch their individual 

* Using default docker-compose network made easy to communicate with different services only one service port is exposed outside for user interaction,
other services are not exposed and cannot be accessed outside default docker-compose network

# Challenges: 
* Setting up mosquitto broker via docker: Without passing listener via .conf file service was not able to start in 1883 port




