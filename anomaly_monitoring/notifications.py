import os
import logging
import ssl

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

import certifi
from dotenv import load_dotenv

load_dotenv()


def send_alert_slack(text: str):
    """ Postes alert message to the Slack channel `anomaly-alerts`.
    """
    logging.info('Sending alert to Slack...')
    # Authenticate to Slack
    token = os.getenv('SLACK_ALERT_BOT_TOKEN')

    ssl_context = ssl.create_default_context(cafile=certifi.where())
    client = WebClient(token=token,
                       ssl=ssl_context)

    # Post message to Slack channel `anomaly-alerts`
    channel_id = os.getenv('SLACK_ALERT_CHANNEL_ID')
    try:
        result = client.chat_postMessage(
            channel=channel_id,
            text=text
            # You could also use a blocks[] array to send richer content
        )
        logging.info("Result of sending query to Slack "
                     "about posting message: \n %s" % result)
    except SlackApiError as e:
        logging.error(f"Error occured while trying to send a Slack alert: {e}")
