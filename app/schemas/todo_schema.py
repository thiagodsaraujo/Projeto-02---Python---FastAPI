from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

# Modelo para criação de uma nova tarefa (todo)
class TodoCreate(BaseModel):
    # Título da tarefa, obrigatório, entre 3 e 50 caracteres
    title: str = Field(
        ..., 
        description="Título da tarefa", 
        min_length=3, 
        max_length=50
    )
    # Descrição detalhada da tarefa, opcional, entre 3 e 500 caracteres se fornecida
    description: Optional[str] = Field(
        None, 
        description="Descrição detalhada da tarefa", 
        min_length=3, 
        max_length=500
    )
    # Status da tarefa, opcional, padrão é False (não concluída)
    status: Optional[bool] = False

# Modelo para atualização de uma tarefa existente
class TodoUpdate(BaseModel):
    # Título pode ser atualizado, mas não é obrigatório
    title: Optional[str]
    # Descrição pode ser atualizada, mas não é obrigatória
    description: Optional[str]
    # Status pode ser atualizado, padrão é False se não fornecido
    status: Optional[bool] = False

# Modelo para detalhamento/retorno de uma tarefa
class TodoDetail(BaseModel):
    # Identificador único da tarefa
    todo_id: UUID
    # Título da tarefa
    title: str
    # Descrição detalhada, pode ser nula
    description: Optional[str]
    # Status da tarefa (True para concluída, False para pendente)
    status: bool
    # Data de criação da tarefa
    created_at: datetime
    # Data da última atualização da tarefa
    update_at: datetime
    # Identificador do dono/usuário da tarefa
    owner_id: UUID

    # Configuração para permitir conversão de ORM para modelo Pydantic
    class Config:
        orm_mode = True