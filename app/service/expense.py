from app.repository.expense import addExpenses, getExpenselist as fetchExpense, deleteExpense, updateExpense
from app.models.expenses import Expenses
from fastapi.responses import JSONResponse
from app.core.customException import CustomException
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from app.schema.expense import ExpenseDateFilter
from datetime import datetime, timedelta

async def addExpensesItem(db: AsyncSession, expenseData, userId: int):
    try:
      expense = Expenses(
          category_id=expenseData.category_id,
          amount=expenseData.amount,
          description=expenseData.description,
          payment_method=expenseData.payment_method,
          user_id=int(userId),
      )
      
      await addExpenses(db, expense)

      await db.commit()
      await db.refresh(expense)

      return {
          "id": expense.id,
          "amount": expense.amount,
          "description": expense.description,
      }
    except Exception as e:
        await db.rollback()
        print(f"Error creating Expense: {e}")
        raise CustomException(500, "Something went wrong") 

async def getExpenselist(userId: int, db: AsyncSession, limit: int, nextCursor: int|None, dateFilter: str):
   now = datetime.now()
   startDate, endDate = None, None
   if dateFilter == ExpenseDateFilter.PAST_WEEK:
       startDate = now - timedelta(days=7)
       endDate = now
   
   elif dateFilter == ExpenseDateFilter.PAST_MONTH:
       startDate = now - timedelta(days=30)
       endDate = now
   
   elif dateFilter == ExpenseDateFilter.LAST_3_MONTHS:
       startDate = now - timedelta(days=90)
       endDate = now
   
   result =  await fetchExpense(db= db, userId= userId, limit= limit, nextCursor=nextCursor,  startDate=startDate,endDate=endDate,)
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