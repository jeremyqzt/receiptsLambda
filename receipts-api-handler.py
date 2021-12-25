try:
  import unzip_requirements
except ImportError:
  pass

import json
import logging
import boto3
import datetime
import dynamo
import os
from PIL import Image
from loader import Loader
logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.client('dynamodb')
s3_client = boto3.client('s3')

dest_bucket = 'receipt-attach'
table_name = 'attach-store'


def create(event, context):
    logger.info(f'Incoming request is: {event}')

    # Set the default error response
    response = {
        "statusCode": 500,
        "body": "An error occured while creating post."
    }

    some_text = "test"
    file_name = "my_test_file.csv"
    lambda_path = "/tmp/" + file_name
    s3_path = "output/" + file_name
    os.system('echo testing... >'+lambda_path)
    s3_client.upload_file(lambda_path, dest_bucket, file_name)

    post_str = event['body']
    post = json.loads(post_str)
    current_timestamp = datetime.datetime.now().isoformat()
    post['createdAt'] = current_timestamp

    s3 = boto3.client('s3')

    res = dynamodb.put_item(
        TableName=table_name, Item=dynamo.to_item(post))

    # If creation is successful
    if res['ResponseMetadata']['HTTPStatusCode'] == 200:
        response = {
            "statusCode": 201,
            "fileName": s3_path
        }

    return response


def get(event, context):
    logger.info(f'Incoming request is: {event}')

    # Set the default error response
    response = {
        "statusCode": 500,
        "body": "An error occured while creating post."
    }

    file_name = "my_test_file.csv"
    lambda_path = "/tmp/" + file_name
    s3_path = "output/" + file_name
    os.system('echo testing... >'+lambda_path)
    s3_client.upload_file(lambda_path, dest_bucket, file_name)

    post_str = Loader.parse_data(event)

    logger.info(f'Store values is: {str(post_str)}')

    res = dynamodb.put_item(
        TableName=table_name, Item=dynamo.to_item(post_str))

    # If creation is successful
    if res['ResponseMetadata']['HTTPStatusCode'] == 200:
        response = {
            "statusCode": 201,
            "fileName": s3_path
        }

    return response

