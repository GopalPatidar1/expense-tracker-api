from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.models.expense_categories import ExpenseCategories

async def create_category(db: AsyncSession, data):
   db.add(data)
   return data

async def get_category(db: AsyncSession):
   data = await db.scalars(select(ExpenseCategories))
   return data.all()

async def update_category(db: AsyncSession, id: int,  data):
   result = await db.execute(
           update(ExpenseCategories)
           .where(ExpenseCategories.id == id,)
           .values(**data.model_dump(exclude_unset=True))
           .returning(ExpenseCategories)
          )
   return result.scalar_one_or_none()

async def delete_category(db: AsyncSession, id: int):
   return await db.execute(delete(ExpenseCategories).where(ExpenseCategories.id == id))