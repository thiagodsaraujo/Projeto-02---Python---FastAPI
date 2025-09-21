from fastapi import APIRouter, HTTPException, status, Depends
from schemas.todo_schema import TodoCreate, TodoUpdate, TodoDetail
from models.user_model import User
from api.dependencies import get_current_user # Função de dependência para obter o usuário atual, autenticado

todo_router = APIRouter()

# Em java o código seria como abaixo:
# @RestController 
# @RequestMapping("/api/v1/todo")
@todo_router.get("/", summary="Listar tarefas (todos)", response_model=list[TodoDetail])
async def list_todos(current_user: User = Depends(get_current_user)):
    # Aqui você implementaria a lógica para listar as tarefas do usuário
    pass