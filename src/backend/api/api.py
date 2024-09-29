from fastapi import APIRouter

from src.backend.api import *

router = APIRouter(
    prefix="/api",
)

router.include_router(AuthController.create_router())
