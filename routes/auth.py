from fastapi import APIRouter, HTTPException, Depends, status
from firebase_admin.exceptions import FirebaseError
from firebase_admin import exceptions
from datetime import datetime
import requests
from sqlalchemy.orm import Session

from firebase import firebase_auth
from schemas import UserCreateSchemas, TokenSchemas, UserLoginSchemas, UserSchemas
from main import FIREBASE_API_KEY
from dependencies import get_session, check_token
from models import User

auth_router = APIRouter(prefix="/auth", tags=["authentication"])


def create_token(uid: str, email: str, name: str):
    # 4. Gerar token customizado
    custom_token = firebase_auth.create_custom_token(uid)

    if isinstance(custom_token, bytes):
        access_token = custom_token.decode('utf-8')
    else:
        access_token = custom_token

    token_response = TokenSchemas(
        access_token=access_token,
        token_type="bearer",
        user={
            'email': email,
            'name': name,
            'created_at': datetime.now(),
        }
    )

    return token_response


def authenticate_firebase_user(password: str, email: str):
    # 1. Autenticar com Firebase REST API
    auth_payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    response = requests.post(
        f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}",
        json=auth_payload
    )

    auth_result = response.json()

    if response.status_code != 200:
        error_message = auth_result.get('error', {}).get(
            'message', 'Erro de autenticação')
        print(f"❌ Erro de autenticação: {error_message}")

        if "INVALID_LOGIN_CREDENTIALS" in error_message:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Falha na autenticação"
            )

    return auth_result['localId']


@auth_router.post("/register", response_model=TokenSchemas, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreateSchemas, session: Session = Depends(get_session)):
    """
    Registra um novo usuário no sistema

    - **email**: Email válido do usuário
    - **password**: Senha (mínimo 6 caracteres)
    - **name**: Nome completo do usuário
    """
    try:
        print(f"📝 Tentativa de registro para: {user_data.email}")

        # 1. Criar usuário no Firebase Authentication
        user = firebase_auth.create_user(
            email=user_data.email,
            password=user_data.password,
            display_name=user_data.name,
            email_verified=False
        )

        print(f"✅ Usuário criado no Auth: {user.uid}")

        # 2. Salvar dados adicionais no Firestore (APÓS ATIVAR A API)
        user_profile = {
            'uid': user.uid,
            'email': user_data.email,
            'name': user_data.name,
            'created_at': datetime.now(),
            'updated_at': datetime.now(),
            'email_verified': False,
            'role': 'user'
        }

        # db.collection('users').document(user.uid).set(user_profile)
        new_user = User(email=user_data.email, usuario=user_data.name)
        session.add(new_user)
        session.commit()
        print(f"💾 (SIMULADO) Perfil salvo no Firestore: {user.uid}")

        token_response = create_token(
            user.uid, user_data.email, user_data.name)

        print(f"🎉 Registro concluído para: {user_data.email}")
        return token_response

    except exceptions.AlreadyExistsError:
        print(f"❌ Email já existe: {user_data.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este email já está cadastrado"
        )

    except exceptions.InvalidArgumentError as e:
        if "password" in str(e).lower():
            print(f"❌ Senha fraca para: {user_data.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A senha é muito fraca. Use uma senha mais forte"
            )
        else:
            print(f"❌ Argumento inválido: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Dados de registro inválidos"
            )

    except FirebaseError as e:
        print(f"❌ Erro do Firebase: {str(e)}")
        error_message = str(e)
        if "email" in error_message.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email inválido"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro no registro: {error_message}"
            )

    except Exception as e:
        print(f"❌ Erro inesperado no registro: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno no servidor. Tente novamente."
        )


# def verify_token()

@auth_router.post("/login", response_model=TokenSchemas)
async def login(login_data: UserLoginSchemas, session: Session = Depends(get_session)):
    try:
        print(f"🔐 Tentativa de login para: {login_data.email}")

        firebase_uid = authenticate_firebase_user(
            login_data.password, login_data.email)

        print(f"✅ Login bem-sucedido para: {firebase_uid}")

        user = session.query(User).filter(
            User.email == login_data.email).first()

        token_response = create_token(
            uid=firebase_uid,
            email=login_data.email,
            name=user.usuario
        )

        print(f"🎉 Login concluído para: {login_data.email}")
        return token_response

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro inesperado no login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno no servidor. Tente novamente."
        )
