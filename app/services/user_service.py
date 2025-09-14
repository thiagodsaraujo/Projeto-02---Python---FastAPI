from schemas.user_schema import UserAuth
from models.user_model import User
from core.security import get_password




# Aqui você pode adicionar funções relacionadas a usuários, como criação, autenticação, etc.
# Os services em geral contêm a lógica de negócio da aplicação.


class UserService:
    @staticmethod
    async def create_user(user: UserAuth):
        usuario = User(
            username=user.username,
            email=user.email,
            hash_password=get_password(user.password),
            first_name=user.first_name,
            last_name=user.last_name,
            disabled=user.disabled
        )
        await usuario.save()
        return usuario