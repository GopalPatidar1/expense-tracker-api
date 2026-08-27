from typing import Optional
from datetime import datetime
from enum import Enum
from sqlalchemy import String, DateTime, func, Enum as SQLEnum, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase ,Mapped, mapped_column, relationship
from app.config.database import Base
import bcrypt

class PaymentMethod(str, Enum):
    CASH = "cash"
    UPI = "upi"
    CARD = "card"
    OTHER = "other"

class Expenses(Base):
    __tablename__ = "expenses"
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(30), nullable=False)
    amount: Mapped[int | None]= mapped_column(Integer, nullable=True)

    payment_method:Mapped[PaymentMethod]=mapped_column(SQLEnum(PaymentMethod), default=PaymentMethod.OTHER, nullable=False)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("expense_categories.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
            back_populates="expenses"
        )

    category: Mapped["ExpenseCategories"] = relationship(
                back_populates="expenses"
            )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False,)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False,)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True,)
