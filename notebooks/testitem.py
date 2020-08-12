from __future__ import annotations
from base import BaseModel


class ItemBase(BaseModel):
    pass

class Item(ItemBase):
    id: int
    owner_id: int
    title: str
    description: str = None

    owner: User

    class Config:
        orm_mode = True
    
from testuser import User
Item.update_forward_refs()