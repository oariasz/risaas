from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from datetime import datetime, timedelta
import csv
import os
from utils import crear_vcf, log_action, enviar_email
from dotenv import load_dotenv
import os


load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'supersecretkey')  # valor por defecto si no existe

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///risaas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuración de email (usa tus credenciales de Gmail)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
# Credenciales del correo
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

mail = Mail(app)
db = SQLAlchemy(app)

class Licencia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    proveedor = db.Column(db.String(64))
    producto = db.Column(db.String(64))
    website = db.Column(db.String(256))
    fecha_suscripcion = db.Column(db.String(20))
    hora_suscripcion = db.Column(db.String(10))
    frecuencia_pago = db.Column(db.String(16))
    vencimiento = db.Column(db.String(20))
    usuario = db.Column(db.String(64))
    correo = db.Column(db.String(64))
    proximo_pago = db.Column(db.String(16))
    tipo = db.Column(db.String(16))
    cliente = db.Column(db.String(64))
    notas = db.Column(db.String(256))
    estatus = db.Column(db.String(16), default="Activo")

def calcular_vencimiento(fecha, frecuencia):
    fecha_dt = datetime.strptime(fecha, "%Y-%m-%d")
    if frecuencia == "Anual":
        return (fecha_dt + timedelta(days=365)).strftime("%Y-%m-%d")
    elif frecuencia == "Mensual":
        return (fecha_dt + timedelta(days=30)).strftime("%Y-%m-%d")
    elif frecuencia == "Semestral":
        return (fecha_dt + timedelta(days=182)).strftime("%Y-%m-%d")
    return fecha

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Recoge campos del formulario
        proveedor = request.form['proveedor']
        producto = request.form['producto']
        website = request.form['website']
        fecha_suscripcion = request.form['fecha_suscripcion']
        hora_suscripcion = request.form.get('hora_suscripcion')
        frecuencia_pago = request.form['frecuencia_pago']
        usuario = request.form['usuario']
        correo = request.form['correo']
        proximo_pago = request.form['proximo_pago']
        tipo = request.form['tipo']
        cliente = request.form.get('cliente') if tipo == "Comercial" else ""
        notas = request.form['notas']
        estatus = "Activo"
        vencimiento = calcular_vencimiento(fecha_suscripcion, frecuencia_pago)

        # Validación obligatoria cliente
        if tipo == "Comercial" and not cliente.strip():
            flash("El campo Cliente es obligatorio para tipo Comercial.", "error")
            return redirect(url_for('index'))

        licencia = Licencia(
            proveedor=proveedor, producto=producto, website=website,
            fecha_suscripcion=fecha_suscripcion, hora_suscripcion=hora_suscripcion,
            frecuencia_pago=frecuencia_pago, vencimiento=vencimiento,
            usuario=usuario, correo=correo, proximo_pago=proximo_pago,
            tipo=tipo, cliente=cliente, notas=notas, estatus=estatus
        )
        db.session.add(licencia)
        db.session.commit()

        # Genera VCF
        vcf_path = crear_vcf(licencia)

        # Log
        log_action("CREAR", licencia)

        # Enviar email
        enviar_email(mail, licencia, vcf_path)

        flash("¡Licencia registrada correctamente!", "success")
        return render_template("index.html", vcf_file=os.path.basename(vcf_path), licencias=Licencia.query.all())
    else:
        return render_template("index.html", licencias=Licencia.query.all())

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    licencia = Licencia.query.get_or_404(id)
    if request.method == "POST":
        # Actualiza campos desde el formulario
        licencia.proveedor = request.form['proveedor']
        licencia.producto = request.form['producto']
        licencia.website = request.form['website']
        licencia.fecha_suscripcion = request.form['fecha_suscripcion']
        licencia.hora_suscripcion = request.form.get('hora_suscripcion')
        licencia.frecuencia_pago = request.form['frecuencia_pago']
        licencia.usuario = request.form['usuario']
        licencia.correo = request.form['correo']
        licencia.proximo_pago = request.form['proximo_pago']
        licencia.tipo = request.form['tipo']
        licencia.cliente = request.form.get('cliente') if licencia.tipo == "Comercial" else ""
        licencia.notas = request.form['notas']
        licencia.estatus = "Activo"
        licencia.vencimiento = calcular_vencimiento(licencia.fecha_suscripcion, licencia.frecuencia_pago)

        db.session.commit()

        # Genera VCF y envía mail
        vcf_path = crear_vcf(licencia)
        log_action("EDITAR", licencia)
        enviar_email(mail, licencia, vcf_path)
        flash("¡Licencia modificada correctamente!", "success")
        return redirect(url_for('index'))
    else:
        return render_template("index.html", editar_licencia=licencia, licencias=Licencia.query.all())

@app.route("/descargar_vcf/<filename>")
def descargar_vcf(filename):
    return send_file(f"logs/{filename}", as_attachment=True)

@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    licencia = Licencia.query.get_or_404(id)
    db.session.delete(licencia)
    db.session.commit()
    log_action("ELIMINAR", licencia)
    flash("Licencia eliminada. Recuerda borrar la entrada del calendario si existe.", "warning")
    return redirect(url_for('index'))

@app.route("/reporte")
def reporte():
    licencias = Licencia.query.filter_by(estatus="Activo").order_by(Licencia.vencimiento.asc()).all()
    csv_path = "logs/reporte_licencias.csv"
    with open(csv_path, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Proveedor", "Producto", "Website", "Fecha Suscripción", "Vencimiento", "Usuario", "Correo", "Próximo Pago (USD)", "Tipo", "Cliente", "Notas", "Estatus"])
        for l in licencias:
            writer.writerow([l.proveedor, l.producto, l.website, l.fecha_suscripcion, l.vencimiento, l.usuario, l.correo, l.proximo_pago, l.tipo, l.cliente, l.notas, l.estatus])
    return send_file(csv_path, as_attachment=True)


if __name__ == "__main__":
    import sys
    import socket

    def get_free_port(start_port=5000, max_tries=10):
        port = start_port
        for _ in range(max_tries):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.bind(("", port))
                    return port
                except OSError:
                    port += 1
        raise OSError("No free port found in range.")

    # Por defecto 5000
    port = int(os.environ.get("PORT", 5000))
    # Permite override via línea de comando: python app.py --port 5050
    if "--port" in sys.argv:
        idx = sys.argv.index("--port")
        if len(sys.argv) > idx + 1:
            port = int(sys.argv[idx + 1])

    # Busca siguiente puerto libre si el primero está ocupado
    port = get_free_port(port)

    with app.app_context():
        db.create_all()
        if not os.path.exists("logs"):
            os.mkdir("logs")
    print(f"==> Servidor arrancando en http://127.0.0.1:{port}/")
    app.run(host="127.0.0.1", port=port, debug=True)

'''
# Main anterior

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        if not os.path.exists("logs"):
            os.mkdir("logs")
    app.run(debug=True)
'''