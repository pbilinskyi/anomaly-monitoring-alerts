import os
import ssl

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

import certifi
from dotenv import load_dotenv

load_dotenv()


def post_alert_message():
    """ Send alert message to Slack channel 'anomaly-alerts'.
    """
    token = os.getenv('SLACK_ALERT_BOT_TOKEN')

    ssl_context = ssl.create_default_context(cafile=certifi.where())
    client = WebClient(token=token,
                       ssl=ssl_context)

    # SEND MESSAGE
    channel_id = os.getenv('SLACK_ALERT_CHANNEL_ID')

    try:
        # Call the conversations.list method using the WebClient
        result = client.chat_postMessage(
            channel=channel_id,
            text="Hello world!"
            # You could also use a blocks[] array to send richer content
        )
        # Print result, which includes information about the message (like TS)
        print(result)

    except SlackApiError as e:
        print(f"Error: {e}")
