from fastapi import APIRouter, HTTPException, Depends, status
from firebase_admin.exceptions import FirebaseError
from firebase_admin import exceptions
from datetime import datetime
import requests
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from firebase import firebase_auth
from schemas import UserCreateSchemas, TokenSchemas, UserLoginSchemas, UserSchemas
from main import FIREBASE_API_KEY
from dependencies import get_session, check_token
from models import User

auth_router = APIRouter(prefix="/auth", tags=["authentication"])


def format_token_response(email: str, name: str, id_token):

    token_response = TokenSchemas(
        access_token=id_token,
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

    return auth_result['localId'], auth_result['idToken']


def delete_user_firebase(email=None, uid=None):
    """
    Deleta um usuário do Firebase Authentication.

    Args:
        email (str): Email do usuário a ser deletado
        uid (str): UID do usuário a ser deletado

    Retorna:
        bool: True se deletado com sucesso, False caso contrário
    """
    try:
        # Deleta o usuário pelo UID
        firebase_auth.delete_user(uid)
        print(f"✅ Usuário deletado com sucesso! UID: {uid}")
        return True

    except firebase_auth.UserNotFoundError:
        print(f"❌ Usuário não encontrado (Email: {email}, UID: {uid})")
        return False
    except Exception as e:
        print(f"❌ Erro ao deletar usuário: {e}")
        return False


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

        user = session.query(User).filter(User.usuario == user_data.name)
        
        if user is not None:
            raise HTTPException(status_code=409, detail=f"Já existe um usuário com o nome {user_data.name}")
        
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

        _, id_token = authenticate_firebase_user(user_data.password, user_data.email)
        token_response = format_token_response(
            id_token=id_token, 
            email=user_data.email, 
            name=user_data.name
        )

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


@auth_router.post("/login", response_model=TokenSchemas)
async def login(login_data: UserLoginSchemas, session: Session = Depends(get_session)):
    try:
        print(f"🔐 Tentativa de login para: {login_data.email}")

        firebase_uid, firebase_id_token = authenticate_firebase_user(
            login_data.password, login_data.email)

        print(f"✅ Login bem-sucedido para: {firebase_uid}")

        user = session.query(User).filter(
            User.email == login_data.email).first()

        token_response = format_token_response(
            id_token=firebase_id_token,
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


@auth_router.delete('/user')
async def delete_user(
    session: Session = Depends(get_session),
    token: UserSchemas = Depends(check_token)
    ):
    try:
        delete_user_firebase(token.email, token.uid)
        user = session.query(User).filter(User.email == token.email).first()

        email = user.email
        name = user.usuario
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        session.delete(user)
        session.commit()
        
        return {
            "message": "Usuário deletado com sucesso",
            "email": email,
            "name": name,
            "timestamp": datetime.now().isoformat()
        }

    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        print(f"❌ Erro ao deletar usuário: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno ao deletar usuário: {str(e)}"
        )

@auth_router.post("/login-form", response_model=TokenSchemas)
async def login_form(login_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    try:
        print(f"🔐 Tentativa de login para: {login_data.username}")

        firebase_uid, firebase_id_token = authenticate_firebase_user(
            login_data.password, login_data.username)

        print(f"✅ Login bem-sucedido para: {firebase_uid}")

        user = session.query(User).filter(User.email == login_data.username).first()

        token_response = format_token_response(
            id_token=firebase_id_token,
            email=login_data.username,
            name=user.usuario
        )

        print(f"🎉 Login concluído para: {login_data.username}")
        return token_response

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro inesperado no login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno no servidor. Tente novamente."
        )