from sqlalchemy import select, delete, update
from sqlalchemy.orm import selectinload
from app.models.expenses import Expenses
from app.models.users import User
from sqlalchemy.ext.asyncio import AsyncSession

async def addExpenses(db:AsyncSession, expenses):
    db.add(expenses)

async def getExpenselist(db: AsyncSession, userId: str, nextCursor: int | None, limit:int):
    filterRec = [Expenses.user_id == userId]

    if nextCursor is not None:
        filterRec.append(Expenses.id <= nextCursor)

    result = await db.scalars(
        select(Expenses)
        .options(selectinload(Expenses.user)) 
        .where(*filterRec)
        .order_by(Expenses.id.desc())
        .limit(limit+1)
    )

    return result.all()

async def deleteExpense(id: int, userId: int, db: AsyncSession):
    result = await db.execute(delete(Expenses).where(
        Expenses.user_id == userId,
        Expenses.id == id
    ))

    await db.commit()

    return result

async def updateExpense(db: AsyncSession, id:int, userId: int, data):
     result = await db.execute(
        update(Expenses)
        .where(
            Expenses.id == id,
            Expenses.user_id == userId
        )
        .values(**data.model_dump(exclude_unset=True))
        .returning(Expenses)
       )

     return result.scalar_one_or_none()