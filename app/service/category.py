from app.repository import category 
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.customException import CustomException
from fastapi import status
from app.models.expense_categories import ExpenseCategories
from app.schema.category import CreateCategory

async def create_category(data, db: AsyncSession):
    try:
     category_data = ExpenseCategories(
       category=data.category
     )

     await category.create_category(db=db, data=category_data)

     await db.commit()

     await db.refresh(category_data)
 
     return { "id": category_data.id }

    except Exception as e:
     await db.rollback()
     raise CustomException(status.HTTP_500_INTERNAL_SERVER_ERROR)

async def get_category(db:AsyncSession):
  try:
   return await category.get_category(db)
  except Exception as e:
    await db.rollback()
    raise CustomException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to fetch categories")

async def update_category(db: AsyncSession, id: int, data):
   try:
     category_data =  await category.update_category(db=db, data=data, id=id)
     if category_data is None:
        raise CustomException(status.HTTP_404_NOT_FOUND, "Category not found")
     await db.commit()

     return category_data
   except CustomException:
     raise
   except Exception as e:
     await db.rollback()
     raise CustomException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to update category")

async def delete_category(db: AsyncSession, id: int):
   try:
     result =  await category.delete_category(db= db, id= id)

     if result.rowcount == 0:
        raise CustomException(status.HTTP_404_NOT_FOUND, "Category not found")
     await db.commit()

     return {
       'message': 'Category deleted successfully'
     }
   except CustomException:
     raise
   except Exception as e:
     await db.rollback()
     raise CustomException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to delete category")