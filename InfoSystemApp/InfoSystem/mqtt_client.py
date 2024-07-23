from paho.mqtt import client as mqtt_client
import json
from .models import Parameter, DataFrame
from datetime import datetime

mqtt_clients = {}

class MQTTClient:
    def __init__(self, client_id, username, password):
        self.client = None
        self.client_id = client_id
        self.username = username
        self.password = password
        self.host = 'localhost'
        self.port = 1883

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print('Successefully connected to MQTT')
        else:
            print(f'Failed to connect, error code: {rc}')

    def connect_to_mqtt(self):
        self.client = mqtt_client.Client(client_id=self.client_id)
        self.client.username_pw_set(username=self.username, password=self.password)
        self.client.on_connect = self.on_connect
        self.client.connect(host=self.host, port=self.port)

    def on_message(self, client, userdata, msg):
        print(f"Client {self.client_id} received '{msg.payload.decode()}' from '{msg.topic}' topic")
        device_id = msg.topic.split('/')[-2]
        parameters = Parameter.objects.filter(device_id=device_id)
        parameter_names = []
        for parameter in parameters:
            if parameter.parameter_name not in parameter_names:
                parameter_names.append(parameter.parameter_name)
        data = json.loads(msg.payload.decode())
        for parameter_name, value in data.items():
            if parameter_name not in parameter_names:
                parameter = Parameter.objects.create(
                    device_id=device_id,
                    parameter_name=parameter_name,
                    parameter_symbol = parameter_name,
                )
                parameter.save()
            else:
                parameter = Parameter.objects.get(device_id=device_id, parameter_name=parameter_name)
            data_frame = DataFrame.objects.create(
                parameter_id = parameter.parameter_id,
                timestamp = datetime.now(),
                result = str(value),
            )
            data_frame.save()

    def subscribe(self, topic_sub: str):
        self.client.subscribe(topic_sub)
        self.client.on_message = self.on_message

def main():
    client = MQTTClient('1', 'kirill', '12345')
    client.connect_to_mqtt()
    client.subscribe('device')
    client.client.loop_start()

    while True:
        pass

if __name__ == '__main__':
    main()