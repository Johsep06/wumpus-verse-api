from fastapi import APIRouter, HTTPException, Depends, status
from firebase_admin.exceptions import FirebaseError
from firebase_admin import auth as firebase_auth
from firebase_admin import auth, exceptions
import firebase_admin
from datetime import datetime
import requests
from sqlalchemy.orm import Session

from firebase import db
from schemas import UserCreateSchemas, UserResponseSchemas, TokenSchemas, UserLoginSchemas, FirebaseUserSchemas
from main import FIREBASE_API_KEY
from dependencies import get_session
from models import User

auth_router = APIRouter(prefix="/auth", tags=["authentication"])


def create_token(uid:str, email:str, name:str):
    # 3. Preparar resposta
        user_response = UserResponseSchemas(
            uid=uid,
            email=email,
            name=name,
            created_at=datetime.now()
        )

        # 4. Gerar token customizado
        custom_token = auth.create_custom_token(uid)

        token_response = TokenSchemas(
            access_token=custom_token.decode(
                'utf-8') if isinstance(custom_token, bytes) else custom_token,
            token_type="bearer",
            user=user_response
        )
        
        return token_response


@auth_router.post("/register", response_model=TokenSchemas, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreateSchemas, session:Session=Depends(get_session)):
    """
    Registra um novo usuário no sistema

    - **email**: Email válido do usuário
    - **password**: Senha (mínimo 6 caracteres)
    - **name**: Nome completo do usuário
    """
    try:
        print(f"📝 Tentativa de registro para: {user_data.email}")

        # 1. Criar usuário no Firebase Authentication
        user = auth.create_user(
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

        token_response = create_token(user.uid, user_data.email, user_data.name)

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
async def login(login_data: UserLoginSchemas, session:Session=Depends(get_session)):
    try:
        print(f"🔐 Tentativa de login para: {login_data.email}")
        
        # 1. Autenticar com Firebase REST API
        auth_payload = {
            "email": login_data.email,
            "password": login_data.password,
            "returnSecureToken": True
        }
        
        response = requests.post(
            f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}",
            json=auth_payload
        )
        
        auth_result = response.json()
        
        if response.status_code != 200:
            error_message = auth_result.get('error', {}).get('message', 'Erro de autenticação')
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
        
        # 2. Dados do usuário autenticado
        user_id = auth_result['localId']
        id_token = auth_result['idToken']
        
        print(f"✅ Login bem-sucedido para: {user_id}")
        
        # 🔥 TEMPORARIAMENTE: Pule o Firestore até ativar a API
        try:
            # Tenta buscar do Firestore
            user_doc = db.collection('users').document(user_id).get()
            if user_doc.exists:
                user_data = user_doc.to_dict()
                user_name = user_data.get('name', login_data.email.split('@')[0])
            else:
                # Se não existe no Firestore, usa dados básicos
                user_record = auth.get_user(user_id)
                user_name = user_record.display_name or login_data.email.split('@')[0]
        except Exception as firestore_error:
            print(f"⚠️  Firestore indisponível, usando dados básicos: {firestore_error}")
            user_name = login_data.email.split('@')[0]  # Nome padrão do email
        
        user = session.query(User).filter(User.email == login_data.email).first()
        
        # 3. Preparar resposta
        user_response = UserResponseSchemas(
            uid=user_id,
            email=login_data.email,
            name=user.usuario,
            created_at=datetime.now()  # Usar data atual temporariamente
        )
        
        token_response = TokenSchemas(
            access_token=id_token,
            token_type="bearer",
            user=user_response
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

# Função para verificar token JWT (útil para rotas protegidas)


async def get_current_user(token: str = Depends(lambda: "")) -> FirebaseUserSchemas:
    """
    Dependency para verificar e decodificar token JWT do Firebase
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticação necessário"
        )

    try:
        # Remove 'Bearer ' se presente
        if token.startswith('Bearer '):
            token = token[7:]

        decoded_token = auth.verify_id_token(token)

        return FirebaseUserSchemas(
            uid=decoded_token['uid'],
            email=decoded_token['email'],
            email_verified=decoded_token.get('email_verified', False)
        )

    except exceptions.InvalidIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )
    except exceptions.ExpiredIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Falha na autenticação"
        )
