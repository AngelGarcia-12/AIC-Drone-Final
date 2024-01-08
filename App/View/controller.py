from time import sleep
import pygame

############################# ENTRADAS DE TECLADO #########################################
# def getkeyboardinput():
#     lr, fb, ud, yv = 0, 0, 0, 0  # left-right forward-backward up-down yaw-velocity

#     speed = 20  # cm/s

#     aspeed = 70  # degrees/s 45 gira  cada vez

#     global x, y, yaw, a

#     d = 0
#     ######################### IZQUIERDA #########
#     if getKey('LEFT'):

#         lr = -speed

#         d = dInterval

#         a = 180

#     ####################### DERECHA ##############
#     elif getKey('RIGHT'):

#         lr = speed

#         d = -dInterval

#         a = 180

#     ##################### ARRIBA ##################
#     if getKey('UP'):

#         fb = speed

#         d = dInterval

#         a = -90

#     #################### ABAJO ###################
#     elif getKey('DOWN'):

#         fb = -speed

#         d = -dInterval

#         a = -90

#     if getKey('w'):

#         ud = speed

#     elif getKey('s'):

#         ud = -speed

#     if getKey('a'):

#         yv = -aspeed

#         yaw -= aInterval

#     elif getKey('d'):

#         yv = aspeed

#         yaw += aInterval

#     sleep(interval)

#     if yaw > 180:
#         yaw = yaw - 360 * (yaw // 180)
#     elif yaw < -180:
#         yaw = yaw + 360 * (-yaw // 180)

#     a += yaw

#     x += int(d * math.cos(math.radians(a)))

#     y += int(d * math.sin(math.radians(a)))

#     return [lr, fb, ud, yv], (x, y), yaw
########################################################################################

# Funcion para deteccion de teclado
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

# Valores iniciales del dron
# x, y = 250, 250
# a = 0
# yaw = 0

###############################################
################# POSICION INICIAL EN MAPEADO #################

# pos = (250, 250)
# points = [(0, 0),(0, 0)]

###############################################################