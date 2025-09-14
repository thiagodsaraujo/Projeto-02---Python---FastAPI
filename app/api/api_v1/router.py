from fastapi import APIRouter
from api.api_v1.handlers.user import user_router

# Aqui nessa classe criamos o roteador principal da API v1
# E então incluímos os roteadores específicos, como o de usuários

router = APIRouter()

router.include_router(
    user_router, 
    prefix="/users", 
    tags=["users"])
