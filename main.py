from fastapi import FastAPI
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import config
import firebase

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.get_allowed_origins(),
    allow_credentials=True,  # IMPORTANTE para cookies/auth tokens
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=[
        "Authorization",          # Token JWT do Firebase
        "Content-Type",
        "Accept",
        "Origin",
        "X-Requested-With",
        "X-CSRF-Token",
        "X-Firebase-AppCheck",    # Header específico do Firebase
        "X-Client-Version",
        "X-Firebase-Auth",        # Outro header comum do Firebase
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
    ],
    expose_headers=[
        "Content-Disposition",
        "X-Total-Count",
        "Content-Range"
    ],
    max_age=600,  # Cache de 10 minutos para preflight requests
)

# importação das rotas
from routes.environment import environment_router
from routes.auth import auth_router

app.include_router(environment_router)
app.include_router(auth_router)
