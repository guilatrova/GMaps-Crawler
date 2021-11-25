from dataclasses import asdict
from typing import TypedDict

import boto3
from mypy_boto3_sqs.type_defs import SendMessageResultTypeDef

from gmaps_crawler.entities import Place
from gmaps_crawler.exceptions import CantEmitPlace


class SQSMessageAttributeFormat(TypedDict):
    place_id: str


class SQSMessageFormat(TypedDict):
    body: str
    attributes: SQSMessageAttributeFormat


class SQSEmitter:
    def __init__(self, queue_url: str):
        self.client = boto3.client("sqs")
        self.queue_url = queue_url

    def emit(self, place: Place):
        try:
            message = self._create_message(place)
            self._send_message(message)
        except Exception as ex:
            raise CantEmitPlace(place, self.queue_url) from ex

    def _create_message(self, place: Place) -> SQSMessageFormat:
        body = str(asdict(place))
        return dict(body=body, attributes=dict(place_id=place.identifier))

    def _send_message(self, message: SQSMessageFormat) -> SendMessageResultTypeDef:
        response = self.client.send_message(
            QueueUrl=self.queue_url,
            MessageBody=message["body"],
            MessageAttributes=message["attributes"],
        )
        return response
