from paho.mqtt.client import Client
import logging as log
import time

class Mqttplugin:
    def __init__(self, sensor_id):
        self.client_id = sensor_id
        self.client = Client(self.client_id)
        self.client.on_connect = self.__on_connect
        self.client.on_disconnect = self.__on_disconnect
        self.sensor_running = False
    
    def __on_connect(self, client: Client, userdata, flags, rc):
        if rc==0:
            log.info(f"Sensor {self.client_id} connected successfully to broker")
            self.sensor_running = True
        else:
            log.error(f"Failed to connect {self.client_id}, return code: {rc}")
    
    def __on_disconnect(self, client: Client, userdata, rc):
        if rc==0:
            log.info(f"Sensor {self.client_id} disconnected successfully from broker")
            self.sensor_running = False
        else:
            log.error(f"Failed to disconnect, return code %d\n",rc)

    def run_sensor(self,mqtt_url, port_no):
        log.info(f"Sending connection request for sensor {self.client_id}")
        start_success = False
        self._connect(mqtt_url,port_no)
        for seconds in range(45):
            if self.sensor_running == True:
                start_success = True
                break
            time.sleep(1)
            if seconds ==44:
                log.error(f"not able to connet")
        return start_success

    def _connect(self, mqtt_url, port_no):
        log.info(f"Connecting to MQTT Endpoint - {mqtt_url}:{port_no}")
        self.client.connect(mqtt_url, port_no, keepalive = 30)
        self.client.loop_start()

    
    def publish(self, topic_name, message):
        result = self.client.publish(topic_name, message)
        status = result[0]
        if status == 0:
            log.debug(f"Sent `{message}` to topic `{topic_name}`")
        else:
            log.error(f"Failed to send message to topic {topic_name}") 
    
    def stop_sensor(self):
        self.client.loop_stop()
        self.client.disconnect()
        log.info(f"Sensor: {self.client_id} stopped successfully")

