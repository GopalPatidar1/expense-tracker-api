# auth/permissions.py

from enum import Enum


class Permission(str, Enum):
    CATEGORY_READ = "category:read"
    CATEGORY_CREATE = "category:create"
    CATEGORY_UPDATE = "category:update"
    CATEGORY_DELETE = "category:delete"