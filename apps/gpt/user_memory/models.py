"""Models for the user memory tool."""
from pydantic import BaseModel, validator

import datetime as dt


class Entry(BaseModel):
    """Memory entry."""
    datetime: dt.datetime
    user_phone: str
    content: str

    @validator("datetime", pre=True)
    def parse_datetime(cls, v):
        """Parse datetime."""
        if isinstance(v, str):
            return dt.datetime.fromisoformat(v)

    def to_string(self) -> str:
        """Return the entry as a string."""
        return (
            f"Date: {self.datetime.isoformat()}\n"
            f"Content: {self.content}"
        )

    def to_dict(self) -> dict:
        """Return the entry as a dictionary."""
        return {
            "datetime": self.datetime.isoformat(),
            "user_phone": self.user_phone,
            "content": self.content
        }
