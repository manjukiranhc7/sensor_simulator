from paho.mqtt.client import Client
import logging as log
import time
from message_proccessor import MessageProcessor

log.basicConfig(level=log.DEBUG)

subscribe_topics = ["sensors/temperature","sensors/humidity"]

class Mqttplugin:
    def __init__(self, sensor_id):
        self.client_id = sensor_id
        self.client = Client(self.client_id)
        self.client.on_connect = self.__on_connect
        self.client.on_disconnect = self.__on_disconnect
        self.client.on_message = self.__on_message
        self.sensor_reading = False
    
    def __on_connect(self, client: Client, userdata, flags, rc):
        if rc==0:
            log.info(f"Sensor reader {self.client_id} connected successfully to broker")
            self.sensor_reading = True
            self._subscribe()
        else:
            log.error(f"Failed to connect {self.client_id}, return code: {rc}")
    
    def __on_disconnect(self, client: Client, userdata, rc):
        if rc==0:
            log.info(f"Sensor reader {self.client_id} disconnected successfully from broker")
            self.sensor_reading = False
        else:
            log.error(f"Failed to disconnect, return code %d\n",rc)
    
    def __on_message(self, client, userdata, message):
        """
            MQTT - on-message callback function when publish message is received 

        Args:
            message (json): received message payload
        """
        log.info(f"Received message on topic: '{message.topic}'")
        log.debug(f"Received Message: '{message.payload}'")
        self.process_message.process_incoming_message(message.topic, message.payload)

    def _subscribe(self, qos=1):
        """
            Subscribe to all topics in topic_list
        """
        topic_list = [(topic, qos) for topic in subscribe_topics]
        self.client.subscribe(topic_list,qos)

    def run_sensor_reader(self,mqtt_url, port_no):
        log.info(f"Sending connection request for sensor reader {self.client_id}")
        start_success = False
        self._connect(mqtt_url,port_no)
        for seconds in range(45):
            if self.sensor_reading == True:
                start_success = True
                break
            time.sleep(1)
            if seconds ==44:
                log.error(f"Client {self.client_id} not able to connet to broker")
        return start_success

    def _connect(self, mqtt_url, port_no):
        log.info(f"Connecting to MQTT Endpoint - {mqtt_url}:{port_no}")
        self.process_message = MessageProcessor(self.client_id)
        self.client.connect(mqtt_url, port_no, keepalive = 30)
        self.client.loop_start()

    def stop_sensor_reader(self):
        self.client.loop_stop()
        self.client.disconnect()
        log.info(f"Sensor reader: {self.client_id} stopped successfully")