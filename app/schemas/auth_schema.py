from pydantic import BaseModel
from uuid import UUID

# Este schema define como será a resposta de autenticação da API.
# Ele contém dois tokens:
# - access_token: Token JWT de acesso, geralmente de curta duração, usado para autenticar requisições.
# - refresh_token: Token de atualização, geralmente de longa duração, usado para obter novos access_tokens sem precisar fazer login novamente.
class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str

# Este schema representa o payload (conteúdo) de um JWT.
# - sub: Normalmente é o identificador do usuário (subject), aqui como UUID. Pode ser None.
# - exp: Timestamp de expiração do token (em segundos desde a época Unix). Pode ser None.
class TokenPayload(BaseModel):
    sub: UUID | None = None
    exp: int | None = None