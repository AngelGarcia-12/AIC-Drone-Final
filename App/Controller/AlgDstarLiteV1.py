# Programa para probar el algoritmo D-StarLite
import pygame

import numpy as np
import math

import time
from djitellopy import tello

import cv2
from d_star_lite import DStarLite
from grid import OccupancyGridMap, SLAM
import os

socket = tello.Tello()
global frame, frameCam

pygame.init()

win = pygame.display.set_mode((200, 200))

# def getkeyboardinput():
#     lr, fb, ud, yv = 0, 0, 0, 0  # left-right forward-backward up-down yaw-velocity

#     speed = 20  # cm/s

#     aspeed = 70  # degrees/s 45 gira  cada vez

#     global yaw, a, x, y

#     d = 0
#     if getKey('LEFT'):

#         lr = -speed

#         d = dInterval

#         a = 180

#     elif getKey('RIGHT'):

#         lr = speed

#         d = -dInterval

#         a = 180

#     if getKey('UP'):

#         fb = speed

#         d = dInterval

#         a = -90

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

#     time.sleep(interval)

#     if yaw > 180:
#         yaw = yaw - 360 * (yaw // 180)
#     elif yaw < -180:
#         yaw = yaw + 360 * (-yaw // 180)

#     a += yaw

#     x += int(d * math.cos(math.radians(a)))

#     y += int(d * math.sin(math.radians(a)))

#     return [lr, fb, ud, yv], (x, y), yaw

