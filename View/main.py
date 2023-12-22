import pygame
from djitellopy import tello
import screen_app

# Inicio de la app
def init():

    # Cargar la ventana de presentacion de la app
    previewWindowLoad()

    # Cargar la ventana principal de la app
    mainWindowApp()
    
# Cargar ventana de presentacion
def previewWindowLoad():
    pygame.init()

    # Display del tamaño de la pantalla
    win = pygame.display.set_mode((800, 500))

    # Establecer icono para app
    icon = pygame.image.load("Model/images/icon/logodron 1.png")
    pygame.display.set_icon(icon)

    # Nombre de la app
    name_app = "AIC-Drone"
    pygame.display.set_caption(name_app)

    # Imagen de App al cargar
    show_image = True
    screen_icon = pygame.image.load("Model/images/icon/ScreenApp.png")
    win.blit(screen_icon, screen_icon.get_rect())
    pygame.display.update()

    # Mostrar imagen por 2 seg
    pygame.time.wait(2000)

    # Cerrar ventana
    pygame.quit()

# Ventana principal de la aplicacion
def mainWindowApp():
    socket = tello.Tello()
    
    # Mostrar nueva ventana para cargar app
    pygame.init()

    # Display del tamaño de la pantalla
    win = pygame.display.set_mode((800, 600))

    # Establecer icono para app
    icon = pygame.image.load("Model/images/icon/logodron 1.png")
    pygame.display.set_icon(icon)

    # Nombre de la app
    name_app = "AIC-Drone"
    pygame.display.set_caption(name_app)

    # Saber si se establecio la conexion
    while socket.is_flying == False: 
        try:
            socket.connect()
        except Exception as e:
            print("Intentando establecer conexion")
            screen_app.loadScreenApp(win)
        else:
            print("Conexion establecida")

    # pygame.display.update() 

# Funcion para la deteccion de teclas del teclado
def getKey(keyName):
    ans = False

    for eve in pygame.event.get(): pass

    keyInput = pygame.key.get_pressed()

    myKey = getattr(pygame, 'K_{}'.format(keyName))

    # print('K_{}'.format(keyName))

    if keyInput[myKey]:

        ans = True

    pygame.display.update()

    return ans

######## PARAMETROS EMPIRICOS ###########

fSpeed = 40 / 10  # Forward Speed in cm/s   (20 cm/s) 115 / 10

aSpeed = 1800 / 10  # Angular Speed Degrees/s  (45 d/s) 60 gira 30 cada vez

interval = 0.25

dInterval = fSpeed * interval

aInterval = aSpeed * interval

###############################################

x, y = 250, 250

a = 0

yaw = 0

init()