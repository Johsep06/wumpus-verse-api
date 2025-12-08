from fastapi import FastAPI
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# Carregando variáveis de ambiente
load_dotenv()

FIREBASE_API_KEY = os.getenv('FIREBASE_API_KEY')

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'port': int(os.getenv('DB_PORT')),
    'name': os.getenv('DB_NAME')
}

# inicialização do FastAPI
app = FastAPI()

# cofiguração do cors para o frontend
origins = [
    'https://wumpus-verse-frontend.vercel.app/',
    'http://localhost:5173',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# importação das rotas
from routes.environment import environment_router
from routes.auth import auth_router

app.include_router(environment_router)
app.include_router(auth_router)
