from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import jwt
from app.api import auth, user, category, expense
from app.core.customException import CustomException
from app.config.secretes import secretes

JWT_SECRET_KEY = secretes.JWT_SECRET_KEY
JWT_ALGORITHM = secretes.JWT_ALGORITHM

app = FastAPI()

@app.middleware("http")
async def validateAuth(request, call_next):
    publicRoutes = [
        '/docs',
        '/openapi.json',
        '/redoc',
        '/health',
        '/auth/login',
        '/auth/register',
        '/logout'
    ]
    if request.url.path not in publicRoutes:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
           try: 
              encoded_jwt = auth_header.split(" ", 1)[1]
              decodeJwt = jwt.decode(encoded_jwt, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
              request.state.userId = int(decodeJwt["userId"])
           except:
               return JSONResponse(status_code=401, content={
                   'detail': 'Token Expired'
               },)
               
        else:
            return JSONResponse(status_code=401, content={
                'detail': 'Invalid or missing token'
            },)
    response = await call_next(request)
    return response


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(category.router)
app.include_router(expense.router)

@app.get("/health")
async def read_root():
    return {
        'Hello': 'World'
    }

@app.exception_handler(CustomException)
async def global_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'error': exc.message
        }
    )