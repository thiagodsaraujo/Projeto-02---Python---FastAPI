from beanie import Document, Indexed
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime




class User(Document):
    user_id: UUID = Field(default_factory=uuid4)
    username: Indexed(str, unique=True)
    email: Indexed(EmailStr, unique=True)
    hash_password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    disabled: Optional[bool] = None


    # O método __repr__ deve retornar uma representação não ambígua do objeto.
    def __repr__(self) -> str:
        return f"<User {self.email}>"
    
    # O método __str__ deve retornar uma representação legível do objeto.
    def __str__(self) -> str:
        return self.email

    # O método __hash__ deve usar um atributo imutável e único.
    # Serve para que possamos usar instâncias de User em sets ou como chaves em dicionários.
    def __hash__(self) -> int:
        return hash(self.emai)
    
    # O método __eq__ deve comparar atributos que definem a identidade do objeto.
    def __eq__(self, other: object) -> bool:
        if isinstance(other, User):
            return self.email == other.email
        return False
    
    # A propriedade create retorna a data de criação do usuário, 
    # baseada no tempo de geração do ID.
    @property
    def create(self) -> datetime:
        return self.id.generation_time
    
    # A função by_email é um método de classe que retorna um usuário com base no email fornecido.
    @classmethod
    async def by_email(self, email: str) -> "User":
        return await self.find_one(self.email == email)