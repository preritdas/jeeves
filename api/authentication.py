"""Routes for authenticating, ex. Zapier."""
from fastapi import APIRouter
import requests

from jeeves.keys import KEYS


router = APIRouter()


@router.get("/zapier-handler/{user_key}")
async def handle_zapier(user_key: str, code: str):
    """
    Handle a Zapier authentication code.

    Args:
        user_key (str): The user key - Deta key for their user entry.
        code (str): The authentication code.
    """
    print(code)
    return {"code": code}
