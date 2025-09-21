from fastapi import APIRouter, HTTPException, status, Depends
from schemas.user_schema import UserAuth, UserDetail
from services.user_service import UserService
import pymongo
from models.user_model import User
from api.dependencies.user_deps import get_current_user


user_router = APIRouter()


@user_router.get("/test")
async def test():
    return {"message": "User router is working!"}


@user_router.post("/create", summary="Create a new user", response_model=UserDetail)
async def create_user(data:UserAuth):
    try:
        return await UserService.create_user(data)
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists."
        )
    


@user_router.get("/me", summary="Get current user details", response_model=UserDetail)
async def get_me(user: User = Depends(get_current_user)):
    """
    Endpoint para obter os detalhes do usuário autenticado atualmente.

    Parâmetros:
    - user: Objeto do tipo User, injetado automaticamente pelo FastAPI através do Depends(get_current_user).
      O Depends é um recurso do FastAPI que permite a injeção de dependências. 
      
      Neste caso, ele executa a função get_current_user, que valida o token JWT enviado na requisição,
      decodifica o token, busca o usuário no banco de dados e retorna o objeto User correspondente.
      Se o token for inválido ou o usuário não existir, uma exceção HTTP é lançada automaticamente.
      Se fosse no Java, o Depends seria algo como um @Autowired ou @Inject, que injeta a dependência necessária.

    Retorno:
    - Um objeto UserDetail (Pydantic), que contém apenas os dados públicos do usuário (sem senha).

    Exemplo de uso do Depends:
    - O FastAPI executa get_current_user antes de executar o endpoint, e injeta o resultado no parâmetro 'user'.
    - Isso facilita a proteção de rotas e o acesso ao usuário autenticado sem precisar repetir código de validação em cada endpoint.
    """
    return UserDetail.from_orm(user)
