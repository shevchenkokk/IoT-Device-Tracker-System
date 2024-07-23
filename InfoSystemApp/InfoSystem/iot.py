import json
import time
import random
from paho.mqtt import client as mqtt_client

host = 'localhost'

def mqtt_publish(device_topic):
    client = mqtt_client.Client()
    client.connect(host, 1883, 60)

    while True:
        data = {'temperature': random.randrange(0, 50), 'humidity': random.randrange(0, 100)}
        payload = json.dumps(data)
        client.publish(device_topic, payload)
        time.sleep(10)

if __name__ == '__main__':
    device_topic = 'esp8266/devices/5/telemetry'
    mqtt_publish(device_topic)