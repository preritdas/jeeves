"""Routes for authenticating, ex. Zapier."""
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
import requests
from deta import Deta

from jeeves.texts import BASE_URL
from jeeves.keys import KEYS


router = APIRouter()


permissions_db = Deta(KEYS.Deta.project_key).Base("permissions")


@router.get("/zapier-start/{user_key}")
async def zapier_start(user_key: str) -> str:
    """Create the link for the user to use to start with Zapier."""
    redirect_uri = BASE_URL + f"/auth/zapier-handler/{user_key}"

    return RedirectResponse(
        f"https://nla.zapier.com/oauth/authorize?"
        f"client_id={KEYS.Zapier.client_id}&response_type=code"
        f"&redirect_uri={redirect_uri}"
        "&scope=nla%3Aexposed_actions%3Aexecute"
    )


@router.get("/zapier-handler/{user_key}")
def handle_zapier(user_key: str, code: str):
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
        return {"error": "User not found."}

    # Generate the access token and refresh token
    url = "https://nla.zapier.com/oauth/token/"
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
        return {"error": "Error generating access token."}

    # Update the user's access token
    user["ZapierAccessToken"] = res.json()["access_token"]
    user["ZapierRefreshToken"] = res.json()["refresh_token"]

    # Save the user
    permissions_db.put(user)

    return {"status": "success"}
