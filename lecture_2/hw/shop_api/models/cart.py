from pydantic import BaseModel
from typing import List


class ItemInCart(BaseModel):
    """Represents Item as a unit in the shopping cart."""
    id: int
    name: str
    quantity: int = 1
    available: bool = True


class Cart(BaseModel):
    """Represents individual cart in the shop."""
    id: int
    items: List[ItemInCart] = []
    price: float = 0.0
