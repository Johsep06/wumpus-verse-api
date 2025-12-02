from fastapi import FastAPI
import os
from dotenv import load_dotenv

# Carregando variáveis de ambiente
load_dotenv()

FIREBASE_API_KEY = os.getenv('FIREBASE_API_KEY')

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'port': int(os.getenv('DB_PORT')),
    'name':os.getenv('DB_NAME')
}

# inicialização do FastAPI
app = FastAPI()

# importação das rotas
from routes.environment import environment_router
from routes.auth import auth_router

app.include_router(environment_router)
app.include_router(auth_router)