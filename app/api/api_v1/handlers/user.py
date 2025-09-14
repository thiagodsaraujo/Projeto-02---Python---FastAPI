from fastapi import APIRouter, HTTPException, status
from schemas.user_schema import UserAuth
from services.user_service import UserService
import pymongo


user_router = APIRouter()


@user_router.get("/test")
async def test():
    return {"message": "User router is working!"}


@user_router.post("/create", summary="Create a new user")
async def create_user(data:UserAuth):
    try:
        return await UserService.create_user(data)
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists."
        )
