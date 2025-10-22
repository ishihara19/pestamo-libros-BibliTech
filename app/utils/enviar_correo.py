from fastapi_mail import FastMail, MessageSchema
from..core.email_config import conf


async def enviar_correo_restablecimiento(correo: str, token: str):
    asunto = "Restablecimiento de contraseña"
    cuerpo = f"""
    <h2>Restablecimiento de contraseña</h2>
    <p>Hola, has solicitado restablecer tu contraseña.</p>
    <p>Tu código de verificación es: <b>{token}</b></p>
    <p>Este código expirará en 10 minutos.</p>
    """

    mensaje = MessageSchema(
        subject=asunto,
        recipients=[correo],
        body=cuerpo,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(mensaje)