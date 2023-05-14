"""Various API utilities."""
import requests

from jeeves.keys import KEYS


def set_telegram_webhook(webhook_url: str) -> bool:
    """
    Set the Telegram webhook. Return True if successful, False otherwise. 

    This is a helper function to set the Telegram webhook. webhook_url should be
    the full URL to the webhook endpoint, including the path.
    """
    url = f"https://api.telegram.org/bot{KEYS.Telegram.bot_token}/setWebhook"
    params = {"secret_token": KEYS.Telegram.api_secret_token}
    res = requests.post(url, data={"url": webhook_url}, params=params)

    res.raise_for_status()
    return True if res.status_code == 200 else False
