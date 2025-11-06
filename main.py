from fastapi import FastAPI

# inicialização do FastAPI
app = FastAPI()

# importação das rotas
from routes.environment import environment_router

app.include_router(environment_router)