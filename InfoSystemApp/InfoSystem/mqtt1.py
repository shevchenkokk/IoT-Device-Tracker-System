from paho.mqtt import client as mqtt_client

#mqtt connection info
host = 'localhost'
port = 1883
topic = ''
topic_sub = 'device1'

client_id = '1'
username = 'kirill'
password = '123'
device_id = ''

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Successefully connected to MQTT')
    else:
        print(f'Failed to connect, error code: {rc}')

def connect_to_mqtt():
    client = mqtt_client.Client(client_id=client_id)
    #client.username_pw_set(username=username, password=password)
    #client.on_connect = on_connect
    #client.connect(host=host, port=port)
    return client
    
def subscribe(client: mqtt_client):
    #def on_message(client, userdata, msg):
    #    print(f"Received '{msg.payload.decode()}' from '{msg.topic}' topic")
    client.subscribe(topic_sub)
    #client.on_message = on_message

def main():
    client = connect_to_mqtt()
    subscribe(client)

    #client.loop_forever()

if __name__ == '__main__':
    main()