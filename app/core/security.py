from passlib.context import CryptContext
from typing import Any,Union, Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from core.config import settings


# Abaixo, configuramos o contexto de criptografia para senhas
# Usamos o algoritmo bcrypt, que é seguro e amplamente utilizado
password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def get_password(password: str) -> str:
    """
    Gera um hash seguro para a senha fornecida.
    """
    return password_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verifica se a senha fornecida corresponde ao hash armazenado.
    """
    return password_context.verify(password, hashed_password)

def create_access_token(
    subject: Union[str, Any],
    expires_delta: Optional[Union[int, timedelta]] = None
) -> str:
    """
    Cria e assina um JWT (JSON Web Token) com expiração.

    Parâmetros:
    - subject: identificador do "dono" do token (ex.: id do usuário). Será convertido para string e
      colocado na claim 'sub' do JWT.
    - expires_delta:
        - timedelta: define diretamente a duração do token.
        - int: interpretado como quantidade de minutos.
        - None: usa o valor padrão settings.ACCESS_TOKEN_EXPIRE_MINUTES.

    Retorno:
    - Uma string com o token JWT assinado.

    Observações:
    - O token contém as claims:
        - sub: subject (string)
        - iat: instante de emissão (UTC)
        - exp: instante de expiração (UTC)
    - A assinatura usa settings.JWT_SECRET_KEY e settings.ALGORITHM.
    """
    # Determina a duração do token a partir do parâmetro recebido ou da configuração padrão.
    if expires_delta is not None:
        delta = timedelta(minutes=expires_delta)
    else:
        delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    issued_at = datetime.utcnow()
    expires_at = issued_at + delta

    # Claims do JWT
    info_jwt = {
        "sub": str(subject),  # assunto do token (ex.: id do usuário)
        "iat": issued_at,     # instante de emissão
        "exp": expires_at     # instante de expiração
    }

    # Assina o token com a chave secreta e algoritmo definidos nas configurações
    jwt_encoded = jwt.encode(
        info_jwt,
        settings.JWT_SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return jwt_encoded

def create_refresh_token(
    subject: Union[str, Any],
    expires_delta: Optional[Union[int, timedelta]] = None
) -> str:

    # Determina a duração do token a partir do parâmetro recebido ou da configuração padrão.
    if expires_delta is not None:
        delta = timedelta(minutes=expires_delta)
    else:
        delta = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    issued_at = datetime.utcnow()
    expires_at = issued_at + delta

    # Claims do JWT
    info_jwt = {
        "sub": str(subject),  # assunto do token (ex.: id do usuário)
        "iat": issued_at,     # instante de emissão
        "exp": expires_at     # instante de expiração
    }

    # Assina o token com a chave secreta e algoritmo definidos nas configurações
    jwt_encoded = jwt.encode(
        info_jwt,
        settings.JWT_REFRESH_SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return jwt_encoded