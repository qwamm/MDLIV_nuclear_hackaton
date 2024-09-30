from fastapi import APIRouter
from .api import AuthController, UserController

router = APIRouter(
    prefix="/api",
)

router.include_router(AuthController.create_router())
router.include_router(UserController.create_router())
