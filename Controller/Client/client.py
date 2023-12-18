####################### ESTABLECER CONEXION HACIA EL SERVIDOR #################
import socket

# Variables para crear la conexion
HOST = "localhost"
PORT = 8000

# Crear socket
my_socket = socket.socket()

# Realizar la conexion con el servidor
my_socket.connect( (HOST, PORT) )

# Envio de datos
my_socket.send("Saludando al servidor")
response = my_socket.recv(1024) # 1024 value for default

print(response)

# Cerrar conexion
my_socket.close()

