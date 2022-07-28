from datetime import datetime
import json
import uuid

import boto3

from app.utils.constants import DATE_FORMAT


def get_request_id(event, context):
    try:
        if event and event['Records'][0]['messageAttributes']['request_id']['stringValue']:
            return uuid.UUID(event['Records'][0]['messageAttributes']['request_id']['stringValue']).hex
        elif context and context.aws_request_id:
            return context.aws_request_id
        else:
            return uuid.uuid1()
    except Exception:
        return uuid.uuid1()


def is_str_or_dict(message):
    if type(message) is str:
        return json.loads(message)
    elif type(message) is dict:
        return message


def format_date(data):
    return data[4:] + "-" + data[2:4] + "-" + data[:2] + 'T00:00:00Z'


def format_amount(amount):
    return format(int(amount) / 100, '.02f')
