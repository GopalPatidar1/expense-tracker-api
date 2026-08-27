from fastapi import APIRouter,Depends
from app.service import auth
from app.config.database import get_db
from app.schema.users import CreateUser, UserLogin
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix='/auth', tags=[
    'Authentication'
])

@router.post('/login')
async def login(request: UserLogin, db: AsyncSession= Depends(get_db)):
    return await auth.userLogin(request, db)
    
@router.post('/register')
async def registerUser(request: CreateUser, db: AsyncSession = Depends(get_db)):
    return await auth.registerUser(request, db)