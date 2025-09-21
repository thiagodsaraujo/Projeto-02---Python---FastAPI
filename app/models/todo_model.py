from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4
from beanie import Document, Indexed, before_event, Link, Replace, Insert
from pydantic import Field
from .user_model import User
from pydantic import BaseModel


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[bool] = None
    # Todos os campos devem ser opcionais para permitir atualizações parciais

class Todo(Document):
    todo_id: UUID = Field(default_factory=uuid4, description="Identificador único do todo")
    status: bool = False
    title: Indexed(str)
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    update_at: datetime = Field(default_factory=datetime.utcnow)
    owner: Link[User] # Em Java(Spring), seria @ManyToOne




    def __repr__(self) -> str:
        """
        Representação “oficial” do objeto.
        
        Finalidade:
        - Fornecer uma string detalhada e não ambígua útil para debugging e logs.
        - Idealmente deve conter informação suficiente para identificar o objeto (ex.: ID e campos importantes).
        
        Exemplo de uso:
        >>> todo = Todo(title='Comprar pão', status=False)
        >>> repr(todo)
        \"Todo(todo_id=..., title=Comprar pão, status=False)\"
        """
        return f"Todo(todo_id={self.todo_id}, title={self.title}, status={self.status})"

    def __str__(self) -> str:
        """
        Representação legível do objeto.

        Em java seria algo como toString()

        Finalidade:
        - Texto curto e agradável para ser exibido ao usuário.
        - Usado por print(obj) e str(obj).
        
        Exemplo de uso:
        >>> print(todo)
        Comprar pão
        """
        return self.title

    def __hash__(self) -> int:
        """
        Valor hash do objeto.

        # Em java seria algo como hashCode()

        Finalidade:
        - Permitir que instâncias de Todo sejam usadas em sets ou como chaves de dicionários.
        - O hash deve ser baseado em atributos imutáveis que definem a identidade do objeto.
          Aqui usamos `todo_id`, que é único por tarefa.
        
        Observações:
        - Se __eq__ for definido, __hash__ também deve ser definido para manter a consistência
          (objetos iguais devem ter o mesmo hash).
        """
        return hash(self.todo_id)

    def __eq__(self, other: object) -> bool:
        """
        Verifica igualdade entre dois objetos Todo.

        # Em java seria algo como equals()

        Finalidade:
        - Determinar se duas instâncias representam a mesma entidade.
        - Compara o `todo_id`, que é o identificador único da tarefa.

        Retorna:
        - True se `other` for uma instância de Todo e tiver o mesmo todo_id; caso contrário, False.
        """
        if isinstance(other, Todo):
            return self.todo_id == other.todo_id
        return False

# A função abaixo é
# um "hook" que atualiza o campo `update_at` sempre que o documento é atualizado ou inserido.
# Em java, seria algo como um @PreUpdate ou @PrePersist.
@before_event(Replace, Insert)
def sync_updated_at(todo: Todo):
    todo.update_at = datetime.utcnow()