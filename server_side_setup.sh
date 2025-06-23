# Python server-side setup script
#!/bin/bash
set -e

echo "==> Limpiando entorno virtual anterior (si existe)..."
rm -rf venv

echo "==> Creando nuevo entorno virtual (Python 3.11)..."
python3.11 -m venv venv

echo "==> Activando entorno virtual..."
source venv/bin/activate

echo "==> Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

echo "==> Verifica el archivo .env (credenciales mail):"
if [ ! -f .env ]; then
    echo "  >> ¡ATENCIÓN! Debes crear/copiar tu archivo .env con las credenciales necesarias."
else
    echo "  >> .env encontrado."
fi

echo ""
echo "==> Todo listo. Lanza tu app así:"
echo "    python app.py"