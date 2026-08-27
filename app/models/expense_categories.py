from typing import Optional
from datetime import datetime
from enum import Enum
from sqlalchemy import String, DateTime, func, Enum as SQLEnum, Integer
from sqlalchemy.orm import DeclarativeBase ,Mapped, mapped_column, relationship
from app.config.database import Base
import bcrypt

class Categories(str, Enum):
    GROCERIES = "groceries"
    LEISURE ="leisure"
    ELECTRONICS="electronics"
    UTILITIES="utilities"
    CLOTHING="clothing"
    HEALTH="health"
    OTHERS="others"

class ExpenseCategories(Base):
    __tablename__ = "expense_categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    expenses: Mapped[list["Expenses"]] = relationship(
                back_populates="category"
            )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False,)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False,)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True,)
