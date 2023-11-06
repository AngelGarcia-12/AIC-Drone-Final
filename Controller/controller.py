from View.main import getKey, dInterval, aInterval, interval
from time import sleep
import math

############################# ENTRADAS DE TECLADO #########################################
def getkeyboardinput():
    lr, fb, ud, yv = 0, 0, 0, 0  # left-right forward-backward up-down yaw-velocity

    speed = 20  # cm/s

    aspeed = 70  # degrees/s 45 gira  cada vez

    global x, y, yaw, a

    d = 0
    ######################### IZQUIERDA #########
    if getKey('LEFT'):

        lr = -speed

        d = dInterval

        a = 180

    ####################### DERECHA ##############
    elif getKey('RIGHT'):

        lr = speed

        d = -dInterval

        a = 180

    ##################### ARRIBA ##################
    if getKey('UP'):

        fb = speed

        d = dInterval

        a = -90

    #################### ABAJO ###################
    elif getKey('DOWN'):

        fb = -speed

        d = -dInterval

        a = -90

    if getKey('w'):

        ud = speed

    elif getKey('s'):

        ud = -speed

    if getKey('a'):

        yv = -aspeed

        yaw -= aInterval

    elif getKey('d'):

        yv = aspeed

        yaw += aInterval

    sleep(interval)

    if yaw > 180:
        yaw = yaw - 360 * (yaw // 180)
    elif yaw < -180:
        yaw = yaw + 360 * (-yaw // 180)

    a += yaw

    x += int(d * math.cos(math.radians(a)))

    y += int(d * math.sin(math.radians(a)))

    return [lr, fb, ud, yv], (x, y), yaw
########################################################################################