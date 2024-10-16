from pydantic import BaseModel
from typing import List, Optional


class Ans(BaseModel):
    name: str
    completed: bool
    l: List[int]


class Item(BaseModel):
    name: str
    completed: bool
