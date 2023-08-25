from mqtt_plugin import Mqttplugin
import time
import logging as log
import sys

mqtt_broker_url = "localhost"
port = 1883

def start_backend_client(client_id):
    mqtt_plugin = Mqttplugin(client_id)
    def stop_device():
        mqtt_plugin.stop_sensor_reader()
        sys.exit()

    start_success = mqtt_plugin.run_sensor_reader(mqtt_broker_url,port)
    if not start_success:
        log.error(f"Failed to start the Sensor with ID: {client_id}")
        return

    try:
        while True:
            if mqtt_plugin.sensor_reading:
                time.sleep(2)
    except KeyboardInterrupt:
        stop_device()

    
if __name__ == '__main__':
    client_id = sys.argv[1]
    log.info(f"Sensor backend client ID: {client_id}")
    start_backend_client(client_id)
    