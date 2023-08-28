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



