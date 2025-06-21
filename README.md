# RiSaaS - Registro Interactivo de Suscripciones SaaS

Webapp Flask moderna para llevar registro, alertas y reporte de tus suscripciones SaaS.

- CRUD completo sobre SQLite
- Exporta .vcf para Google Calendar (con recordatorio automático)
- Reporte en CSV
- Emails automáticos
- Bootstrap 5 + SweetAlert2 para UX moderna

## Estructura del Proyecto

risaas/
│
├── app.py
├── utils.py
├── requirements.txt
├── LICENSE.txt
├── README.md
├── risaas.db # Base de datos SQLite (se crea la primera vez)
├── logs/
│ └── risaas.log
├── templates/
│ ├── base.html
│ ├── index.html
│ └── reporte.html
└── static/
└── custom.css


## Instalación

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
