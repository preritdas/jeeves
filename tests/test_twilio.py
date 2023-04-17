"""Check Vonage balance, account status, etc."""
import texts


def test_twilio_balance():
    """Make sure the Vonage account has at least $3 loaded."""
    balance = float(texts.twilio_client.balance.fetch().balance)
    assert balance >= 3
