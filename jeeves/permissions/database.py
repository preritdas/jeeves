"""Permissions database."""
from deta import Deta
from pydantic import BaseModel, validator

from typing import Self

from jeeves.keys import KEYS
from jeeves.utils import validate_phone_number


permissions_db = Deta(KEYS.Deta.project_key).Base("permissions")


class User(BaseModel):
    """A user."""
    name: str
    phone: str
    use_applets: bool
    zapier_key: str | None = None
    telegram_id: int | None = None

    @validator("phone")
    def validate_phone(cls, phone: str) -> str:
        """Validate phone number."""
        return validate_phone_number(phone)

    @classmethod
    def from_phone(cls, phone: str) -> Self | None:
        """Get a user by phone number. Returns None if not found."""
        items = permissions_db.fetch({"Phone": phone}).items

        if not items:
            return None

        if len(items) > 1:
            raise ValueError(
                f"Multiple users found with the same phone number. "
                f"This is almost certainly an error."
            )

        user = items[0]
        return cls(
            name=user["Name"],
            phone=user["Phone"],
            use_applets=user["UseApplets"],
            zapier_key=user["ZapierKey"],
            telegram_id=user["TelegramID"]
        )
