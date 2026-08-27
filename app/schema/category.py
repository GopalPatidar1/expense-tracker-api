from pydantic import BaseModel, Field, ConfigDict
from enum import Enum

class Categories(str, Enum):
    GROCERIES = "groceries"
    LEISURE ="leisure"
    ELECTRONICS="electronics"
    UTILITIES="utilities"
    CLOTHING="clothing"
    HEALTH="health"
    OTHERS="others"


class CreateCategory(BaseModel):
    category: str = Categories
    model_config = ConfigDict(extra="forbid")

