from sqlalchemy import select, delete, update
from sqlalchemy.orm import selectinload
from app.models.expenses import Expenses
from app.models.users import User
from sqlalchemy.ext.asyncio import AsyncSession

async def add_expenses(db:AsyncSession, expenses):
    db.add(expenses)

async def get_expense_list(db: AsyncSession, user_id: str, next_cursor: int | None, limit:int, start_date,  end_date):
    filter = [Expenses.user_id == user_id]

    if start_date is not None:
        filter.append(Expenses.created_at >= start_date)

    if end_date is not None:
        filter.append(Expenses.created_at <= end_date)

    if next_cursor is not None:
        filter.append(Expenses.id <= next_cursor)

    result = await db.scalars(
        select(Expenses)
        .options(selectinload(Expenses.user), selectinload(Expenses.category)) 
        .where(*filter)
        .order_by(Expenses.id.desc())
        .limit(limit+1)
    )

    return result.all()

async def delete_expense(id: int, user_id: int, db: AsyncSession):
    result = await db.execute(delete(Expenses).where(
        Expenses.user_id == user_id,
        Expenses.id == id
    ))

    await db.commit()

    return result

async def update_expense(db: AsyncSession, id:int, user_id: int, data):
     result = await db.execute(
        update(Expenses)
        .where(
            Expenses.id == id,
            Expenses.user_id == user_id
        )
        .values(**data.model_dump(exclude_unset=True))
        .returning(Expenses)
       )

     return result.scalar_one_or_none()