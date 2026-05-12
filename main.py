from fastapi import FastAPI, Request
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

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

limiter = Limiter(key_func=get_remote_address, default_limits=["10/minute"])

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# importação das rotas
from routes.environment import environment_router
from routes.auth import auth_router
from routes.agents import agents_router
from routes.execution import execution_router

app.include_router(environment_router)
app.include_router(auth_router)
app.include_router(agents_router)
app.include_router(execution_router)
