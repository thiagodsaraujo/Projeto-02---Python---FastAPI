from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any
from services.user_service import UserService
from core.security import create_access_token, create_refresh_token



auth_router = APIRouter()

@auth_router.post("/login")
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
