from fastapi import APIRouter, HTTPException, Depends, status
from firebase_admin.exceptions import FirebaseError
from firebase_admin import auth as firebase_auth
from firebase_admin import auth, exceptions
import firebase_admin
from datetime import datetime

from firebase import db
from schemas import UserCreateSchemas, UserResponseSchemas, TokenSchemas


auth_router = APIRouter(prefix="/auth", tags=["authentication"])


@auth_router.post("/register", response_model=TokenSchemas, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreateSchemas):
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
        
        # 🔥 COMENTE ESTA LINHA TEMPORARIAMENTE PARA TESTAR
        # db.collection('users').document(user.uid).set(user_profile)
        print(f"💾 (SIMULADO) Perfil salvo no Firestore: {user.uid}")
        
        # 3. Preparar resposta
        user_response = UserResponseSchemas(
            uid=user.uid,
            email=user_data.email,
            name=user_data.name,
            created_at=datetime.now()
        )
        
        # 4. Gerar token customizado
        custom_token = auth.create_custom_token(user.uid)
        
        token_response = TokenSchemas(
            access_token=custom_token.decode('utf-8') if isinstance(custom_token, bytes) else custom_token,
            token_type="bearer",
            user=user_response
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


