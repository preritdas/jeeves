"""Routes for authenticating, ex. Zapier."""
from fastapi import APIRouter
from fastapi.responses import RedirectResponse

import requests
from deta import Deta

import urllib.parse

from jeeves.texts import BASE_URL
from jeeves.keys import KEYS
from jeeves.utils import validate_phone_number


router = APIRouter()
permissions_db = Deta(KEYS.Deta.project_key).Base("permissions")


@router.get("/user-by-phone/{phone_number}")
async def user_by_phone(phone_number: str, access_code: str) -> dict:
    """Get the user's key by their phone number."""
    # Check the access code
    if access_code != KEYS.General.auth_access_code:
        return {"error": "Invalid access code."}

    try:
        phone_number = validate_phone_number(phone_number)
    except ValueError as e:
        return {"error": f"Invalid phone number. {str(e)}"}

    res = permissions_db.fetch({"Phone": phone_number}).items

    if not res:
        return {"error": "User not found."}

    if len(res) > 1:
        return {"error": "Multiple users found."}

    return {"user": res[0]["key"]}


@router.get("/zapier-start/{user_key}")
async def zapier_start(user_key: str) -> RedirectResponse:
    """
    Create the link for the user to use to start with Zapier. Redirects the user
    to their Zapier authentication setup page.
    """
    redirect_uri = BASE_URL + "/auth/zapier-handler/"
    redirect_uri = urllib.parse.quote_plus(redirect_uri)

    return RedirectResponse(
        f"https://nla.zapier.com/oauth/authorize/"
        f"?client_id={KEYS.Zapier.client_id}&response_type=code"
        f"&redirect_uri={redirect_uri}"
        f"&state={user_key}"
        "&scope=nla%3Aexposed_actions%3Aexecute"
    )


@router.get("/zapier-handler")
def handle_zapier(state: str, code: str):
    """
    Handle a Zapier authentication code. Takes the code and update's the user's
    access token in the permissions database.

    Args:
        state (str): The user key - Deta key for their user entry.
        code (str): The authentication code.
    """
    # Find the user in the database
    user: dict = permissions_db.get(state)

    if not user:
        return {"error": "User not found."}

    # Generate the access token and refresh token
    res = requests.post(
        url="https://nla.zapier.com/oauth/token/",
        data={
            "client_id": KEYS.Zapier.client_id,
            "client_secret": KEYS.Zapier.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": BASE_URL + "/auth/zapier-handler/"
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )

    if res.status_code != 200:
        return {"error": "Error generating access token."}

    # Update the user's access token
    res_json = res.json()
    user.update(
        {
            "ZapierAccessToken": res_json["access_token"],
            "ZapierRefreshToken": res_json["refresh_token"]
        }
    )

    # Save the user
    permissions_db.put(user)

    return {"status": "success"}
