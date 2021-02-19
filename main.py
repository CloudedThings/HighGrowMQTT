import time
from decimal import Decimal
import math
import paho.mqtt.client as mqtt
import json
from botocore.exceptions import ClientError
from table_maker import store_data, get_resource

mqtt_address = "192.168.0.26"
port = 1883
topic = "Arbetsrum/HighGrow"


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topic)


def on_message(client, userdata, msg):
    message = msg.payload.decode('ascii')
    print(message)
    extract_data_from_json(message)


def extract_data_from_json(msg):
    data = json.loads(msg, parse_float=Decimal)
    timestamp = math.floor(time.time())
    temp = data['temp']['temp']
    humid = data['humid']['humid']
    soil = data['soil']['soil']
    data_to_send = {
        "deviceid": '1',
        "devicename": 'HighGrow',
        "timestamp": timestamp,
        "temp": temp,
        "humid": humid,
        "soil": soil,

    }
    store_data(data_to_send)


def get_all_data(dynamodb=None):
    if not dynamodb:
        dynamodb = get_resource()

    table = dynamodb.Table('SensorData2')

    try:
        response = table.scan()
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Items']


def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(host=mqtt_address, port=port, keepalive=60)
    client.loop_forever()


if __name__ == '__main__':
    main()
