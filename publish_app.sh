#!/bin/bash
set -e

# CONFIGURACIÓN
APP_NAME="risaas"
FLASK_VENV_PATH="/opt/bitnami/estratekdata/app/$APP_NAME/venv"
APP_PATH="/opt/bitnami/estratekdata/app/$APP_NAME"
WSGI_FILE="$APP_PATH/risaas.wsgi"
VHOST_CONF="/opt/bitnami/apache2/conf/bitnami/bitnami-apps-vhosts.conf"
BACKUP="$VHOST_CONF.bak.$(date +%Y%m%d_%H%M%S)"
APACHECTL="/opt/bitnami/apache2/bin/apachectl"
CTL_SCRIPT="/opt/bitnami/ctlscript.sh"
APP_DOMAIN="app.estratekdata.com"
SUBPATH="/risaas"
VHOST_MARKER="## RISAAAS FLASK APP"

echo "==> [INFO] Respaldando configuración actual: $VHOST_CONF"
sudo cp "$VHOST_CONF" "$BACKUP"

# Bloque para no duplicar
if ! grep -q "$VHOST_MARKER" "$VHOST_CONF"; then
  sudo tee -a "$VHOST_CONF" > /dev/null <<EOF

$VHOST_MARKER
<VirtualHost *:80>
    ServerName $APP_DOMAIN
    WSGIDaemonProcess $APP_NAME user=bitnami group=bitnami threads=5 python-home=$FLASK_VENV_PATH
    WSGIScriptAlias $SUBPATH $WSGI_FILE
    <Directory $APP_PATH>
        Require all granted
    </Directory>
    Alias $SUBPATH/static $APP_PATH/static
    <Directory $APP_PATH/static/>
        Require all granted
    </Directory>
    ErrorLog \${APACHE_LOG_DIR}/$APP_NAME-error.log
    CustomLog \${APACHE_LOG_DIR}/$APP_NAME-access.log combined
</VirtualHost>
EOF
  echo "==> [INFO] VirtualHost añadido a $VHOST_CONF"
else
  echo "==> [INFO] Ya existe el VirtualHost para $APP_NAME, no se modifica."
fi

echo "==> [INFO] Verificando sintaxis de Apache..."
sudo $APACHECTL -t
if [ $? -ne 0 ]; then
  echo "!!! ERROR: Configuración inválida. Restaurando backup."
  sudo cp "$BACKUP" "$VHOST_CONF"
  exit 1
fi

echo "==> [INFO] Reiniciando Apache..."
sudo $CTL_SCRIPT restart apache

echo "==> [SUCCESS] Tu app Flask $APP_NAME está en https://$APP_DOMAIN$SUBPATH"
echo "==> Para restaurar configuración previa: sudo cp $BACKUP $VHOST_CONF && sudo $CTL_SCRIPT restart apache"
