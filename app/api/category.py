from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schema.category import CreateCategory
from app.service import category
from app.config.database import get_db

router = APIRouter(prefix="/catergory", tags=[
  'Category'
])

@router.get('/')
async def get_category(db: AsyncSession= Depends(get_db)):
  return await category.get_category(db)

@router.post('/')
async def create_category(data: CreateCategory, db: AsyncSession = Depends(get_db)):
  return await category.create_category(data=data, db=db)

@router.put('/{id}')
async def update_category(id: int, db: AsyncSession= Depends(get_db), data = CreateCategory):
  return await category.update_category(db= db,data= data, id=id)

@router.delete('/{id}')
async def delete_category(id: int, db: AsyncSession= Depends(get_db)):
  return await category.delete_category(db=db, id=id)
