from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.models.expenseCategories import ExpenseCategories

async def createCategory(db: AsyncSession, data):
   db.add(data)
   return data

async def getCategory(db: AsyncSession):
   data = await db.scalars(select(ExpenseCategories))
   return data.all()

async def updateCategory(db: AsyncSession, id: int,  data):
   result = await db.execute(
           update(ExpenseCategories)
           .where(ExpenseCategories.id == id,)
           .values(**data.model_dump(exclude_unset=True))
           .returning(ExpenseCategories)
          )
   return result.scalar_one_or_none()

async def deleteCategory(db: AsyncSession, id: int):
   return await db.execute(delete(ExpenseCategories).where(ExpenseCategories.id == id))