# auth/authorization.py

from fastapi import Depends, HTTPException, status, Request

from app.auth.permissions import Permission
from app.repository.user import getUserById
from app.config.database import get_db

ROLE_PERMISSIONS = {
    "user": {
        Permission.CATEGORY_READ,
    },

    "admin": {
        Permission.CATEGORY_READ,
        Permission.CATEGORY_CREATE,
        Permission.CATEGORY_UPDATE,
        Permission.CATEGORY_DELETE,
    },
}

async def get_current_user(request: Request, db=Depends(get_db)):
    return await getUserById(db, request.state.user_id)

def require_permission(permission: Permission):
    async def checker(current_user=Depends(get_current_user)):
        user_permissions = ROLE_PERMISSIONS.get(current_user.role, set())
        if permission not in user_permissions:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
        return current_user
    return checker