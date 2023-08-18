"""Permissions database."""
from pymongo import MongoClient
from bson.objectid import ObjectId
from pydantic import ConfigDict, BaseModel, field_validator, model_validator

from typing import Self

from jeeves.keys import KEYS
from jeeves.utils import validate_phone_number, refresh_zapier_access_token, access_token_expired


# Connect to the MongoDB permissions database collection
PERMISSIONS_COLL = MongoClient(KEYS.MongoDB.connect_str)["Jeeves"]["permissions"]


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
    db_id: ObjectId
    name: str
    gender_male: bool
    phone: str
    timezone: str
    use_applets: bool
    zapier_access_token: str | None = None
    zapier_refresh_token: str | None = None
    telegram_id: int | None = None

    # Pydantic configuration
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("phone")
    def validate_phone(cls, phone: str) -> str:
        """Validate phone number."""
        return validate_phone_number(phone)

    @field_validator("timezone")
    def validate_timezone(cls, timezone: str) -> str:
        """Convert timezone to Olson format, for pytz in prompt formatting."""
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

    @model_validator(mode="after")
    def validate_zapier(self) -> dict:
        """
        Check the access token for validity. If it's invalid, use the refresh token 
        to refresh it and update the access token both in the User object 
        and in the database.
        """
        if self.zapier_access_token and access_token_expired(self.zapier_access_token):
            # Refresh the access token and update the refresh token
            self.zapier_access_token, self.zapier_refresh_token = (
                refresh_zapier_access_token(self.zapier_refresh_token)
            )

            # Update the database
            PERMISSIONS_COLL.update_one(
                {"_id": self.db_id},
                {"$set": {
                    "ZapierAccessToken": self.zapier_access_token,
                    "ZapierRefreshToken": self.zapier_refresh_token
                }}
            )

        return self

    @classmethod
    def _from_db_id(cls, db_id: ObjectId) -> Self:
        """
        Create an object given a key from the database. Use this private
        classmethod when creating other public classmethods that retrieve
        the key in various ways, ex. via phone or via Telegram.
        """
        user = PERMISSIONS_COLL.find_one({"_id": db_id})

        if not user:
            raise ValueError(f"User with _id {db_id} not found.")

        return cls(
            db_id=user["_id"],
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
    def from_phone(cls, phone: str) -> Self | None:
        """Get a user by phone number. Returns None if not found."""
        items = list(PERMISSIONS_COLL.find({"Phone": validate_phone_number(phone)}))

        if not items:
            return None

        if len(items) > 1:
            raise ValueError(
                f"Multiple users found with the same phone number. "
                f"This is almost certainly an error."
            )

        user = items[0]
        return cls._from_db_id(user["_id"])

    @classmethod
    def from_telegram_id(cls, telegram_id: int) -> Self | None:
        """
        Get a user by Telegram ID. Returns None if not found.
        """
        items = list(PERMISSIONS_COLL.find({"TelegramID": telegram_id}))

        if not items:
            return None
        
        if len(items) > 1:
            raise ValueError(
                f"Multiple users found with the same Telegram ID. "
                f"This is almost certainly an error."
            )
        
        user = items[0]
        return cls._from_db_id(user["_id"])
