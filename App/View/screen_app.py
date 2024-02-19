import pygame
from time import sleep, time
import math
from djitellopy import tello
import cv2
from controller import *
from d_star_lite import DStarLite, convdist
from grid import OccupancyGridMap, SLAM
import numpy as np
import os

socket = tello.Tello()
global frame, frameCam

# Valores iniciales del drone

x, y = 250, 250 #Posicion inicial
a = 0
i = 0
yaw = 0 #Angulo inicial
x_dim = 500
y_dim = 500
start = (x, y)
destpx = (500, 500)
view_range = 5
map = OccupancyGridMap(x_dim, y_dim, '8N')
points = [(0, 0), (0, 0)]
modo = 0
pos = (250, 250)
posPath = (250, 250)
lastpos = (x-1, y-1)
slam = SLAM(map=map, view_range=view_range)
new_observation = {"pos": None, "type": None}
path = []
# --------------- Limite de rango para el dron ----------------------#
LIMIT_EXAMPLE = 230
LIMIT = 50
# ------------------------- Constantes ------------------------------#
OBSTACLE = 255
UNOCCUPIED = 0
# -------------------------------------------------------------------#

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
        sleep(2)

    ############### DESPEGAR #####################
    elif getKey('t'):
        socket.takeoff()
        sleep(0.25)

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
        frameCam = socket.get_frame_read().frame
        cv2.imwrite(PATH_FILE, frameCam)
        sleep(0.2)

    ################# DESCONECTAR ###################
    elif getKey('q'):
        # np.save('datos/posicion.npy', pos)
        # np.save('datos/angulo.npy', yaw)
        # np.save('datos/recorrido.npy', points)
        socket.end()
    
    ################ SALIR DE LA APP #################
    elif getKey('e'):
        pygame.quit()

    sleep(0.25)

    if yaw > 180:
        yaw = yaw - 360 * (yaw // 180)
    elif yaw < -180:
        yaw = yaw + 360 * (-yaw // 180)

    a += yaw

    x += int(d * math.cos(math.radians(a)))

    y += int(d * math.sin(math.radians(a)))

    return [lr, fb, ud, yv], (x, y), yaw

# Alarma de deteccion de perdidad de señal
def reprodAlarm():
    pygame.mixer.init()
    pygame.mixer.music.load("App/Model/sounds/alarma.mp3")
    pygame.mixer.music.play(20)

def drawpoints(img, points, pos, angulo=0.0, modo = 0):
    global path

    for point in points:

        cv2.circle(img, point, 1, (240, 240, 240), cv2.FILLED)  # bgr color circulos blancos


    cv2.putText(img, f'({round((points[-1][0] - 250)/10, 2)},{round((-points[-1][1] + 250)/10, 2)},{socket.get_height()/100}) m {angulo}gr',
                (points[-1][0] + 3, points[-1][1] + 5), cv2.FONT_HERSHEY_PLAIN, 0.75, (255, 50, 0), 1)
    # Alerta sobre posible perdida de señal
    if pos[1] <= LIMIT_EXAMPLE+3:
        text_size = cv2.getTextSize("Alcanzo el limite", cv2.FONT_HERSHEY_SIMPLEX, 0.85, 2)[0]
        text_x = (500 - text_size[0]) // 2
        text_y = 50
        cv2.putText(img, "Alcanzo el limite", (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.85, (0, 0, 255), 2)
    # elif pos[1] >= LIMIT:
    #     reprodAlarm()

    if modo == 1:
        for point in path:
            cv2.circle(img, point, 1, (130, 130, 240), cv2.FILLED)

    cv2.drawMarker(img, pos, (245, 170, 0), cv2.MARKER_STAR, 6, 1) # Estrella azul (255,0,0)

def loadScreenApp(win):
    font = pygame.font.Font("App/Model/images/icon/sarpanch/Sarpanch-Medium.ttf", 50)
    dot_count = 0
    dot_animation_timer = pygame.time.get_ticks()

    # Cargar una imagen
    image = pygame.image.load('App/Model/images/icon/ScreenAppLoading.png')

    # Bucle principal
    clock = pygame.time.Clock()
    running = True
    flag = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        win.fill((0, 0, 0))  # Limpiar la pantalla

        # Mostrar la imagen
        win.blit(image, (0, 0))

        # Mostrar el texto "Cargando" con los puntos adicionales
        current_time = pygame.time.get_ticks()
        if current_time - dot_animation_timer > 500:  # Agregar un punto cada segundo
            dot_count = (dot_count + 1) % 4  # Ajustar la cantidad de puntos
            dot_animation_timer = current_time
    
        loading_dots = '.' * dot_count
        text_with_dots = font.render('Estableciendo conexion' + loading_dots, True, (255, 255, 255))
    
        # Centrar el texto en la pantalla
        text_rect = text_with_dots.get_rect(center=win.get_rect().center)
        win.blit(text_with_dots, text_rect.topleft)
    
        pygame.display.flip()
        clock.tick(20)  # Controlar la velocidad de la animación

        flag += 1

        if flag == 80: # Si pasaron 3 seg
            running = False

pygame.quit()

def cameraScreen(win, path, destm, destpx, obstaculos):
    SIZE_WIDTH = 50
    SIZE_HEIGH = 50
    i = 0
    lastpos = (x-1, y-1)

    # Mostrar info de la bateria
    font = pygame.font.Font("App/Model/images/icon/sarpanch/Sarpanch-Medium.ttf", 20)

    # Botones
    btn_up = pygame.image.load('App/Model/images/buttons/button-up.png')
    btn_bottom = pygame.image.load('App/Model/images/buttons/button-bottom.png')
    btn_left = pygame.image.load('App/Model/images/buttons/button-left.png')
    btn_right = pygame.image.load('App/Model/images/buttons/button-right.png')
    btn_takeoff = pygame.image.load('App/Model/images/buttons/takeoff-dron.png')
    btn_land = pygame.image.load('App/Model/images/buttons/land-dron.png')
    btn_takeoff_key = pygame.image.load('App/Model/images/buttons/key-t.png')
    btn_land_key = pygame.image.load('App/Model/images/buttons/key-l.png')

    # Cambiar tamano
    icon_btn_up = pygame.transform.scale(btn_up, (SIZE_WIDTH, SIZE_HEIGH))
    icon_btn_bottom = pygame.transform.scale(btn_bottom, (SIZE_WIDTH, SIZE_HEIGH))
    icon_btn_left = pygame.transform.scale(btn_left, (SIZE_WIDTH, SIZE_HEIGH))
    icon_btn_right = pygame.transform.scale(btn_right, (SIZE_WIDTH, SIZE_HEIGH))
    icon_btn_takeoff = pygame.transform.scale(btn_takeoff, (SIZE_WIDTH+20, SIZE_HEIGH+20))
    icon_btn_land = pygame.transform.scale(btn_land, (SIZE_WIDTH, SIZE_HEIGH))
    icon_btn_takeoff_key = pygame.transform.scale(btn_takeoff_key, (SIZE_WIDTH+48, SIZE_HEIGH+8))# 40px de diferencia
    icon_btn_land_key = pygame.transform.scale(btn_land_key, (SIZE_WIDTH-12, SIZE_HEIGH-12))

    # Obtener los rectángulos de las imágenes para su posicionamiento
    button_up_rect = icon_btn_up.get_rect()
    button_down_rect = icon_btn_bottom.get_rect()
    button_left_rect = icon_btn_left.get_rect()
    button_right_rect = icon_btn_right.get_rect()
    buttom_takeoff_rect = icon_btn_takeoff.get_rect()
    buttom_land_rect = icon_btn_land.get_rect()
    buttom_takeoff_key_rect = icon_btn_takeoff_key.get_rect()
    buttom_land_key_rect = icon_btn_land_key.get_rect()

    # Posicionar los botones en la esquina inferior derecha
    button_down_rect.bottomright = (800 - 60, 600 - 20)
    button_right_rect.bottomright = (800 - 20, 600 - 60)
    button_up_rect.bottomright = (800 - 60, 600 - 100)
    button_left_rect.bottomright = (800 - 100, 600 - 60)
    buttom_takeoff_rect.center = (350, 20)
    buttom_land_rect.center = (450, 20)
    buttom_takeoff_key_rect.center = (350, 20)
    buttom_land_key_rect.center = (450, 20)

    # Hacer que parpadee el boton al pulsarlo
    clock = pygame.time.Clock()
    visible = True
    interval = 500  # Intervalo de tiempo para el parpadeo en milisegundos
    last_toggle = pygame.time.get_ticks()

    # Saber si se establecio la conexion
    while socket.is_flying == False: 
        try:
            socket.connect()
            socket.streamon()
            camera = 1

            while True:
                [vals, pos, yaw]=getkeyboardinput()
                # vals = getkeyboardinput()
                socket.send_rc_control(vals[0], vals[1], vals[2], vals[3])
                sleep(0.15)
                if camera == 1:
                    frame = socket.get_frame_read().frame
                    frameCam = socket.get_frame_read().frame
                    # img = cv2.resize(frame, (600, 400))
                    # cv2.imshow("DJI TELLO", img)
                    win.fill((0,0,0))  # Limpiar la pantalla
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame = np.rot90(frame)
                    frame = pygame.surfarray.make_surface(frame)
                    win.blit(frame,(0,0))

                """
                    ################## MAPEADO #################
                """
                # print(points)
                # mapeado = np.zeros((500, 500, 3), np.uint8)
                
                # if points[-1][0] != pos[0] or points[-1][1] != pos[1]:
                #     points.append(pos)
                # # Mapeado
                # drawpoints(mapeado, points, pos, yaw, modo)
                # cv2.imshow('Mapping', mapeado)

                #LIMIT es una constante que representa el limite permitido
                mapeado = np.zeros((500, 500, 3), np.uint8)
                print(pos)

                # Movimiento en direccion y (adelante)
                if (pos[1] <= LIMIT_EXAMPLE and vals[1] >= 10) or pos[1] <= LIMIT_EXAMPLE or len(path) >= 1:
                    print("Alcanzo el limite")
                    # socket.send_rc_control(vals[0], -20, vals[2], vals[3])
                    if i > 3:
                        socket.send_rc_control(vals[0],vals[1], vals[2], vals[3]) 
                    else:   
                        socket.send_rc_control(vals[0], -20, vals[2], vals[3])    
                    print("Pos: ", pos)
                    if i == 0:
                        posPath = (pos[0],LIMIT_EXAMPLE)
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
                    else:
                        pos = path[1]
                        posPath = path[1]
                # Movimiento en direccion x (derecha)
                elif (pos[0] <= LIMIT_EXAMPLE and vals[0] >= 10) or pos[0] <= LIMIT_EXAMPLE:
                    print("Alcanzo el limite")

                if points[-1][0] != pos[0] or points[-1][1] != pos[1]:
                    points.append(pos)

                drawpoints(mapeado, points, pos, yaw, 1)
                cv2.imshow('Mapeado', mapeado)
                
                """
                    #################### MAPEADO ###################
                """

                cv2.waitKey(1)

                # Porcentaje de la bateria
                text = font.render(f"bateria: {socket.get_battery()}%", True, (255,225,255))

                # Posicionar el texto en la esquina superior izquierda (coordenadas 0, 0)
                text_rect = text.get_rect(topleft=(0, 0))
                # win.blit(text, text_rect)  # Mostrar el texto en la posición especificada

                current_time = pygame.time.get_ticks()
                if current_time - last_toggle > interval:
                    visible = not visible
                    last_toggle = current_time

                # Mostrar u ocultar la imagen dependiendo del estado visible
                if visible and getKey('UP'):
                    win.blit(icon_btn_up, button_up_rect)
                elif visible and getKey('DOWN'):
                    win.blit(icon_btn_bottom, button_down_rect)
                elif visible and getKey('LEFT'):
                    win.blit(icon_btn_left, button_left_rect)
                elif visible and getKey('RIGHT'):
                    win.blit(icon_btn_right, button_right_rect)
                elif visible and getKey('t'):
                    win.blit(icon_btn_takeoff, buttom_takeoff_rect)
                elif visible and getKey('l'):
                    win.blit(icon_btn_land, buttom_land_rect)
                else:
                    win.blit(icon_btn_up, button_up_rect)
                    win.blit(icon_btn_bottom, button_down_rect)
                    win.blit(icon_btn_left, button_left_rect)
                    win.blit(icon_btn_right, button_right_rect)
                    win.blit(icon_btn_takeoff_key, buttom_takeoff_key_rect)
                    win.blit(icon_btn_land_key, buttom_land_key_rect)

                win.blit(text, text_rect)  # Mostrar el texto en la posición especificada

                pygame.display.flip() 
                clock.tick(20)  # Controlar la velocidad del bucle

            # Clean up
            cv2.destroyAllWindows()
        except Exception as e:
            print("Intentando establecer conexion")
            loadScreenApp(win)
            print(e)
        else:
            print("Conexion establecida")