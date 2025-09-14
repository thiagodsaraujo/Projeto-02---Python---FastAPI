from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserAuth (BaseModel):
    email: EmailStr = Field(..., description="Email do usuário")
    username: str = Field(..., description="Nome de usuário")
    password: str = Field(..., min_length= 5, max_length= 20, description="Senha do usuário")
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    disabled: Optional[bool] = False

