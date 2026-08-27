from pydantic import BaseModel, Field
from enum import Enum

class PaymentMethod(str, Enum):
    CASH = "cash"
    UPI = "upi"
    CARD = "card"
    OTHER = "other"


class ExpenseItem(BaseModel):
    amount: int = Field(ge=1)
    description: str = Field(min_length=5, max_length=255)
    payment_method: PaymentMethod
    category_id: int

class UpdateExpenseItem(BaseModel):
    amount: int | None = Field(ge=1)
    payment_method: PaymentMethod | None = None
    description: str | None = Field(min_length=5, max_length=255)
    category_id: int | None = None
