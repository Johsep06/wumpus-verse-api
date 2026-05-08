from .config import firebase_auth


def generate_verification_link(email: str):
    '''
    Gera um link para validação de email do usuário.
    '''
    link = firebase_auth.generate_email_verification_link(email)
    return link


def generate_reset_lik(email: str) -> str:
    '''
    Gera um link de redefinição de senha para o email informado.
    '''
    try:
        link = firebase_auth.generate_password_reset_link(email)
        return link
    except firebase_auth.UserNotFoundError:
        raise ValueError("Usuário não encontrado")
    except Exception as e:
        raise RuntimeError(f"Erro ao gerar link: {e}")


def is_email_verified(uid: str) -> bool:
    '''
    Verifica se um usuário possui o email verificado.
    '''
    user = firebase_auth.get_user(uid)
    return user.email_verified
