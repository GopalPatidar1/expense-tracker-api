from fastapi import APIRouter, Request, Depends, status
from app.service import expense
from app.config.database import get_db
from app.schema.expense import ExpenseItem, UpdateExpenseItem,ExpenseResponse
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix='/expense', tags=[
    'Expense'
])

@router.get('/', response_model=ExpenseResponse)
async def getExpenselist(request: Request, db: AsyncSession = Depends(get_db), limit:int = 10, nextCursor: int | None=None, dateFilter:str|None=None):
    userId =  request.state.userId
    return await expense.getExpenselist(userId=userId, db=db, limit=limit, nextCursor=nextCursor, dateFilter= dateFilter)

@router.post('/', status_code=status.HTTP_201_CREATED)
async def addExpenseItem(request: Request, data: ExpenseItem, db: AsyncSession = Depends(get_db)):
    userId = request.state.userId
    return await expense.addExpensesItem(db, data, userId)

@router.put('/{id}')
async def updateExpenseItem(id: int, request: Request, item: UpdateExpenseItem, db: AsyncSession = Depends(get_db)):
    return await expense.updateExpensesItem(userId=request.state.userId, data=item, db=db, id=id)

@router.delete('/{id}')
async def deleteExpenseItem(id: int,request: Request, db: AsyncSession =Depends(get_db)):
    return await expense.deleteExpenseItem(id=id, db= db, userId= request.state.userId)

@router.get('/{id}')
def getExpenseItem(id: int):
    return {
        'id': id,
        'title': f'Expense item {id}',
        'completed': False
    }
