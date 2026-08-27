from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schema.category import CreateCategory
from app.service import category
from app.config.database import get_db

router = APIRouter(prefix="/catergory", tags=[
  'Category'
])

@router.get('/')
async def getCategory(db: AsyncSession= Depends(get_db)):
  return await category.getCategory(db)

@router.post('/')
async def createCategory(data: CreateCategory, db: AsyncSession = Depends(get_db)):
  return await category.createCategory(data=data, db=db)

@router.put('/{id}')
async def updateCategory(id: int, db: AsyncSession= Depends(get_db), data = CreateCategory):
  return await category.updateCategory(db= db,data= data, id=id)

@router.delete('/{id}')
async def deleteCategory(id: int, db: AsyncSession= Depends(get_db)):
  return await category.deleteCategory(db=db, id=id)