def getkeyboardinput():
    lr, fb, ud, yv = 0, 0, 0, 0  # left-right forward-backward up-down yaw-velocity
    d = 0
    global camera, x, y, yaw, a
    speed = 10  # cm/s

    aspeed = 70  # degrees/s 45 gira  cada vez

    ##################### IZQUIERDA ###############
    if getKey('LEFT'):

        lr = -speed
        d = dInterval
        a = -180

    #################### DERECHA ##################
    elif getKey('RIGHT'):

        lr = speed
        d = -dInterval
        a = 180

    #################### ADELANTE ##################
    if getKey('UP'):

        fb = speed
        d = dInterval
        a = -90

    ################### ATRAS #####################
    elif getKey('DOWN'):

        fb = -speed
        d = -dInterval
        a = 270

    #################### ELEVAR ###############
    if getKey('w'):

        ud = speed

    ################### DESCENDER #############
    elif getKey('s'):

        ud = -speed

    ################## GIRAR IZQUIERDA ##########
    if getKey('a'):

        yv = -aspeed
        yaw -= aInterval

    ################# GIRAR DERECHA ##############
    elif getKey('d'):

        yv = aspeed
        yaw += aInterval

    ################ ATERRIZAR ###################
    if getKey('l'):
        socket.land()
        time.sleep(2)

    ############### DESPEGAR #####################
    elif getKey('t'):
        socket.takeoff()
        time.sleep(0.25)

    ############### CAMARA #######################
    elif getKey('c'):
        if camera == 1:
            socket.streamoff()
            camera = 0
        elif camera == 0:
            socket.streamon()
            camera = 1
    
    ################ IA ##########################
    

    ############## FOTO #############################
    elif getKey('f'):
        FOLDER = 'Photos/'
        PICTURE = f'photodrone_{time()}.jpg'
        if not os.path.exists(FOLDER):
            os.makedirs(FOLDER)

        PATH_FILE = os.path.join(os.getcwd(), (FOLDER + PICTURE))
        # cv2.imwrite(f'Fotografias/fotografiadrone{time()}.jpg', frame)
        cv2.imwrite(PATH_FILE, frameCam)
        time.sleep(0.2)

    ################# DESCONECTAR ###################
    elif getKey('q'):
        # np.save('datos/posicion.npy', pos)
        # np.save('datos/angulo.npy', yaw)
        # np.save('datos/recorrido.npy', points)
        socket.end()
    
    ################ SALIR DE LA APP #################
    elif getKey('e'):
        pygame.quit()

    time.sleep(0.25)

    if yaw > 180:
        yaw = yaw - 360 * (yaw // 180)
    elif yaw < -180:
        yaw = yaw + 360 * (-yaw // 180)

    a += yaw

    x += int(d * math.cos(math.radians(a)))

    y += int(d * math.sin(math.radians(a)))

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
# --------------- Limite de rango para el dron ----------------------#
LIMIT = 230
# -------------------------------------------------------------------#

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

    # for point in obstaculos:

    #     cv2.circle(img, tuple(point), 1, (10, 130, 240), cv2.FILLED)
        # bgr color

    cv2.putText(img, f'({round((points[-1][0] - 250)/10, 2)},{round((-points[-1][1] + 250)/10, 2)}) m {angulo}gr',
                (points[-1][0] + 3, points[-1][1] + 5), cv2.FONT_HERSHEY_PLAIN, 0.75, (255, 0, 70), 1)

    if pos[1] <= LIMIT+1:
        text_size = cv2.getTextSize("Alcanzo el limite", cv2.FONT_HERSHEY_SIMPLEX, 0.85, 2)[0]
        text_x = (500 - text_size[0]) // 2
        text_y = 50
        cv2.putText(img, "Alcanzo el limite", (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.85, (0, 0, 255), 2)
        # reprodAlarm()
        
    # if pos[1] >= LIMIT:
    #     reprodAlarm()

    if modo == 1:
        for point in path:
            cv2.circle(img, point, 1, (130, 130, 240), cv2.FILLED)
    cv2.drawMarker(img, pos, (255, 255, 255), cv2.MARKER_STAR, 6, 1)

path = []
destm = []
destpx = []
i = 0
try:
    socket.connect()
    while True:
        [vals, pos, yaw] = getkeyboardinput()
        socket.send_rc_control(vals[0], vals[1], vals[2], vals[3])
        # Valor de Y (arriba) va disminuyendo cuando se mueve
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

                # pf.replan()                # path=pf.get_path()
                # Marca el destino
            i += 1
            if i % 50 == 0:
                obstaculos = np.unique(obstaculos, axis=0)
            lastpos = pos

            # print(pos)
            if len(path) == 1 or 0:
                print("Ha llegado a su destino, aterrice")
            else:
                pos = path[1]
                posPath = path[1]
                socket.send_rc_control(vals[0], -10, vals[2], vals[3])
        elif (pos[0] <= LIMIT and vals[0] >= 10) or pos[0] <= LIMIT:
            print("Alcanzo el limite")
            socket.send_rc_control(-20, vals[1], vals[2], vals[3])

        # if vals[0] != 0 or vals[1] != 0 or vals[2] != 0 or vals[3] != 0:
        #     socket.send_rc_control(vals[0], vals[1], vals[2], vals[3])
        time.sleep(0.15)
        mapeado = np.zeros((500, 500, 3), np.uint8)
        # if posControl != 0:
        #     pos = posControl
        # if getKey('m'):
        #     if modo == 0:
        #         path = []
        #         destm = []
        #         destpx = []
        #         i = 0
        #         print('Cambiado a modo automatico')
        #     modo = not modo

        # if getKey('r'):
        #     points = [(0, 0), (0, 0)]


        # # if modo == 0:
        # #     [vals, pos, yaw] = Manual0.getkeyboardinput()
        # #     time.sleep(0.2)
        # elif modo == 1:
        #     print("pos i: ", pos)
        #     # pos = posPath
        #     # print("points: ", points)
        #     if i == 0:

        #         print("Escriba las coordenadas (x,y) de destino en metros con precision de 2 decimales")
        #         n = float(input("Coordenada x = "))  # metros
        #         z = float(input("Coordenada y = "))
        #         destm = (n, z)
        #         destpx = convdist(destm)

        #         slam = SLAM(map=map, view_range=view_range)
        #         new_observation = {"pos": None, "type": None}
        #         dstar = DStarLite(map, pos, destpx)
        #         path, g, rhs = dstar.move_and_replan(robot_position=pos)
        #         c = len(path)
        #         # print("Path: ",path)

        #     if new_observation is not None:
        #         old_map = map
        #         slam.set_ground_truth_map(gt_map=map)


        #     if pos != lastpos:
        #         lastpos = pos

        #         # slam

        #         new_edges_and_old_costs, slam_map = slam.rescan(global_position=pos)
        #         dstar.new_edges_and_old_costs = new_edges_and_old_costs
        #         dstar.sensed_map = slam_map

        #         # d star
        #         path, g, rhs = dstar.move_and_replan(robot_position=pos)
        #         c2 = len(path)
        #         print("Path2: ",path)

        #     # pf.replan()
        #     # path=pf.get_path()
        #     # Marca el destino
        #     cv2.drawMarker(mapeado, destpx, (150, 230, 150), cv2.MARKER_DIAMOND, 6, 1)
        #     cv2.putText(mapeado, f'({round(destm[0] , 2)},{round(destm[1] , 2)},) m ',
        #                 (destpx[0] + 5, destpx[1] + 10), cv2.FONT_HERSHEY_PLAIN, 0.75, (150, 230, 150), 1)
        #     i += 1
        #     if i % 50 == 0:
        #         obstaculos = np.unique(obstaculos, axis=0)
        #     lastpos = pos
        #     #print(i)

        #     if len(path) == 1 or 0:
        #         # if pos[1] <= 220:
        #         #     x = 0
        #         #     y = -3
        #         #     destm = (x, y)
        #         #     destpx = convdist(destm)

        #         #     slam = SLAM(map=map, view_range=view_range)
        #         #     new_observation = {"pos": None, "type": None}
        #         #     dstar = DStarLite(map, pos, destpx)
        #         #     path, g, rhs = dstar.move_and_replan(robot_position=pos)
        #         #     c = len(path)
        #         #     print("Path: ",path)
        #         print(pos)
        #         print("Ha llegado a su destino, aterrice")
        #     else:
        #         # pos = path[1]
        #         # posPath = path[1]
        #         time.sleep(0.25)
        if points[-1][0] != pos[0] or points[-1][1] != pos[1]:
            points.append(pos)
        # Mapeado
        drawpoints(mapeado, points, pos, obstaculos, yaw, modo)
        cv2.imshow('Mapeado', mapeado)

        cv2.waitKey(1)

        if getKey('q'):
            cv2.imwrite(f'Mapeado/mapeadofinal{time.time()}.jpg', mapeado)
            time.sleep(0.2)
            print('¡Hasta la proxima')
            break

        # cv2.waitKey(1)

    # Clean up
    cv2.destroyAllWindows()
except Exception as e:
    print("No se pudo hacer la conexion")
    print(e)