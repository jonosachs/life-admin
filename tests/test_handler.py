from functions.slack_handler.handler import lambda_handler
from tests.mock_event import mock_event


def test_slack_handler():
    lambda_handler(event=mock_event, context=None)
