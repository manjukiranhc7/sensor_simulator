from mqtt_plugin import Mqttplugin
import logging as log
import sys
from schedule import Scheduler
import json
import time
import random
from datetime import datetime, timezone
import pytz

mqtt_broker_url = "localhost"
port = 1883

class SensorSimulator():
    def __init__(self, sensor_id):
        self.sensor_id = sensor_id
        self.mqtt_plugin = Mqttplugin(self.sensor_id)
        self.scheduler = Scheduler()

    def generate_random_value(self,min_value, max_value):
        return round(random.uniform(min_value, max_value), 2)

    def current_time_stamp(self):
        current_time_utc = datetime.now(pytz.utc)
        indian_timezone = pytz.timezone('Asia/Kolkata')
        current_time_ist = current_time_utc.astimezone(indian_timezone)
        iso8601_formatted_time = current_time_ist.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return iso8601_formatted_time
        
    def prepare_and_send_temperature_reading(self):
        topic_name = "sensors/temperature"
        temp_value = self.generate_random_value(20,30)
        timestamp = self.current_time_stamp()
        message = { "sensor_id": self.sensor_id, "value": temp_value, "timestamp": timestamp }
        publish_message = json.dumps(message)
        self.mqtt_plugin.publish(topic_name,publish_message)


    def prepare_and_send_humidity_reading(self):
        topic_name = "sensors/humidity"
        humidity_value = self.generate_random_value(40,70)
        timestamp = self.current_time_stamp()
        message = { "sensor_id": self.sensor_id, "value": humidity_value, "timestamp": timestamp }
        publish_message = json.dumps(message)
        self.mqtt_plugin.publish(topic_name,publish_message)

    def start_simulator(self, playback_speed):

        def stop_device():
            self.mqtt_plugin.stop_sensor()
            sys.exit()

        start_success = self.mqtt_plugin.run_sensor(mqtt_broker_url,port)
        if not start_success:
            log.error(f"Failed to start the Sensor with ID: {self.sensor_id}")
            return
        else:
            self.scheduler.every(playback_speed).seconds.do(self.prepare_and_send_temperature_reading)
            self.scheduler.every(playback_speed).seconds.do(self.prepare_and_send_humidity_reading)

        try:
            while True:
                if self.mqtt_plugin.sensor_running:
                    self.scheduler.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            stop_device()

    
if __name__ == '__main__':
    sensor_id = sys.argv[1]
    if len(sys.argv)> 2:
        playback_speed = int(sys.argv[2])
    else:
        playback_speed = 5
    log.info(f"Sensor ID: {sensor_id}")
    sensor_simulator = SensorSimulator(sensor_id)
    sensor_simulator.start_simulator(playback_speed)

