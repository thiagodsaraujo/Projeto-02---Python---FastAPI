from fastapi import APIRouter, HTTPException, status, Depends
from schemas.todo_schema import TodoCreate, TodoDetail, TodoUpdate
from models.user_model import User
from api.dependencies.user_deps import get_current_user # Função de dependência para obter o usuário atual, autenticado
from services.todo_service import TodoService
from models.todo_model import Todo
from typing import List
from uuid import UUID



todo_router = APIRouter()

# Em java o código seria como abaixo:
# @RestController 
# @RequestMapping("/api/v1/todo")
@todo_router.get("/", summary="Listar tarefas (todos)", response_model=List[TodoDetail], status_code=status.HTTP_200_OK)
async def list_todos(current_user: User = Depends(get_current_user)):
    # Aqui você implementaria a lógica para listar as tarefas do usuário
    return await TodoService.list_todos(current_user)

@todo_router.post("/create", summary="Criar nova tarefa (todo)", response_model=Todo, status_code=status.HTTP_201_CREATED)
async def create_todo(data: TodoCreate, current_user: User = Depends(get_current_user)):
    return await TodoService.create_todo(current_user, data)


@todo_router.get(
    "/{todo_id}",  # Rota que espera um UUID como parâmetro na URL
    summary="Detalhar tarefa (todo) por ID",  # Resumo para documentação OpenAPI
    response_model=TodoDetail,  # Modelo de resposta (serialização e documentação)
    status_code=status.HTTP_200_OK  # Código de status padrão para sucesso
)
async def detail(
    todo_id: UUID,  # ID da tarefa a ser detalhada, extraído da URL
    current_user: User = Depends(get_current_user)  # Usuário autenticado, obtido via dependência
):
    """
    Recupera os detalhes de uma tarefa específica do usuário autenticado.

    Parâmetros:
        todo_id (UUID): O identificador único da tarefa.
        current_user (User): O usuário autenticado, injetado automaticamente.

    Retorna:
        TodoDetail: Detalhes da tarefa, caso encontrada.

    Erros:
        404: Se a tarefa não for encontrada ou não pertencer ao usuário.
    """
    # Busca a tarefa pelo ID e pelo usuário dono
    todo = await TodoService.detail(current_user, todo_id)
    
    # Se não encontrar, retorna erro 404
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada"
        )
    # Retorna os detalhes da tarefa encontrada
    return todo

@todo_router.patch(
    "/{todo_id}",
    summary="Atualizar tarefa (todo) por ID",
    response_model=TodoDetail,
    status_code=status.HTTP_200_OK)
async def update(
    todo_id: UUID,
    data: TodoUpdate,
    current_user: User = Depends(get_current_user)
):
    """
    Atualiza uma tarefa existente pelo seu ID.

    Parâmetros:
    - todo_id (UUID): ID da tarefa a ser atualizada (vem da URL).
    - data (TodoUpdate): Dados novos para atualizar a tarefa (vem do corpo da requisição).
    - current_user (User): Usuário autenticado, obtido via dependência.

    Retorna:
    - TodoDetail: Detalhes da tarefa atualizada.

    Erros:
    - 404: Se a tarefa não for encontrada.
    """
    updated_todo = await TodoService.update(current_user, todo_id, data)
    if not updated_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada"
        )
    return updated_todo
# ...existing code...


@todo_router.delete(
    "/{todo_id}",
    summary="Deletar tarefa (todo) por ID",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete(
    todo_id: UUID,  # Recebe o ID da tarefa como parâmetro da rota
    current_user: User = Depends(get_current_user)  # Injeta o usuário autenticado usando Depends
):
    """
    Delete a todo item by its ID.
    Args:
       - todo_id (UUID): The unique identifier of the todo item to delete.
       - current_user (User, optional): The currently authenticated user, injected by dependency.
    Raises:
       - HTTPException: If the todo item is not found, raises 404 Not Found.
    Returns:
       - None: Returns HTTP 204 No Content on successful deletion.
    """
    # Chama o serviço para deletar a tarefa, passando o usuário atual e o ID da tarefa
    deleted = await TodoService.delete(current_user, todo_id)

    # Se a tarefa não foi encontrada ou não pôde ser deletada
    if not deleted:
        # Lança uma exceção HTTP 404 (não encontrado) com uma mensagem personalizada
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada"
        )
    # Retorna None explicitamente, indicando sucesso (HTTP 204 No Content)
    return None