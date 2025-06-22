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
