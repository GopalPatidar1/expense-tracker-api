from app.repository.expense import add_expenses, get_expense_list as fetch_expense, delete_expense, update_expense
from app.models.expenses import Expenses
from fastapi.responses import JSONResponse
from app.core.customException import CustomException
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from app.schema.expense import ExpenseDateFilter
from datetime import datetime, timedelta

async def add_expenses_item(db: AsyncSession, expense_data, user_id: int):
    try:
      expense = Expenses(
          category_id=expense_data.category_id,
          amount=expense_data.amount,
          description=expense_data.description,
          payment_method=expense_data.payment_method,
          user_id= user_id,
      )
      
      await add_expenses(db, expense)

      await db.commit()
      await db.refresh(expense)

      return {
          "id": expense.id,
          "amount": expense.amount,
          "description": expense.description,
      }
    except Exception as e:
        await db.rollback()
        raise CustomException(500, "Something went wrong") 

async def get_expense_list(user_id: int, db: AsyncSession, limit: int, next_cursor: int|None, date_filter: ExpenseDateFilter | None):
   now = datetime.now()
   start_date, end_date = None, None
   if date_filter == ExpenseDateFilter.PAST_WEEK:
       start_date = now - timedelta(days=7)
       end_date = now
   
   elif date_filter == ExpenseDateFilter.PAST_MONTH:
       start_date = now - timedelta(days=30)
       end_date = now
   
   elif date_filter == ExpenseDateFilter.LAST_3_MONTHS:
       start_date = now - timedelta(days=90)
       end_date = now
   
   result =  await fetch_expense(db= db, user_id= user_id, limit= limit, next_cursor=next_cursor,  start_date=start_date,end_date= end_date,)
   next_cursor = result[-1].id if result else None
   avail_next = len(result) > limit
   return {"next_cursor": next_cursor, "avail_next":avail_next ,"result": result[:limit]}

async def delete_expense_item(db: AsyncSession, user_id: int, id: int):
   result = await delete_expense(db=db, user_id=user_id, id=id)

   if result.rowcount == 0:
      raise CustomException(404,"Expense not found") 
   
   return {
       'success': True
   }

async def update_expenses_item(db: AsyncSession, id: int, user_id: int, data,):
   result = await update_expense(db= db, id= id, user_id= user_id, data= data)

   if result is None:
      raise CustomException(404,"Expense not found") 

   await db.commit()
   
   return result