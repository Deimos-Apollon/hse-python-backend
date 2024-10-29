from typing import Optional

from pydantic import BaseModel, ConfigDict


class Item(BaseModel):
    """Represents Item as a unit in the store."""
    id: int
    name: str
    price: float
    deleted: bool = False


class ItemCreate(BaseModel):
    """Represents info for item creation in the store."""
    name: str
    price: float


class ItemReplace(BaseModel):
    """Represents info for item replacing in the store."""
    name: str
    price: float
    deleted: bool = False

    model_config = ConfigDict(extra="forbid")

class ItemModify(BaseModel):
    """Represents info for item replacing in the store."""
    name: Optional[str] = None
    price: Optional[float] = None

    model_config = ConfigDict(extra="forbid")
