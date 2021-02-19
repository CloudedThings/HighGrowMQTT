import boto3
from config import *


def get_resource():
    return boto3.resource('dynamodb',
                          aws_access_key_id=ACCESS_KEY,
                          aws_secret_access_key=SECRET_KEY,
                          region_name=REGION_NAME)


def create_sensor_table(dynamodb=None):
    if not dynamodb:
        dynamodb = get_resource()

    table = dynamodb.create_table(
        TableName='SensorData',
        KeySchema=[
            {
                'AttributeName': 'devicename',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'timestamp',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'devicename',
                'AttributeType': 'S'  # Partition key
            },
            {
                'AttributeName': 'timestamp',
                'AttributeType': 'N'  # Partition key
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table


def store_data(data, dynamodb=None):
    if not dynamodb:
        dynamodb = get_resource()

    table = dynamodb.Table('SensorData2')
    print('Adding new data to table...')
    table.put_item(Item=data)


def main():
    create_sensor_table()


if __name__ == '__main__':
    main()