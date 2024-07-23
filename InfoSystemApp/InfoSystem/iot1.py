import json
import time
from paho.mqtt import client as mqtt_client

host = 'localhost'

def mqtt_publish(device_topic):
    client = mqtt_client.Client()
    client.connect(host, 1883, 60)

    while True:
        data = {'temperature': 100, 'humidity': 50}
        payload = json.dumps(data)
        client.publish(device_topic, payload)
        time.sleep(10)

if __name__ == '__main__':
    device_topic = 'device1'
    mqtt_publish(device_topic)