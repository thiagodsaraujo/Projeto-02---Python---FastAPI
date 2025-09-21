from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any
from services.user_service import UserService
from core.security import create_access_token, create_refresh_token
from schemas.auth_schema import TokenSchema
from schemas.user_schema import UserDetail
from models.user_model import User
from api.dependencies.user_deps import get_current_user
from pydantic import ValidationError
from core.config import settings
from schemas.auth_schema import TokenPayload
from jose import jwt



auth_router = APIRouter()


@auth_router.post("/login", summary="Criação de token JWT e Refresh Token", response_model=TokenSchema)
# Os paramentros do /login. O summary aparece na documentação automática (Swagger UI). e response_model define o schema de resposta
async def login(
    data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Endpoint de autenticação (login).
    
    Fluxo:
    1. Recebe credenciais via formulário (application/x-www-form-urlencoded) no padrão OAuth2 Password.
    2. Obtém os campos: username e password (padrão do OAuth2PasswordRequestForm).
    3. Interpreta 'username' como e-mail (caso você esteja usando e-mail para login).
    4. Chama o serviço de autenticação.
    5. Retorna erro 401 se falhar; caso sucesso, retorna dados básicos (provisório).

    IMPORTANTE:
    OAuth2PasswordRequestForm NÃO fornece 'email' por padrão.
    Use data.username como e-mail OU crie uma classe customizada se quiser data.email.

    Próximo passo recomendado:
    - Gerar um token JWT (access_token + token_type).
    - Possivelmente incluir refresh token.
    """
    # Usa 'email' a partir de username ou de um possível atributo 'email'
    # (caso você tenha estendido a classe).
    email = getattr(data, "email", data.username)

    # Autentica o usuário (deve validar senha e retornar objeto usuário ou None).
    usuario = await UserService.authenticate(
        email=email,
        password=data.password
    )

    # Se não autenticou, retorna 401.
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas - E-mail ou senha incorretos",
        )

    return {
        "access_token": create_access_token(usuario.user_id),
        "refresh_token": create_refresh_token(usuario.user_id),
    }

@auth_router.post("/test-token", summary="Testa o token JWT", response_model=UserDetail)
async def test_token(user: User = Depends(get_current_user)):
    """
    Endpoint de teste para verificar a validade do token JWT.
    
    Fluxo:
    1. Recebe o token automaticamente via Depends(get_current_user).
    2. Se o token for válido, retorna os dados do usuário.
    3. Se inválido, retorna erro 401 ou 403 conforme o caso.

    IMPORTANTE:
    Este endpoint é útil para testar se o token JWT está funcionando corretamente.
    Ele depende da função get_current_user que valida o token e busca o usuário no banco.
    """
    return UserDetail.from_orm(user)

@auth_router.post("/refresh", summary="Refresh Token", response_model=TokenSchema)
async def refresh_token(refresh_token: str = Body(...)):
    try:
        payload = jwt.decode(
            refresh_token,
            settings.JWT_REFRESH_SECRET_KEY,
            settings.ALGORITHM
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Refresh token inválido ou expirado.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    user = await UserService.get_user_by_id(token_data.sub)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return {
        "access_token": create_access_token(user.user_id),
        "refresh_token": create_refresh_token(user.user_id)
    }