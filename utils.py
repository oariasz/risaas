from datetime import datetime
import os
from flask_mail import Message

def crear_vcf(licencia):
    event_title = f"SaaS: {licencia.producto} ({licencia.proveedor})"
    start_date = licencia.fecha_suscripcion
    freq = licencia.frecuencia_pago.upper()
    alarm_minutes = 2*24*60  # 2 días antes

    dtstart = datetime.strptime(start_date, "%Y-%m-%d").strftime("%Y%m%dT090000Z")
    if freq == "ANUAL":
        rrule = "FREQ=YEARLY"
    elif freq == "MENSUAL":
        rrule = "FREQ=MONTHLY"
    elif freq == "SEMESTRAL":
        rrule = "FREQ=MONTHLY;INTERVAL=6"
    else:
        rrule = "FREQ=YEARLY"

    vcf = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Estratek RiSaaS//ES
BEGIN:VEVENT
SUMMARY:{event_title}
DTSTART:{dtstart}
RRULE:{rrule}
DESCRIPTION:{licencia.notas}
LOCATION:{licencia.website}
STATUS:CONFIRMED
BEGIN:VALARM
TRIGGER:-P2D
DESCRIPTION:Recordatorio de pago de licencia SaaS
ACTION:DISPLAY
END:VALARM
END:VEVENT
END:VCALENDAR
"""
    if not os.path.exists("logs"):
        os.makedirs("logs")
    path = f"logs/{licencia.producto}_{licencia.usuario}_{int(datetime.now().timestamp())}.vcf"
    with open(path, "w", encoding="utf-8") as f:
        f.write(vcf)
    return path

def log_action(action, licencia):
    with open("logs/risaas.log", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} | {action} | {licencia.proveedor} | {licencia.producto} | {licencia.usuario} | {licencia.correo}\n")

def enviar_email(mail, licencia, vcf_path):
    msg = Message(
        subject=f"[RiSaaS] {licencia.producto} - {licencia.usuario} - {licencia.fecha_suscripcion} ({licencia.frecuencia_pago})",
        sender="oariasz72@gmail.com",
        recipients=["oariasz72@gmail.com"]
    )
    msg.body = f"""Registro de Licencia SaaS

Proveedor: {licencia.proveedor}
Producto: {licencia.producto}
Website: {licencia.website}
Fecha Suscripción: {licencia.fecha_suscripcion}
Frecuencia: {licencia.frecuencia_pago}
Vencimiento: {licencia.vencimiento}
Usuario: {licencia.usuario}
Correo: {licencia.correo}
Próximo Pago (USD): {licencia.proximo_pago}
Tipo: {licencia.tipo}
Cliente: {licencia.cliente}
Notas: {licencia.notas}
Estatus: {licencia.estatus}
"""
    with open(vcf_path, "rb") as fp:
        msg.attach(os.path.basename(vcf_path), "text/calendar", fp.read())
    try:
        mail.send(msg)
    except Exception as e:
        print(f"Error enviando email: {e}")
