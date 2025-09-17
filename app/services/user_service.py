from schemas.user_schema import UserAuth
from models.user_model import User
from core.security import get_password, verify_password
from typing import Optional




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

    # A função abaixo pega um usuário pelo email
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        # Sua assinatura recebe um email (string) e retorna um usuário (User) ou None
        return await User.find_one(User.email == email)
    
    @staticmethod
    async def authenticate(email: str, password: str) -> Optional[User]:
        """
        Autentica um usuário com base no e-mail e na senha fornecidos.

        Parâmetros:
        - email: E-mail do usuário a ser autenticado.
        - password: Senha fornecida pelo usuário.

        Retorno:
        - Retorna o objeto User se a autenticação for bem-sucedida; caso contrário, retorna None.
        """
        # Busca o usuário pelo e-mail fornecido
        user = await UserService.get_user_by_email(email)
        
        # Se o usuário não for encontrado, retorna None
        if not user:
            return None
        
        # Verifica se a senha fornecida corresponde ao hash armazenado
        if not verify_password(
            password=password,
            hashed_password=user.hash_password):
            return None  # Retorna None se a senha estiver incorreta
        
        # Retorna o objeto do usuário se a autenticação for bem-sucedida
        return user