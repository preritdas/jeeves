"""Permissions database."""
from deta import Deta
from pydantic import BaseModel, validator, root_validator

from typing import Self
import time

from jeeves.keys import KEYS
from jeeves.utils import validate_phone_number, refresh_zapier_access_token, access_token_expired


permissions_db = Deta(KEYS.Deta.project_key).Base("permissions")


class User(BaseModel):
    """
    A user in the permissions database.
    
    Attributes:
        name: The user's name.
        gender_male: if True, male, if False, female.
        phone: The user's phone number.
        time_offset: The user's time offset from UTC.
        use_applets: Whether the user can use applets.
        zapier_key: The user's Zapier key. Optional.
        telegram_id: The user's Telegram ID. Optional.
    """
    key: str
    name: str
    gender_male: bool
    phone: str
    timezone: str
    use_applets: bool
    zapier_access_token: str | None = None
    zapier_refresh_token: str | None = None
    telegram_id: int | None = None

    @validator("phone")
    def validate_phone(cls, phone: str) -> str:
        """Validate phone number."""
        return validate_phone_number(phone)

    @validator("timezone", pre=True)
    def validate_timezone(cls, timezone: str) -> str:
        """Pre to turn offset into a string."""
        assert isinstance(timezone, str)
        timezone = timezone.upper()

        mappings: dict[str, str] = {
            "EST": "America/New_York",
            "CST": "America/Chicago",
            "MST": "America/Denver",
            "PST": "America/Los_Angeles"
        }

        if not timezone in mappings:
            raise ValueError(f"Invalid timezone: {timezone}")

        return mappings[timezone]

    @root_validator
    def validate_zapier(cls, values: dict) -> dict:
        """
        Check the access token for validity. If it's invalid, use the refresh token 
        to refresh it and update the access token both in the User object 
        and in the database.
        """
        if access_token_expired(values["zapier_access_token"]):
            values["zapier_access_token"] = refresh_zapier_access_token(
                values["zapier_refresh_token"]
            )
            permissions_db.update(
                {"ZapierAccessToken": values["zapier_access_token"]},
                values["key"]
            )

        return values

    @classmethod
    def from_phone(cls, phone: str) -> Self | None:
        """Get a user by phone number. Returns None if not found."""
        try:
            items = permissions_db.fetch({"Phone": validate_phone_number(phone)}).items
        except Exception as e:
            if "Request-sent" in str(e):
                time.sleep(0.5)
                items = permissions_db.fetch({"Phone": validate_phone_number(phone)}).items

        if not items:
            return None

        if len(items) > 1:
            raise ValueError(
                f"Multiple users found with the same phone number. "
                f"This is almost certainly an error."
            )

        user = items[0]
        return cls(
            key=user["key"],
            name=user["Name"],
            gender_male=user["GenderMale"],
            phone=user["Phone"],
            timezone=user["Timezone"],
            use_applets=user["UseApplets"],
            zapier_access_token=user["ZapierAccessToken"],
            zapier_refresh_token=user["ZapierRefreshToken"],
            telegram_id=user["TelegramID"]
        )

    @classmethod
    def from_telegram_id(cls, telegram_id: int) -> Self | None:
        """
        Get a user by Telegram ID. Returns None if not found.
        """
        try:
            items = permissions_db.fetch({"TelegramID": telegram_id}).items
        except Exception as e:
            if "Request-sent" in str(e):
                time.sleep(0.5)
                items = permissions_db.fetch({"TelegramID": telegram_id}).items

        if not items:
            return None
        
        if len(items) > 1:
            raise ValueError(
                f"Multiple users found with the same Telegram ID. "
                f"This is almost certainly an error."
            )
        
        user = items[0]
        return cls(
            name=user["Name"],
            gender_male=user["GenderMale"],
            phone=user["Phone"],
            timezone=user["Timezone"],
            use_applets=user["UseApplets"],
            zapier_key=user["ZapierKey"],
            telegram_id=user["TelegramID"]
        )
