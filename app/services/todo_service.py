from models.user_model import User
from models.todo_model import Todo
from typing import List, Optional
from schemas.todo_schema import TodoCreate, TodoUpdate
from uuid import UUID


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
    
    @staticmethod
    async def create_todo(user: User, data: TodoCreate) -> Todo:
        """
        Cria uma nova tarefa (todo) para um usuário específico.

        :param user: Instância do usuário autenticado.
        :param data: Dados para criar a nova tarefa (título, descrição, etc).
        :return: A instância de Todo recém-criada.
            """
        # Cria uma nova instância de Todo usando os dados fornecidos (data) e define o proprietário (owner) como o usuário atual.
        # O método model_dump() converte o objeto 'data' (Pydantic model) em um dicionário, 
        # permitindo a expansão dos campos como argumentos nomeados (**kwargs) para o construtor de Todo.
        # Em java, seria algo como new Todo(data.getTitle(), data.getDescription(), user)
        # Porém, em Python, usamos o unpacking com **data.model_dump() para passar todos os campos de uma vez.
        # Os dois ** servem para "desempacotar" o dicionário retornado por data.model_dump() 
        # e passar seus pares chave-valor como argumentos nomeados para o construtor de Todo.
        todo = Todo(**data.model_dump(), owner=user)

        # Insere o novo objeto Todo no banco de dados de forma assíncrona.
        # O método insert() salva o documento na coleção correspondente e retorna a própria instância já persistida.
        return await todo.insert()
    
    @staticmethod
    async def detail(user: User, todo_id: UUID) -> Optional[Todo]:
        """
        Recupera uma tarefa (todo) pelo seu ID e pelo usuário dono.

        Parâmetros:
            user (User): O usuário solicitante.
            todo_id (UUID): O ID da tarefa a ser recuperada.

        Retorna:
            Todo | None: A instância de Todo correspondente ao ID e usuário, ou None se não encontrada.

        Observação:
            Garante que o usuário só possa acessar tarefas que lhe pertencem.
        """
        # Busca a tarefa pelo ID e pelo dono
        todo = await Todo.find_one(
            Todo.todo_id == todo_id,
            Todo.owner.id == user.id
        )
        return todo
    
    @staticmethod
    async def update(user: User, todo_id: UUID, data: TodoUpdate):
        """
        Atualiza uma tarefa (todo) existente de um usuário.

        Parâmetros:
            user (User): Usuário solicitante.
            todo_id (UUID): ID da tarefa a ser atualizada.
            data (TodoUpdate): Dados com os campos a serem atualizados.

        Retorna:
            Todo: A tarefa atualizada.

        Fluxo:
            1. Busca a tarefa pelo ID e usuário.
            2. Atualiza apenas os campos fornecidos em 'data'.
            3. Salva e retorna a tarefa atualizada.
        """
        # Busca a tarefa existente
        todo = await TodoService.detail(user, todo_id)
        if not todo:
            return None
        # Atualiza os campos informados
        await todo.update({
            "$set": data.model_dump(exclude_unset=True)
        })
        # Salva as alterações no banco
        await todo.save()
        # Retorna a tarefa atualizada
        return todo

    @staticmethod
    async def delete(user: User, todo_id: UUID) -> bool:
        """
        Exclui uma tarefa (todo) existente de um usuário.

        Parâmetros:
            user (User): Usuário solicitante.
            todo_id (UUID): ID da tarefa a ser excluída.

        Retorna:
            bool: True se deletado com sucesso

        Fluxo:
            1. Busca a tarefa pelo ID e usuário.
            2. Exclui a tarefa se encontrada.
        """
        # Busca a tarefa existente
        todo = await TodoService.detail(user, todo_id)
        if not todo:
            return False
        # Exclui a tarefa do banco de dados
        await todo.delete()
        return True

        