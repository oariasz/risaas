#!/bin/bash
set -e

# VARIABLES CONFIGURABLES
APP_NAME="risaas"
REMOTE_USER="bitnami"
REMOTE_HOST="etk-web"         # O puedes usar la IP: "3.216.52.106"
REMOTE_BASE="/opt/bitnami/estratekdata/app"
REMOTE_APP_DIR="$REMOTE_BASE/$APP_NAME"
TARFILE="${APP_NAME}.tar.gz"
EXCLUDES=(
    --exclude='venv'
    --exclude='logs' 
    --exclude='risaas.db' 
    --exclude='.env' 
    --exclude='.DS_Store'
      --exclude='._*')
LOCAL_DIR="$(pwd)"

# Actualizar librerias
./venv/bin/pip freeze > requirements.txt

# Empaquetar
echo ">> Empaquetando el proyecto (sin venv, logs, base ni .env)..."
tar -czf "$TARFILE" "${EXCLUDES[@]}" *

# Subir paquete
echo ">> Subiendo $TARFILE a $REMOTE_USER@$REMOTE_HOST:/tmp/"
scp "$TARFILE" "$REMOTE_USER@$REMOTE_HOST:/tmp/"

# Desplegar en el server remoto
echo ">> Conectando por SSH para desplegar en $REMOTE_APP_DIR ..."
ssh "$REMOTE_USER@$REMOTE_HOST" bash -s << EOF
  set -e
  mkdir -p "$REMOTE_APP_DIR"
  rm -rf "$REMOTE_APP_DIR/venv" "$REMOTE_APP_DIR/logs" "$REMOTE_APP_DIR/risaas.db"
  tar -xzf "/tmp/$TARFILE" -C "$REMOTE_APP_DIR"
  rm "/tmp/$TARFILE"
  cd "$REMOTE_APP_DIR"
  echo ">> Código desplegado en $REMOTE_APP_DIR"
  echo ""
  echo "==> Ahora haz lo siguiente en la SSH:"
  echo "  1. cd $REMOTE_APP_DIR"
  echo "  2. python3 -m venv venv"
  echo "  3. source venv/bin/activate"
  echo "  4. pip install --upgrade pip && pip install -r requirements.txt"
  echo "  5. Copia o edita tu archivo .env con credenciales mail"
  echo "  6. python app.py"
EOF

# Limpiar el archivo comprimido local
rm "$TARFILE"

echo ">> Deployment listo. Termina la configuración manual en el server remoto por SSH."
