"""Module for defining JSOn schema models"""

from pydantic import BaseModel


class Keywords(BaseModel):
    """Object for keywords extraction"""

    keywords: list[str]
