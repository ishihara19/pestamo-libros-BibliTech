from fastapi_mail import FastMail, MessageSchema
from ..core.email_config import conf


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
    

async def enviar_correo_prestamo(correo: str, codigo_libro: str, titulo: str, fecha_entrega: str, documento_usuario: str):
    asunto = "Confirmación de Préstamo de Libro - Biblioteca"
    cuerpo = f"""
    <h2>📚 Confirmación de Préstamo de Libro</h2>
    <p>Hola, este mensaje confirma el préstamo de un libro a tu nombre.</p>

    <h3>📖 Detalles del Libro:</h3>
    <ul>
        <li><b>Título:</b> {titulo}</li>
        <li><b>Código:</b> {codigo_libro}</li>
    </ul>

    <h3>👤 Datos del Usuario:</h3>
    <ul>
        <li><b>Documento:</b> {documento_usuario}</li>
    </ul>

    <h3>📅 Información del Préstamo:</h3>
    <ul>
        <li><b>Fecha de devolución:</b> {fecha_entrega}</li>
    </ul>

    <p>⚠ <b>Importante:</b> Para reclamar o devolver el libro, es obligatorio presentar tu documento y el código del libro.</p>

    <p>✔ Por favor, conserva este correo como comprobante.</p>
    """

    mensaje = MessageSchema(
        subject=asunto,
        recipients=[correo],
        body=cuerpo,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(mensaje)
