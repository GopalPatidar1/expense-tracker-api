from app.repository.expense import addExpenses, getExpenselist as fetchExpense, deleteExpense, updateExpense
from app.models.expenses import Expenses
from fastapi.responses import JSONResponse
from app.core.customException import CustomException
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio

async def addExpensesItem(db: AsyncSession, expenseData, userId: int):
    try:
      expense = Expenses(
          task=expenseData.task,
          desc=expenseData.desc,
          user_id=int(userId),
      )
      
      await addExpenses(db, expense)

      await db.commit()
      await db.refresh(expense)

      return {
          "id": expense.id,
          "task": expense.task,
      }
    except Exception as e:
        await db.rollback()
        print(f"Error creating Expense: {e}")
        raise CustomException(500, "Something went wrong") 

async def getExpenselist(userId: int, db: AsyncSession, limit: int, nextCursor: int|None):
   result =  await fetchExpense(db= db, userId= userId, limit= limit, nextCursor=nextCursor)
   nextCursor = result[-1].id if result else None
   availNext = len(result) > limit
   return {"nextCursor": nextCursor, "availNext":availNext ,"result": result[:limit]}

async def deleteExpenseItem(db: AsyncSession, userId: int, id: int):
   result = await deleteExpense(db=db, userId=userId, id=id)

   if result.rowcount == 0:
      raise CustomException(404,"Expense not found") 
   
   return {
       'success': True
   }

async def updateExpensesItem(db: AsyncSession, id: int, userId: int, data,):
   result = await updateExpense(db= db, id= id, userId= userId, data= data)

   if result is None:
      raise CustomException(404,"Expense not found") 

   await db.commit()
   
   return result