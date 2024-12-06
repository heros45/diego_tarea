#!/bin/bash
echo "instalanddo pip, por si no esta instalado"
apt install python3-pip -y
echo "instalando sqlite3"
apt install sqlite3 -y
.databases
.exit
echo "actualizando pip"
python3 -m pip install --upgrade pip
echo "instalando virtualenv"
apt install python3-venv
echo "creando entorno virtual"
python3 -m venv venv
echo "activando entorno virtual"
source venv/bin/activate

echo "instalando requirements"
pip install -r requirements.txt
 
echo "ejecuntado flask"
python3 login.py 

