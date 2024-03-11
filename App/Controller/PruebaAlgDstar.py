# Programa para probar el algoritmo D-StarLite
import pygame

import numpy as np
import math

import time

import cv2
from d_star_lite import DStarLite
from grid import OccupancyGridMap, SLAM

pygame.init()

win = pygame.display.set_mode((200, 200))

def getkeyboardinput():
    lr, fb, ud, yv = 0, 0, 0, 0  # left-right forward-backward up-down yaw-velocity

    speed = 20  # cm/s

    aspeed = 70  # degrees/s 45 gira  cada vez

    global yaw, a, x, y

    d = 0
    if getKey('LEFT'):

        lr = -speed

        d = dInterval

        a = 180

    elif getKey('RIGHT'):

        lr = speed

        d = -dInterval

        a = 180

    if getKey('UP'):

        fb = speed

        d = dInterval

        a = -90

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

    time.sleep(interval)

    if yaw > 180:
        yaw = yaw - 360 * (yaw // 180)
    elif yaw < -180:
        yaw = yaw + 360 * (-yaw // 180)

    a += yaw

    x += int(d * math.cos(math.radians(a)))

    y += int(d * math.sin(math.radians(a)))

    return [lr, fb, ud, yv], (x, y), yaw

def simulGetKeyboardInput(tecla):
    lr, fb, ud, yv = 0, 0, 0, 0  # left-right forward-backward up-down yaw-velocity

    speed = 20  # cm/s

    aspeed = 70  # degrees/s 45 gira  cada vez

    global yaw, a, x, y

    d = 0
    if tecla == 'LEFT':

        lr = -speed

        d = dInterval

        a = 180

    elif tecla == 'RIGHT':

        lr = speed

        d = -dInterval

        a = 180

    if tecla == 'UP':

        fb = speed

        d = dInterval

        a = -90

    elif tecla == 'DOWN':

        fb = -speed

        d = -dInterval

        a = -90

    time.sleep(interval)

    if yaw > 180:
        yaw = yaw - 360 * (yaw // 180)
    elif yaw < -180:
        yaw = yaw + 360 * (-yaw // 180)

    a += yaw

    x += int(d * math.cos(math.radians(a)))

    y += int(d * math.sin(math.radians(a)))

    return [lr, fb, ud, yv], (x, y), yaw

def resetgetkeyboardinput():
    lr, fb, ud, yv = 0, 0, 0, 0  # left-right forward-backward up-down yaw-velocity

    speed = 20  # cm/s

    aspeed = 70  # degrees/s 45 gira  cada vez

    d = 0
    x, y = 250, 250
    yaw = 0

    return [lr, fb, ud, yv], (x, y), yaw

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

# Valores iniciales del drone
x, y = 250, 250  # posicion inicial
yaw = 0 # angulo inicial
OBSTACLE = 255
UNOCCUPIED = 0

x_dim = 500
y_dim = 500
start = (x, y)
destpx = (500, 500)
view_range = 5
map = OccupancyGridMap(x_dim, y_dim, '8N')
points = [(0, 0),(0, 0)]
modo = 0
obstaculos = []
interval = 0.25
fSpeed = 40 / 10  # Forward Speed in cm/s   (20 cm/s) 115 / 10
aSpeed = 1800 / 10  # Angular Speed Degrees/s  (45 d/s) 60 gira 30 cada vez
dInterval = fSpeed * interval
aInterval = aSpeed * interval

for j in range(10):
    for p in range(-3, 3):
        map.set_obstacle((225 + 10 - j + p, 225 + 5 + j))
        obstaculos.append((225 + 10 - j + p, 225 + 5 + j))
for j in range(10):
    for p in range(-3, 3):
        map.set_obstacle((200 + 10 - j + p, 200 + 5 + j))
        obstaculos.append((200 + 10 - j + p, 200 + 5 + j))

for j in range(5):
        map.set_obstacle((j, j))
        obstaculos.append((j , j))

for j in range(10):
    for p in range(-3, 3):
        map.set_obstacle((225 + 10 + j + p, 225 + 5 - j))
        obstaculos.append((225 + 10 + j + p, 225 + 5 - j))
for j in range(10):
    for p in range(-3, 3):
        map.set_obstacle((225 + 10 + j - p, 225 + 5 + j))
        obstaculos.append((225 + 10 + j - p, 225 + 5 + j))
for j in range(10):
    for p in range(-3, 3):
        map.set_obstacle((300 + 10 + j + p, 100 + 5 - j))
        obstaculos.append((300 + 10 + j + p, 100 + 5 - j))
for j in range(10):
    for p in range(-3, 3):
        map.set_obstacle((225 + 10 + j + p, 225 + 5 - j))
        obstaculos.append((225 + 10 + j + p, 225 + 5 - j))
for j in range(10):
    for p in range(-3, 3):
        map.set_obstacle((210 + 10 + j + p, 300 + 5 - j))
        obstaculos.append((210 + 10 + j + p, 300 + 5 - j))
for j in range(10):
    for p in range(-3, 3):
        map.set_obstacle((260 + 10 + j + p, 270 + 5 - j))
        obstaculos.append((260 + 10 + j + p, 270 + 5 - j))

for j in range(10):
    for p in range(-3, 3):
        map.set_obstacle((225 + 10 + j + p, 225 + 5 - j))
        obstaculos.append((225 + 10 + j + p, 225 + 5 - j))
i = 0
a = 0
pos = (250, 250)
posPath = (250, 250)
lastpos = (x-1, y-1)
slam = SLAM(map=map, view_range=view_range)
new_observation = {"pos": None, "type": None}
def convdist(posicion, modo=0):
    """
    modo 0 es m a px """
    nposicion = []
    if modo == 0:  # Convertir de m a px del mapeado
        nposicion.append(int(posicion[0]*100/10+250))
        nposicion.append(int(round(250-posicion[1] * 100 / 10)))

    elif modo == 1: #convertir px del mapeado a m
        nposicion.append(round((posicion[0]-250)*10/100, 2))
        nposicion.append(round(-(posicion[1]-250)*10/100, 2))
    npos=(nposicion[0], nposicion[1])
    return npos

def reprodAlarm():
    pygame.mixer.init()
    pygame.mixer.music.load("App/Model/sounds/alarma.mp3")
    pygame.mixer.music.play(20)

def drawpoints(img, points, pos, obstaculos, angulo=0.0, modo = 0):
    global path
    for point in points:

        cv2.circle(img, point, 1, (240, 240, 240), cv2.FILLED)  # bgr color

    for point in obstaculos:

        cv2.circle(img, tuple(point), 1, (10, 130, 240), cv2.FILLED)
        # bgr color

    cv2.putText(img, f'({round((points[-1][0] - 250)/10, 2)},{round((-points[-1][1] + 250)/10, 2)}) m {angulo}gr',
                (points[-1][0] + 3, points[-1][1] + 5), cv2.FONT_HERSHEY_PLAIN, 0.75, (255, 0, 70), 1)
    
    # Alerta sobre posible perdida de señal
    if pos[1] <= 233:
        text_size = cv2.getTextSize("Alcanzo el limite", cv2.FONT_HERSHEY_SIMPLEX, 0.85, 2)[0]
        text_x = (500 - text_size[0]) // 2
        text_y = 50
        cv2.putText(img, "Alcanzo el limite", (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.85, (0, 0, 255), 2)
    # elif pos[1] >= 230:
    #     reprodAlarm()
    if modo == 1:
        for point in path:
            cv2.circle(img, point, 1, (130, 130, 240), cv2.FILLED)
    cv2.drawMarker(img, pos, (255, 255, 255), cv2.MARKER_STAR, 6, 1)

LIMIT = 230
path = []
destm = []
destpx = []
running_again = False
i = 0
while True:
    [vals, pos, yaw] = getkeyboardinput()
    mapeado = np.zeros((500, 500, 3), np.uint8)
    # socket.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    # Valor de Y (arriba) va disminuyendo cuando se mueve
    if running_again == True:
        pos = posNew
        path = []
        running_again = False
        print('Pos Again: ', pos)

    if (pos[1] <= LIMIT and vals[1] >= 10) or pos[1] <= LIMIT or len(path) >= 1:
        print("Alcanzo el limite")
        # socket.send_rc_control(vals[0], -1, vals[2], vals[3])    
        print("Pos: ", pos)
        if i == 0:
            posPath = (pos[0],LIMIT)
        pos = posPath
        if i == 0:
            n = 0.0
            z = -2.0
            destm = (n, z)
            destpx = convdist(destm)
            slam = SLAM(map=map, view_range=view_range)
            new_observation = {"pos": None, "type": None}
            dstar = DStarLite(map, pos, destpx)
            path, g, rhs = dstar.move_and_replan(robot_position=pos)
            c = len(path)
            print("Path: ",path)

        if new_observation is not None:
            old_map = map
            slam.set_ground_truth_map(gt_map=map)

        if pos != lastpos:
            lastpos = pos

            # slam

            new_edges_and_old_costs, slam_map = slam.rescan(global_position=pos)
            dstar.new_edges_and_old_costs = new_edges_and_old_costs
            dstar.sensed_map = slam_map

            # d star
            path, g, rhs = dstar.move_and_replan(robot_position=pos)
            c2 = len(path)
            # print("Path2: ",path)

            # pf.replan()
            # path=pf.get_path()
            # Marca el destino
        i += 1
        if i % 50 == 0:
            obstaculos = np.unique(obstaculos, axis=0)
        lastpos = pos

        # print(pos)
        if len(path) == 1 or 0:
            print("Ha llegado a su destino, aterrice")
            cv2.destroyAllWindows()
            points = [(0, 0),(0, 0)]
            destm = []
            destpx = []
            i = 0
            # [vals, pos, yaw] = resetgetkeyboardinput()
            running_again = True
        else:
            pos = path[1]
            posPath = path[1]
            if len(path) != 1:
                [vals, posNew, yaw] = simulGetKeyboardInput('DOWN')
                print("Pos New: ", posNew)
            if pos[0] > 250 and posNew[0] > 250:
                [vals, posNew, yaw] = simulGetKeyboardInput('LEFT')
    elif (pos[0] <= LIMIT and vals[0] >= 10) or pos[0] <= LIMIT:
        print("Alcanzo el limite")
    
    if points[-1][0] != pos[0] or points[-1][1] != pos[1]:
        points.append(pos)

    # Mapeado
    # drawpoints(mapeado, points, pos, obstaculos, yaw, modo)
    drawpoints(mapeado, points, pos, obstaculos, yaw, 1)
    cv2.imshow('Mapeado', mapeado)

    if getKey('q'):
        cv2.imwrite(f'Mapeado/mapeadofinal{time.time()}.jpg', mapeado)
        time.sleep(0.2)
        print('¡Hasta la proxima')
        break

    cv2.waitKey(1)

# Clean up
cv2.destroyAllWindows()