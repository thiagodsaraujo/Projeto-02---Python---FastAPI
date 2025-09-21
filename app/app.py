from fastapi import FastAPI
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from core.config import settings

from models.user_model import User  # Importe seus modelos aqui
from api.api_v1.router import router
from models.todo_model import Todo



app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

@app.on_event("startup")
async def app_init():
    """
    Inicializa a aplicação FastAPI, conectando ao MongoDB e configurando o Beanie.
    """
    # Cria uma instância do cliente MongoDB
    client = AsyncIOMotorClient(
        settings.MONGO_CONNECTION_STRING).todoapp
    
    # Inicializa o Beanie com a conexão do MongoDB e os modelos definidos
    await init_beanie(database = client, 
                      document_models=[
                            # Adicione seus modelos de documento aqui
                            # Exemplo: User, Item, etc.
                            User,
                            Todo
                      ]
                      
                      
        )
    

# Abaixo, incluímos o roteador da API versão 1
app.include_router(
    router,
    prefix=settings.API_V1_STR,
)