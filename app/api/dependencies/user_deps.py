from fastapi.security import OAuth2PasswordBearer
from core.config import settings
from fastapi import Depends, HTTPException, status
from models.user_model import User
from jose import JWTError, jwt
from schemas.auth_schema import TokenPayload
from datetime import datetime
from pydantic import ValidationError
from services.user_service import UserService


# Cria um esquema OAuth2 reutilizável para autenticação via JWT.
# - tokenUrl: URL do endpoint de login que gera o token.
# - scheme_name: nome do esquema de autenticação (aparece na documentação Swagger).
# o trecho de código abaixo cria uma instância de OAuth2PasswordBearer, que é uma classe fornecida pelo FastAPI para lidar com a autenticação OAuth2 usando o fluxo de senha (password flow). Essa instância é configurada para usar um endpoint específico para obter tokens de acesso.
# Em java, seria algo como:
# OAuth2PasswordBearer oauthReusavel = new OAuth2PasswordBearer("http://localhost:8000/api/v1/auth/login", "JWT");
oauth_reusavel = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login",
    scheme_name="JWT"
)

# Função de dependência para obter o usuário atual a partir do token JWT.
# - Recebe o token automaticamente via Depends(oauth_reusavel).
# - Decodifica o token, valida a assinatura e verifica expiração.
# - Se válido, retorna os dados do usuário (aqui só valida o token, não busca o usuário no banco).
async def get_current_user(token: str = Depends(oauth_reusavel)) -> User:
    try:
        # Decodifica o token JWT usando a chave secreta e o algoritmo definidos nas configurações.
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            settings.ALGORITHM
        )
        # Constrói o schema TokenPayload para validar e acessar os dados do token.
        token_data = TokenPayload(**payload)
        # Verifica se o token está expirado comparando o campo 'exp' com o horário atual.
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expirado",
                headers={"WWW-Authenticate": "Bearer"}
            )
    # Captura erros de validação do JWT ou do schema.
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não foi possível validar as credenciais",
            headers={"WWW-Authenticate": "Bearer"}
        )
        # Busca o usuário no banco de dados usando o ID do token.
    user = await UserService.get_user_by_id(token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user