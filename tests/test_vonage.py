"""Check Vonage balance, account status, etc."""
import texts


def test_vonage_balance():
    """Make sure the Vonage account has at least $3 loaded."""
    balance = float(texts.nexmo_client.get_balance()["value"])
    assert balance > 1
