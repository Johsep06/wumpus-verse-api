import os
from brevo import Brevo
from brevo.transactional_emails import SendTransacEmailRequestSender, SendTransacEmailRequestToItem

BREVO_API_KEY = os.getenv('BREVO_API_KEY')
FROM_EMAIL = os.getenv('FROM_EMAIL')

def send_email(
    to_email: str,
    user_name: str,
    subject: str,
    body: str,
) -> bool:
    """
    Envia um email com a API do Brevo.
    Retorna True se enviado com sucesso.
    """
    brevo_client = Brevo(api_key=BREVO_API_KEY)
    try:
        brevo_client.transactional_emails.send_transac_email(
            subject=subject,
            sender=SendTransacEmailRequestSender(
                email=FROM_EMAIL,
                name='Equipe Wumpus Verse',
            ),
            to=[
                SendTransacEmailRequestToItem(
                    email=to_email,
                    name=user_name,
                )
            ],
            html_content=body,
        )

        return True
    except Exception as e:
        print(f"Erro ao enviar e-mail de verificação via Brevo: {e}")
        return False
