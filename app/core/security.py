from passlib.context import CryptContext


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