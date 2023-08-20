"""Models for the user memory tool."""
from pydantic import field_validator, BaseModel

import datetime as dt


class Entry(BaseModel):
    """Memory entry."""
    datetime: dt.datetime
    user_phone: str
    content: str

    @field_validator("datetime", mode="before")
    def parse_datetime(cls, v):
        """Parse datetime. Mode is 'before' to convert to datetime before validation."""
        if isinstance(v, str):
            return dt.datetime.fromisoformat(v)
        elif isinstance(v, dt.datetime):
            return v
        else:
            raise ValueError("datetime must be a string or a datetime object.")

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
