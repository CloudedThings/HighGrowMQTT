import boto3
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError
from datetime import datetime, timezone
from datetime import timedelta

from config import *


def get_resource():
    return boto3.resource('dynamodb',
                          aws_access_key_id=ACCESS_KEY,
                          aws_secret_access_key=SECRET_KEY,
                          region_name=REGION_NAME)


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


def get_all_by_devicename(devicename, dynamodb=None):
    if not dynamodb:
        dynamodb = get_resource()

    table = dynamodb.Table('SensorData2')

    try:
        response = table.scan(FilterExpression=Attr('devicename').eq(devicename))
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Items']


class Device:
    def __init__(self, time, deviceid, devicename, humid, soil, temp):
        self.time = time
        self.deviceid = deviceid
        self.devicename = devicename
        self.humid = humid
        self.soil = soil
        self.temp = temp

    def __repr__(self):
        return f'Device({self.time}, {self.deviceid}, {self.devicename}, {self.humid}, {self.soil}, {self.temp})'

    def __str__(self):
        return f'Device {self.devicename} with id {self.deviceid} gave value temp: {self.temp}, soil: {self.soil}, ' \
               f'humid: {self.humid} at {self.time}'


    @staticmethod
    def create_from_dict(dict_data):
        timestamp = int(dict_data['timestamp'])
        time = datetime.fromtimestamp(timestamp, timezone.utc)
        deviceid = dict_data['deviceid']
        devicename = dict_data['devicename']
        humid = dict_data['humid']
        soil = dict_data['soil']
        temp = dict_data['temp']

        return Device(time, deviceid, devicename, humid, soil, temp)


def main():
    values = get_all_data()
    values = [Device.create_from_dict(value) for value in values]
    for value in values:
        print(value)


if __name__ == '__main__':
    main()