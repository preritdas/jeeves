"""Models for the user memory tool."""
from pydantic import BaseModel

import datetime as dt


class Entry(BaseModel):
    """Memory entry."""
    datetime: dt.datetime
    user_phone: str
    content: str

    def to_dict(self) -> dict:
        """Return the entry as a dictionary."""
        return {
            "datetime": self.datetime.isoformat(),
            "user_phone": self.user_phone,
            "content": self.content
        }
