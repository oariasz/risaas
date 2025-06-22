import os
import datetime
from flask_mail import Message
from flask import flash
import smtplib
import unicodedata


# ---- 1. Función para crear el archivo .ics (calendario) ----

def crear_vcf(licencia):
    """Genera un archivo .ics para Google Calendar según frecuencia"""
    from icalendar import Calendar, Event, Alarm

    freq_map = {
        "Anual": "YEARLY",
        "Semestral": "MONTHLY",  # workaround: interval=6 para semestral
        "Mensual": "MONTHLY"
    }
    freq = freq_map.get(licencia.frecuencia_pago, "YEARLY")
    interval = 6 if licencia.frecuencia_pago == "Semestral" else 1

    cal = Calendar()
    event = Event()
    titulo = f"[RiSaaS] {licencia.producto} - {licencia.proveedor}"
    event.add('summary', titulo)
    event.add('dtstart', datetime.datetime.strptime(licencia.vencimiento, "%Y-%m-%d"))
    event.add('dtend', datetime.datetime.strptime(licencia.vencimiento, "%Y-%m-%d") + datetime.timedelta(hours=1))
    event.add('description', licencia.notas or "")
    event.add('location', licencia.website or "")
    event.add('rrule', {'freq': freq, 'interval': interval})
    # Alarma 2 días antes
    alarm = Alarm()
    alarm.add('trigger', datetime.timedelta(days=-2))
    alarm.add('action', 'DISPLAY')
    alarm.add('description', 'Próximo pago de suscripción SaaS')
    event.add_component(alarm)
    cal.add_component(event)

    if not os.path.exists("logs"):
        os.mkdir("logs")
    fname = f"risaas_{licencia.producto}_{licencia.id}.ics"
    fpath = os.path.join("logs", fname)
    with open(fpath, "wb") as f:
        f.write(cal.to_ical())
    return fpath

# ---- 2. Función para registrar acción en el log ----

def log_action(accion, licencia):
    """Registra acciones en un log de texto plano."""
    if not os.path.exists("logs"):
        os.mkdir("logs")
    with open("logs/risaas.log", "a", encoding="utf-8") as log:
        log.write(f"{datetime.datetime.now().isoformat()} | {accion} | {licencia.proveedor} | {licencia.producto} | {licencia.usuario} | {licencia.correo} | {licencia.tipo} | {licencia.cliente}\n")

# ---- 3. Función para enviar email (puedes ajustar los campos a gusto) ----

def enviar_email(mail, licencia, vcf_path):
    """Envía un email con los datos de la licencia y adjunta el .ics, manejando errores y sanitizando el correo"""
    # Normaliza el correo (elimina ñ, tildes, etc.)
    correo = unicodedata.normalize('NFKD', licencia.correo).encode('ascii', 'ignore').decode('ascii')
    # Opción: valida si el correo sigue siendo válido (opcional)

    from flask_mail import Message
    msg = Message(
        subject=f"[RiSaaS] Nueva suscripción: {licencia.producto} ({licencia.proveedor})",
        sender="oariasz72@gmail.com",
        recipients=[correo] if correo else ["oariasz72@gmail.com"]
    )
    msg.body = f"""
Registro exitoso de suscripción SaaS:

Proveedor: {licencia.proveedor}
Producto: {licencia.producto}
Website: {licencia.website}
Fecha Suscripción: {licencia.fecha_suscripcion}
Hora: {licencia.hora_suscripcion or '-'}
Frecuencia: {licencia.frecuencia_pago}
Vencimiento: {licencia.vencimiento}
Usuario: {licencia.usuario}
Correo: {licencia.correo}
Tipo: {licencia.tipo}
Cliente: {licencia.cliente or '-'}
Próximo pago: {licencia.proximo_pago}
Notas: {licencia.notas or '-'}

Archivo calendario adjunto.
    """

    # Adjunta el archivo .ics si existe
    if vcf_path and os.path.exists(vcf_path):
        with open(vcf_path, "rb") as ics:
            msg.attach(os.path.basename(vcf_path), "text/calendar; charset=utf-8", ics.read())

    try:
        mail.send(msg)
        flash("Email enviado correctamente.", "info")
    except smtplib.SMTPAuthenticationError:
        flash("Error de autenticación con el servidor SMTP de Gmail. Verifica tu usuario y contraseña de aplicación.", "error")
    except smtplib.SMTPException as e:
        flash(f"Error SMTP al enviar email: {e}", "error")
    except Exception as e:
        flash(f"Error inesperado al enviar email: {e}", "error")