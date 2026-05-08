import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(
    to_email: str,
    subject: str,
    body: str,
    smtp_server: str,
    smtp_port: int,
    sender_email: str,
    sender_password: str,
    use_tls: bool = True
) -> bool:
    """
    Envia um email via SMTP.
    Retorna True se enviado com sucesso.
    """
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            if use_tls:
                server.starttls()  # Ativa criptografia TLS
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
        return False