sudo apt install sqlite3 
# paso2 crear la base de  datos users.db con sqlite3
sqlite3 users.db

## luego entraremos a la shell de sqlite y escribimos lo siguiente  y nos da la ruta de la base de datos
.databases
.exit
# con esto ya tenemos la base da datos creada
# ejecutar el app login.py
python3 flask login.py