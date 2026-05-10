import os
from datetime import datetime

from .sending_emails import send_email


def send_verification_email(user_name: str, user_email: str, verification_link: str):
    status = send_email(
        to_email=user_email,
        user_name=user_name,
        subject='Complete seu cadastro - Verifique seu e-mail no Wumpus Verse',
        body=verification_text.format(
                nome_usuario=user_name,
                link_de_verificacao=verification_link,
                ano=datetime.now().year,
        ),
    )

    return status


def send_reset_email(user_name: str, user_email: str, reset_link: str):
    status = send_email(
        to_email=user_email,
        user_name=user_name,
        subject='Solicitação para mudança de senha na plataforma Wumpus Verse',
        body=reset_text.format(
                name=user_name,
                link=reset_link,
                ano=datetime.now().year,
        ),
    )

    return status


__all__ = [
    'send_email',
    'send_verification_email',
]

verification_text = '''<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Verifique seu e‑mail | Wumpus Verse</title>
  <style>
    body {{margin: 0; padding: 0; font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif; background-color: #f4f4f7;}}
    .container {{max-width: 600px; margin: 20px auto; background: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.05);}}
    .header {{background-color: #1a2a3a; padding: 24px 20px; text-align: center;}}
    .header h1 {{margin: 0; color: #ffcc00; font-size: 28px; letter-spacing: 1px;}}
    .content {{padding: 32px 28px;}}
    .greeting {{font-size: 18px; font-weight: 600; color: #2c3e4e; margin-bottom: 20px;}}
    .message {{color: #4a5b6e; line-height: 1.6; margin-bottom: 24px;}}
    .button-container {{text-align: center; margin: 32px 0;}}
    .button {{background-color: #ffcc00; color: #1a2a3a; text-decoration: none; padding: 12px 28px; border-radius: 40px; font-weight: bold; display: inline-block; font-size: 16px; transition: background 0.2s;}}
    .button:hover {{background-color: #e6b800;}}
    .info-box {{background-color: #f9f9fc; border-left: 4px solid #ffcc00; padding: 16px 20px; margin: 24px 0; border-radius: 8px;}}
    .info-title {{font-weight: 700; color: #2c3e4e; margin-bottom: 8px;}}
    .info-list {{margin: 0; padding-left: 20px; color: #4a5b6e;}}
    .info-list li {{margin-bottom: 6px;}}
    .warning {{color: #b33; font-size: 14px; margin-top: 28px; border-top: 1px solid #e0e4e8; padding-top: 20px;}}
    .footer {{background-color: #f0f2f5; padding: 20px; text-align: center; font-size: 12px; color: #6c7a8a;}}
    .footer a {{color: #1a2a3a; text-decoration: none;}}
    @media (max-width: 600px) {{.content {{padding: 20px 16px;}} .button {{padding: 10px 20px;}}}}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>🐉 Wumpus Verse</h1>
    </div>
    <div class="content">
      <p class="greeting">Olá, <strong>{nome_usuario}</strong>!</p>
      <div class="message">
        <p>A equipe do <strong>Wumpus Verse</strong> recebeu seu cadastro e notamos que seu e‑mail ainda não foi verificado. Para garantir a segurança da sua conta e liberar todas as funcionalidades do jogo, precisamos confirmar que este endereço pertence a você.</p>
      </div>
      
      <div class="button-container">
        <a href="{link_de_verificacao}" class="button" target="_blank">✅ Verificar meu e‑mail</a>
      </div>
      
      <div class="info-box">
        <div class="info-title">🔐 Por que verificar?</div>
        <ul class="info-list">
          <li>Recuperação de senha e proteção da conta</li>
          <li>Acesso completo às funcionalidades do sistema</li>
          <li>Novidades do projeto em primeira mão</li>
        </ul>
      </div>
      
      <div class="warning">
        ⚠️ <strong>Não solicitou este cadastro?</strong><br>
        Ignore este e‑mail. Nenhuma ação será tomada e o link expirará automaticamente em <strong>24 horas</strong>.
      </div>
      <p style="font-size: 14px; color: #6c7a8a; margin-top: 20px;">Se o botão não funcionar, copie e cole o link abaixo no seu navegador:<br>
      <span style="word-break: break-all;">{link_de_verificacao}</span></p>
    </div>
    <div class="footer">
      <p>© {ano} Wumpus Verse – Todos os direitos reservados.</p>
      <p>Mensagem automática, não responda este e‑mail.</p>
      <p><a href="#">Política de Privacidade</a> | <a href="#">Suporte</a></p>
    </div>
  </div>
</body>
</html>'''

reset_text = '''<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Redefinição de senha | Wumpus Verse</title>
  <style>
    body {{margin: 0; padding: 0; font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif; background-color: #f4f4f7;}}
    .container {{max-width: 600px; margin: 20px auto; background: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.05);}}
    .header {{background-color: #1a2a3a; padding: 24px 20px; text-align: center;}}
    .header h1 {{margin: 0; color: #ffcc00; font-size: 28px;}}
    .content {{padding: 32px 28px;}}
    .greeting {{font-size: 18px; font-weight: 600; color: #2c3e4e; margin-bottom: 20px;}}
    .message {{color: #4a5b6e; line-height: 1.6; margin-bottom: 24px;}}
    .button-container {{text-align: center; margin: 32px 0;}}
    .button {{background-color: #dc3545; color: white; text-decoration: none; padding: 12px 28px; border-radius: 40px; font-weight: bold; display: inline-block; font-size: 16px; background-color: #c0392b;}}
    .button:hover {{background-color: #a82315;}}
    .warning {{background-color: #fef5e7; border-left: 4px solid #f39c12; padding: 16px 20px; margin: 24px 0; border-radius: 8px; font-size: 14px;}}
    .footer {{background-color: #f0f2f5; padding: 20px; text-align: center; font-size: 12px; color: #6c7a8a;}}
    .footer a {{color: #1a2a3a; text-decoration: none;}}
    @media (max-width: 600px) {{.content {{padding: 20px 16px;}} .button {{padding: 10px 20px;}}}}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>🐉 Wumpus Verse</h1>
    </div>
    <div class="content">
      <p class="greeting">Olá, <strong>{name}</strong>!</p>
      <div class="message">
        <p>Recebemos uma solicitação para redefinir sua senha no <strong>Wumpus Verse</strong>. Clique no botão abaixo para criar uma nova senha.</p>
        <p>Este link é <strong>válido por 1 hora</strong>.</p>
      </div>
      
      <div class="button-container">
        <a href="{link}" class="button" target="_blank">🔐 Redefinir minha senha</a>
      </div>
      
      <div class="warning">
        <strong>⚠️ Não solicitou alteração de senha?</strong><br>
        Ignore este e‑mail. Sua senha permanecerá a mesma e nenhuma ação será tomada.
      </div>
      <p style="font-size: 14px; color: #6c7a8a; margin-top: 20px;">Se o botão não funcionar, copie e cole o link abaixo no seu navegador:<br>
      <span style="word-break: break-all;">{link}</span></p>
    </div>
    <div class="footer">
      <p>© {ano} Wumpus Verse – Todos os direitos reservados.</p>
      <p>Mensagem automática, não responda este e‑mail.</p>
      <p><a href="#">Política de Privacidade</a> | <a href="#">Suporte</a></p>
    </div>
  </div>
</body>
</html>'''
