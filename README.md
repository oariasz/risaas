# RiSaaS - Registro Interactivo de Suscripciones SaaS

Webapp Flask moderna para llevar registro, alertas y reportes de tus suscripciones SaaS.

- CRUD completo sobre SQLite
- Exporta .ics para Google Calendar (con recordatorio automático)
- Reporte en CSV
- Emails automáticos (configurables por .env)
- Bootstrap 5 + SweetAlert2 para UX moderna
- Soporte modo claro/oscuro y logos dinámicos

## Estructura del Proyecto

```text
risaas/
│
├── app.py
├── utils.py
├── requirements.txt
├── LICENSE.txt
├── README.md
├── .env.example         # Archivo ejemplo para credenciales email
├── .gitignore
├── risaas.db            # Base de datos SQLite (se crea automáticamente)
├── logs/
│   └── risaas.log
├── templates/
│   ├── base.html
│   ├── index.html
│   └── reporte.html
└── static/
    ├── custom.css
    ├── Logotipo PNG.png
    └── Logotipo Gris 00% Blanco.png

```

## Instalación


1. **Clona el repositorio y entra al directorio**
    ```bash
    git clone https://github.com/oariasz/risaas.git
    cd risaas
    ```

2. **Crea un entorno virtual y actívalo**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Instala los requerimientos**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configura tus credenciales de email**
    - Copia `.env.example` a `.env`
    - Edita `.env` con tus datos reales de Gmail:
      ```
      MAIL_USERNAME=tu_email@gmail.com
      MAIL_PASSWORD=tu_app_password
      ```
      > **Nota:** Usa una App Password de Gmail (no tu password regular). Más información: https://support.google.com/mail/answer/185833

5. **Agrega `.env` a tu `.gitignore`**
    - Ya está listado en el `.gitignore` por defecto, pero asegúrate de **no subir** el `.env` real.

6. **Inicializa la base de datos y ejecuta la app**
    ```bash
    python app.py
    ```

7. **Abre tu navegador en** [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## Ejemplo de `.env.example`

```env
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=tu_app_password
```


## Ejecución avanzada y selección de puerto
Por defecto, la aplicación corre en el puerto **5000**.  
Si el puerto 5000 está ocupado, el servidor busca automáticamente el siguiente disponible (5001, 5002, ..., hasta 5010).

Puedes modificar el puerto de tres maneras:

**Mediante argumento de línea de comando:**
```bash
python app.py --port 5050
```

**Mediante variable de entorno:**
```bash
export PORT=8080
python app.py
```

**Automáticamente:**  
Si el puerto solicitado está en uso, el script intentará hasta 10 puertos consecutivos.

Siempre verás en consola un mensaje como:
```cpp
==> Servidor arrancando en http://127.0.0.1:5001/
```

**Ejemplo completo:**
```bash
python app.py                   # Intenta 5000...5010
python app.py --port 5050       # Usa 5050 (o el siguiente libre)
export PORT=8888
python app.py                   # Usa 8888 (o el siguiente libre)
```

## Uso general

- Completa la forma para registrar una suscripción.
- Descarga el archivo .vcf e impórtalo a tu Google Calendar.
- Edita/elimina desde el CRUD inferior.
- Consulta próximos vencimientos y emite reportes en CSV.
- El sistema envía automáticamente un email al usuario registrado y adjunta el evento de calendario.
- Cambia a modo oscuro con el botón de la luna.

## Despliegue en producción

- Puedes usar [Gunicorn](https://gunicorn.org/) o [uWSGI](https://uwsgi-docs.readthedocs.io/) para servir la app detrás de Nginx/Apache.
- Cambia `app.run(debug=True)` por `app.run(debug=False)` para producción.
- Cambia la `SECRET_KEY` por una mucho más segura.
- Configura tu servidor SMTP real y revisa las políticas de seguridad de tu proveedor de correo.

## Licencia

MIT License - ver LICENSE.txt