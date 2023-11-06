import pygame

# Inicio de la app
def init():

    pygame.init()

    # Display del tamaño de la pantalla
    win = pygame.display.set_mode((200, 200))

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