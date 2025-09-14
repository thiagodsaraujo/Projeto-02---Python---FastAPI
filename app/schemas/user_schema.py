from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID
from typing import Optional


# User para quando enviar a requisição de criação de usuário
# Não armazenamos a senha em texto puro, apenas o hash
# Por isso, usamos o campo 'password' aqui, que será convertido em hash antes de salvar no banco
class UserAuth (BaseModel):
    email: EmailStr = Field(..., description="Email do usuário")
    username: str = Field(..., description="Nome de usuário", min_length=3, max_length=20)
    password: str = Field(..., min_length= 5, max_length= 20, description="Senha do usuário")
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    disabled: Optional[bool] = False


# Essa classe é usada para retornar detalhes do usuário, sem expor a senha
class UserDetail(BaseModel):
    user_id: UUID
    email: EmailStr
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    disabled: Optional[bool] = False


# ORM = Object-Relational Mapping
# ODM = Object-Document Mapping (usado em bancos NoSQL como MongoDB)