from __future__ import annotations

from typing import List
from base import BaseModel



class UserBase(BaseModel):
    pass

class User(UserBase):
    id: int
    email: str
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True

from testitem import Item
User.update_forward_refs()