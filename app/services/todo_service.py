from models.user_model import User
from models.todo_model import Todo
from typing import List
from schemas.todo_schema import TodoCreate


class TodoService:


    @staticmethod
    async def list_todos(user: User) -> List[Todo]:
        """
        Lista todas as tarefas (todos) de um usuário específico.

        :param user: Instância do usuário autenticado.
        :return: Lista de instâncias de Todo pertencentes ao usuário.
        """
        todos = await Todo.find(Todo.owner.id == user.id).to_list()
        return todos