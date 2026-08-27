from pydantic import BaseModel, Field
from enum import Enum

class PaymentMethod(str, Enum):
    CASH = "cash"
    UPI = "upi"
    CARD = "card"
    OTHER = "other"

class ExpenseDateFilter(str, Enum):
    PAST_WEEK = "past_week"
    PAST_MONTH = "past_month"
    LAST_3_MONTHS = "last_3_months"
    CUSTOM = "custom"

class ExpenseItem(BaseModel):
    amount: int = Field(ge=1)
    description: str = Field(min_length=5, max_length=255)
    payment_method: PaymentMethod
    category_id: int

class UpdateExpenseItem(BaseModel):
    amount: int | None = Field(default=None, ge=1)
    payment_method: PaymentMethod | None = None
    description: str | None = Field(min_length=5, max_length=255)
    category_id: int | None = None

class UserInfo(BaseModel):
    firstname: str
    lastname: str

class CategoryInfo(BaseModel):
    id: int
    category: str

class ExpenseResponseItem(BaseModel):
    id: int
    amount: int
    description: str
    payment_method: PaymentMethod
    category: CategoryInfo
    user: UserInfo


class ExpenseResponse(BaseModel):
    next_cursor: int | None = None
    avail_next: bool
    result: list[ExpenseResponseItem]