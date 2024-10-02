from fastapi import APIRouter
from .api import (AuthController, UserController, OrganisationController, InviteController, GithubController,
                  TelegramController)

router = APIRouter(
    prefix="/api",
)

router.include_router(AuthController.create_router())
router.include_router(UserController.create_router())
router.include_router(GithubController.create_router())
router.include_router(OrganisationController.create_router())
router.include_router(InviteController.create_router())
router.include_router(TelegramController.create_router())
