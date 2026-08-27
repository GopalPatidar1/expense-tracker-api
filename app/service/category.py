from app.repository import category 
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.customException import CustomException
from fastapi import status
from app.models.expenseCategories import ExpenseCategories

async def createCategory(data, db: AsyncSession):
    try:
     categoryData = ExpenseCategories(
       category=data.category
     )

     await category.createCategory(db=db, data=categoryData)

     await db.commit()
     await db.refresh(categoryData)
 
     return {"id":categoryData.id}

    except Exception as e:
     await db.rollback()
     raise CustomException(status.HTTP_422_UNPROCESSABLE_CONTENT)

async def getCategory(db:AsyncSession):
  try:
    await category.getCategory(db)
  except Exception as e:
    await db.rollback()
    raise CustomException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to fetch categories")

async def updateCategory(db: AsyncSession, id: int, data):
   try:
     categoryData =  await category.updateCategory(db=db, data=data, id=id)
     if categoryData is None:
        raise CustomException(status.HTTP_404_NOT_FOUND, "Category not found")
     await db.commit()
   except CustomException:
     raise
   except Exception as e:
     await db.rollback()
     raise CustomException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to update category")

async def deleteCategory(db: AsyncSession, id: int, data):
   try:
     result =  await category.deleteCategory(db= db, id= id)

     if result.rowcount == 0:
        raise CustomException(status.HTTP_404_NOT_FOUND, "Category not found")
     await db.commit()

     return {"message": "Category deleted successfully"}
   except CustomException:
     raise
   except Exception as e:
     await db.rollback()
     raise CustomException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to delete category")