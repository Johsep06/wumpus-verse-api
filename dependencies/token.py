from fastapi import Depends, HTTPException, status
from firebase import firebase_auth, exceptions
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from firebase_admin._auth_utils import InvalidIdTokenError

from . import get_session
from models import User
from schemas import UserSchemas


oauth2_schema = OAuth2PasswordBearer(tokenUrl='auth/login')


def check_token(token=Depends(oauth2_schema), session: Session = Depends(get_session)) -> UserSchemas:
    """
    Verifica token JWT do Firebase e retorna usuário autenticado
    """
    try:
        decoded_token = firebase_auth.verify_id_token(token)
        user_id = decoded_token['uid']
        email = decoded_token['email']

        # 2. Buscar usuário no banco de dados (não no Firebase)
        user = session.query(User).filter(User.email == email).first()

        if not user:
            # Usuário autenticado no Firebase mas não existe no seu DB
            # Pode criar automaticamente ou retornar erro
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado no sistema"
            )

        user_response = UserSchemas(
            email=email, uid=user_id, name=user.usuario)

        return user_response
    except InvalidIdTokenError:
        raise HTTPException(
            status_code=401, 
            detail="Token inválido ou expirado"
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro na verificação do token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Falha na autenticação"
        )
