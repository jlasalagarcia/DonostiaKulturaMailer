# DonostiaKulturaMailer
Conectarse a la web de Donostia Kultura y enviar correo con los préstamos de varios usuarios

RunAvisoFechaLibros.bat: archivo a ejecutar para iniciar el programa. Consejo:  crear un acceso directo en el escritorio para poder ejecutarlo cada semana.

AvisoFechaLibrosBibliotecas.py: programa en Python que se conecta a la web de Donostia Kultura para cada usuario de "users.cvs", y recolecta los préstamos de cada uno, y envía un correo "resumen" donde los préstamos a devolver en menos de 7 días están en rojo.

users.csv: usuarios de Donostia Kultura de los que queramos consultar sus préstamos.

mail.csv: correos electrónicos que usa el programa. El primer correo tiene que ser de gmail, y será desde el que se envíe el correo resumen. El destino del correo serán todos los correos electrónicos dados de alta, incluido el primero. Aunque el primer correo tiene que ser de gmail, el resto no tienen porqué serlo.
