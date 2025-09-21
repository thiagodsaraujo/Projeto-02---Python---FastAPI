from fastapi import APIRouter
from api.api_v1.handlers.user import user_router
from api.auth.jwt import auth_router
from api.api_v1.handlers import todo

# Aqui nessa classe criamos o roteador principal da API v1
# E então incluímos os roteadores específicos, como o de usuários

router = APIRouter()

router.include_router(
    user_router,
    prefix="/users", 
    tags=["users"])

router.include_router(
    auth_router,
    prefix="/auth",
    tags=["auth"])


router.include_router(
    todo.todo_router,
    prefix="/todo",
    tags=["todo"]
)