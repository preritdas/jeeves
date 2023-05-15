"""Routes for authenticating, ex. Zapier."""
from fastapi import APIRouter, Response
import requests
from deta import Deta

from jeeves.keys import KEYS


router = APIRouter()


permissions_db = Deta(KEYS.Deta.project_key).Base("permissions")


@router.get("/zapier-handler/{user_key}")
async def handle_zapier(user_key: str, code: str):
    """
    Handle a Zapier authentication code. Takes the code and update's the user's
    access token in the permissions database.

    Args:
        user_key (str): The user key - Deta key for their user entry.
        code (str): The authentication code.
    """
    # Find the user in the database
    user = permissions_db.get(user_key)

    if not user:
        return Response("User not found.", status_code=404)

    # Generate the access token and refresh token
    url = "https://nla.zapier.com/oauth/token"
    res = requests.post(
        url,
        data={
            "client_id": KEYS.Zapier.client_id,
            "client_secret": KEYS.Zapier.client_secret,
            "code": code,
            "grant_type": "authorization_code"
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )

    if res.status_code != 200:
        return Response("Error generating access token.", status_code=500)

    # Update the user's access token
    user["ZapierAccessToken"] = res.json()["access_token"]
    user["ZapierRefreshToken"] = res.json()["refresh_token"]

    # Save the user
    permissions_db.put(user)

    return Response("Success!", status_code=200)
