import os

from .smtp import send_email

SMTP_CONFIG = {
    "smtp_server": os.getenv('smtp_server'),
    "smtp_port": int(os.getenv('smtp_port')),
    "sender_email": os.getenv('sender_email'),
    "sender_password": os.getenv('sender_password'),
    "use_tls": True
}


def send_verification_email(user_name: str, user_email: str, verification_link: str):
    send_email(
        to_email=user_email,
        subject='Complete seu cadastro - Verifique seu e-mail no Wumpus Verse',
        body=verification_text.format(
                nome_usuario=user_name,
                link_de_verificacao=verification_link
        ),
        **SMTP_CONFIG,
    )


def send_reset_email(user_name: str, user_email: str, reset_link: str):
    status = send_email(
        to_email=user_email,
        subject='Solicitação para mudança de senha na plataforma Wumpus Verse',
        body=reset_text.format(
                name=user_name,
                link=reset_link
        ),
        **SMTP_CONFIG,
    )
    
    return status


__all__ = [
    'send_email',
    'SMTP_CONFIG',
    'send_verification_email',
]

verification_text = '''Olá {nome_usuario},

A equipe do Wumpus Verse recebeu seu cadastro e notamos que seu e–mail ainda não foi verificado. Para garantir a segurança da sua conta e liberar todas as funcionalidades do jogo, precisamos confirmar que este endereço pertence a você.

✅ Clique no link abaixo para verificar seu e–mail em até 24 horas:
➡️ {link_de_verificacao}

Se o botão não funcionar, copie e cole o endereço diretamente no seu navegador.

Por que verificar?

    Recuperação de senha e proteção da conta

    Acesso completo as funcionalidades do sistema.

    Novidades do projeto.

Não solicitou este cadastro?
Ignorar este e–mail. Nenhuma ação será tomada e o link expirará automaticamente.

Agradecemos por fazer parte do Wumpus Verse!

— Equipe Wumpus Verse
Mensagem automática. Não responda este e–mail.'''

reset_text = """Olá {name},

Recebemos uma solicitação para redefinir sua senha no Wumpus Verse.

Clique no link abaixo para criar uma nova senha (válido por 1 hora):

{link}

Se você não solicitou, ignore este e‑mail. Sua senha permanecerá a mesma.

— Equipe Wumpus Verse
"""
