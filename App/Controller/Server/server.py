##################### CREANDO CONEXION PARA DRON ##################
import socket
from djitellopy import tello

# Variables para crear la conexion
HOST = "localhost"
PORT = 8000

# Crear socket
my_socket = socket.socket()

# Estableciendo conexion
my_socket.bind( (HOST, PORT) )

# Estableciendo el numero de peticiones
my_socket.listen(5)

while True:
    connection, address = my_socket.accept()

    print(f"Estableciendo conexion con {address}")

    connection.send("Enviando informacion desde el servidor")
    connection.close()