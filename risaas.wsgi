import sys
import os

# Añade el path de la app para que Python la encuentre
sys.path.insert(0, os.path.dirname(__file__))

# Si usas un virtualenv, puedes activar su contexto (opcional, generalmente no es necesario)
# activate_this = '/opt/bitnami/estratekdata/app/risaas/venv/bin/activate_this.py'
# exec(open(activate_this).read(), {'__file__': activate_this})

from app import app as application