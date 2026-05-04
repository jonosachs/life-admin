from datetime import datetime, timedelta
import boto3
from models.event import Event
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import logging
import json
from decimal import Decimal

logger = logging.getLogger(__name__)


# Docs:
# https://docs.aws.amazon.com/boto3/latest/guide/quickstart.html
# https://docs.aws.amazon.com/code-library/latest/ug/python_3_dynamodb_code_examples.html


class Declined:
    def __init__(self):
        self.dynamodb = boto3.resource("dynamodb")
        self.table = self.dynamodb.Table("Declined")

    def add(self, event: Event):
        e = json.loads(event.model_dump_json(), parse_float=Decimal)
        # expiry used with Dynamo's Time to Live (TTL) which auto deletes expired entries
        expiry = int((datetime.now() + timedelta(days=5)).timestamp())

        try:
            self.table.put_item(
                Item={
                    "id": e["id_"],
                    "expiry": expiry,
                    **e,
                }
            )
        except ClientError as err:
            logger.error(
                f"Couldn't add event {event.id_}.",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise

    def get_all(self):
        try:
            response = self.table.scan()
            items = response.get("Items", [])
            return items
        except ClientError as err:
            logger.error(
                "Couldn't get events.",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )

    def delete(self, id):
        try:
            self.table.delete_item(Key={"id": id})
        except ClientError as err:
            logger.error(
                f"Couldn't delete event {id}.",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
