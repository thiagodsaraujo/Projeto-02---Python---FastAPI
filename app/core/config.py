from typing import List
from decouple import config
from pydantic import AnyHttpUrl, BaseSettings


class Settings(BaseSettings):
    # Prefixo para as rotas da API versão 1
    API_V1_STR: str = "/api/v1"
    
    # Chave secreta usada para gerar tokens JWT
    JWT_SECRET_KEY: str = config("JWT_SECRET_KEY")
    
    # Chave secreta usada para gerar tokens JWT de refresh
    JWT_REFRESH_SECRET_KEY: str = config("JWT_REFRESH_SECRET_KEY", cast=str)
    
    # Nome do projeto, vindo do arquivo de configuração (.env)
    PROJECT_NAME: str = config("TODO-AUTH")
    
    # Algoritmo usado para assinar os tokens JWT, padrão HS256
    ALGORITHM: str = config("ALGORITHM", default="HS256")
    
    # Tempo de expiração do token de acesso (em minutos)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Tempo de expiração do token de refresh (em minutos) - 7 dias
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30 * 7 # 7 dias
    
    # Lista de origens permitidas para CORS (Cross-Origin Resource Sharing)
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    
    # String de conexão com o banco de dados MongoDB
    MONGO_CONNECTION_STRING: str = config("MONGO_CONNECTION_STRING", cast=str)

    class Config:
        # Define se os nomes dos campos são sensíveis a maiúsculas/minúsculas
        case_sensitive = True

# Instância única das configurações
# Pode ser importada e usada em toda a aplicação
settings = Settings()