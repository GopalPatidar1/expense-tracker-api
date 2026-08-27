from pydantic import BaseModel, Field, ConfigDict
from enum import Enum

class Categories(str, Enum):
    CASH = "cash"
    UPI = "upi"
    CARD = "card"
    OTHER = "other"


class CreateCategory(BaseModel):
    category: str = Categories
    model_config = ConfigDict(extra="forbid")

