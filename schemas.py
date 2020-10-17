from typing import List
from pydantic import BaseModel
from tortoise.contrib.pydantic.base import PydanticModel, PydanticListModel


class Status(BaseModel):
    message: str
