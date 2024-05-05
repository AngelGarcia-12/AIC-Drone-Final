# Programa para probar el algoritmo D-StarLite
from d_star_lite import DStarLite
from djitellopy import tello
from grid import OccupancyGridMap, SLAM
import cv2
import math
import numpy as np
import os
import pygame
import time

socket = tello.Tello()

#! ############ DECLARACION DE VARIABLES ############ !#
# Valores iniciales del drone
x, y = 250, 250  # posicion inicial
yaw = 0 # angulo inicial
OBSTACLE = 255
UNOCCUPIED = 0

#!##################### LIMITES ######################!#

LIMIT_YP_EXAMPLE = 230
LIMIT_YM_EXAMPLE = 270
LIMIT_XP_EXAMPLE = 230
LIMIT_XM_EXAMPLE = 270

 #!####################################################!#

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
posNew = (250, 250)
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

def reprodAlarm( flag ):
    pygame.mixer.init()
    pygame.mixer.music.load("App/Model/sounds/alarma.mp3")
    pygame.mixer.music.play(20)

    if flag == True:
        pygame.mixer.music.stop()

def drawpoints(img, points, pos, obstaculos, angulo=0.0, modo = 0):
    global path
    flag = False

    for point in points:
        cv2.circle(img, point, 1, (240, 240, 240), cv2.FILLED)  # bgr color
    for point in obstaculos:
        cv2.circle(img, tuple(point), 1, (10, 130, 240), cv2.FILLED)
        # bgr color
    cv2.putText(img, f'({round((points[-1][0] - 250)/10, 2)},{round((-points[-1][1] + 250)/10, 2)}) m {angulo}gr',
                (points[-1][0] + 3, points[-1][1] + 5), cv2.FONT_HERSHEY_PLAIN, 0.75, (255, 0, 70), 1)
    
    # Alerta sobre posible perdida de señal
    if pos[1] <= LIMIT_YP_EXAMPLE + 3:
        text_size = cv2.getTextSize("Alcanzo el limite", cv2.FONT_HERSHEY_SIMPLEX, 0.85, 2)[0]
        text_x = (500 - text_size[0]) // 2
        text_y = 50
        cv2.putText(img, "Alcanzo el limite", (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.85, (0, 0, 255), 2)
        reprodAlarm(flag)
    elif pos[1] >= LIMIT_YM_EXAMPLE - 3:
        text_size = cv2.getTextSize("Alcanzo el limite", cv2.FONT_HERSHEY_SIMPLEX, 0.85, 2)[0]
        text_x = (500 - text_size[0]) // 2
        text_y = 50
        cv2.putText(img, "Alcanzo el limite", (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.85, (0, 0, 255), 2)
        reprodAlarm(flag)
    elif pos[0] <= LIMIT_XP_EXAMPLE + 3:
        text_size = cv2.getTextSize("Alcanzo el limite", cv2.FONT_HERSHEY_SIMPLEX, 0.85, 2)[0]
        text_x = (500 - text_size[0]) // 2
        text_y = 50
        cv2.putText(img, "Alcanzo el limite", (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.85, (0, 0, 255), 2)
        reprodAlarm(flag)
    elif pos[0] >= LIMIT_XM_EXAMPLE - 3:
        text_size = cv2.getTextSize("Alcanzo el limite", cv2.FONT_HERSHEY_SIMPLEX, 0.85, 2)[0]
        text_x = (500 - text_size[0]) // 2
        text_y = 50
        cv2.putText(img, "Alcanzo el limite", (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX,
                        0.85, (0, 0, 255), 2)
        reprodAlarm(flag)
    else:
        flag = True
        reprodAlarm( flag ) 
    # elif pos[1] >= 230:
    #     reprodAlarm()
    if modo == 1:
        for point in path:
            cv2.circle(img, point, 1, (130, 130, 240), cv2.FILLED)
    cv2.drawMarker(img, pos, (255, 255, 255), cv2.MARKER_STAR, 6, 1)

# LIMIT = 230
path = []
destm = []
destpx = []
running_again = False

FLAG_XP = False
FLAG_YP = False
FLAG_XM = False
FLAG_YM = False

i = 0

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
        time.sleep(0.2)

    ################# DESCONECTAR ###################
    elif getKey('q'):
        # np.save('datos/posicion.npy', pos)
        # np.save('datos/angulo.npy', yaw)
        # np.save('datos/recorrido.npy', points)
        socket.end()
    
    ################ SALIR DE LA APP #################
    elif getKey('e'):
        cv2.destroyAllWindows()
        pygame.display.quit()
        socket.end()
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

def simulGetKeyboardInput(tecla):
    lr, fb, ud, yv = 0, 0, 0, 0  # left-right forward-backward up-down yaw-velocity
    speed = 10  # cm/s
    aspeed = 70  # degrees/s 45 gira  cada vez
    global yaw, a, x, y
    d = 0

    if tecla == 'LEFT':
        lr = -speed
        d = dInterval
        a = -180

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
        a = 270

    time.sleep(interval)

    if yaw > 180:
        yaw = yaw - 360 * (yaw // 180)
    elif yaw < -180:
        yaw = yaw + 360 * (-yaw // 180)

    a += yaw

    x += int(d * math.cos(math.radians(a)))

    y += int(d * math.sin(math.radians(a)))

    return [lr, fb, ud, yv], (x, y), yaw

# Funcion para detectar tecla presionada
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

def loadScreenApp(win):
    global font

    font = pygame.font.Font("App/Model/images/icon/sarpanch/Sarpanch-Medium.ttf", 50)
    dot_count = 0
    dot_animation_timer = pygame.time.get_ticks()

    # Cargar una imagen
    image = pygame.image.load('App/View/images/icon/ScreenAppLoading.png')

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
            socket.end()
            break

pygame.quit()

def gamepadDrone():
    # Inicializar pygame
    pygame.init()

    # Inicializar el joystick
    pygame.joystick.init()

    # Comprobar si hay joysticks disponibles
    if pygame.joystick.get_count() == 0:
        print("No se encontraron joysticks disponibles.")

    # Seleccionar el primer joystick disponible
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print("Nombre del joystick:", joystick.get_name())

    joystick.init()

    # Display del tamaño de la pantalla
    WIDTH_SCREEN = 800
    HIGTH_SCREEN = 600

    win = pygame.display.set_mode((WIDTH_SCREEN, HIGTH_SCREEN))

    try:
        # Establecer icono para app
        # icon = pygame.image.load("App/Model/images/icon/logodron-1.png")
        icon = pygame.image.load("App/View/images/icon/logodron-1.png")
        pygame.display.set_icon(icon)
    except Exception as e:
        print(e)
        icon = pygame.image.load("App/View/images/icon/logodron-1.png")
        pygame.display.set_icon(icon)
        
    # Nombre de la app
    name_app = "AIC-Drone"
    pygame.display.set_caption(name_app)

    global running_again
    global points
    global FLAG_YP
    global FLAG_YM
    global FLAG_XP
    global FLAG_XM
    global obstaculos
    global lastpos
    global frame, frameCam

    SIZE_WIDTH = 50
    SIZE_HEIGH = 50
    i = 0
    font = ''

    # Valores para vuelo del dron
    flag_dstar = 0
    lr, fb, ud, yv = 0, 0, 0, 0  # left-right forward-backward up-down yaw-velocity
    speed = 20  # cm/s
    aspeed = 70  # degrees/s 45 gira  cada vez
    global yaw, a, x, y
    d = 0

    # Mostrar info de la bateria
    font = pygame.font.Font("App/Model/images/icon/sarpanch/Sarpanch-Medium.ttf", 20)

    # Porcentaje de la bateria
    textGamepad = font.render(f"Gamepad: {joystick.get_name()}", True, (255,225,255))
    # Posicionar el texto en la esquina superior izquierda (coordenadas 0, 0)
    text_rect = text.get_rect(topleft=(WIDTH_SCREEN/2, 0))

    try:
        # Botones
        btn_up = pygame.image.load('App/View/images/buttons/button-up.png')
        btn_bottom = pygame.image.load('App/View/images/buttons/button-bottom.png')
        btn_left = pygame.image.load('App/View/images/buttons/button-left.png')
        btn_right = pygame.image.load('App/View/images/buttons/button-right.png')
        btn_takeoff = pygame.image.load('App/View/images/buttons/takeoff-dron.png')
        btn_land = pygame.image.load('App/View/images/buttons/land-dron.png')
        btn_takeoff_key = pygame.image.load('App/View/images/buttons/key-t.png')
        btn_land_key = pygame.image.load('App/View/images/buttons/key-l.png')
    except Exception as e:
        btn_up = pygame.image.load('App/View/images/buttons/button-up.png')
        btn_bottom = pygame.image.load('App/View/images/buttons/button-bottom.png')
        btn_left = pygame.image.load('App/View/images/buttons/button-left.png')
        btn_right = pygame.image.load('App/View/images/buttons/button-right.png')
        btn_takeoff = pygame.image.load('App/Viewimages/buttons/takeoff-dron.png')
        btn_land = pygame.image.load('App/View/images/buttons/land-dron.png')
        btn_takeoff_key = pygame.image.load('App/View/images/buttons/key-t.png')
        btn_land_key = pygame.image.load('App/View/images/buttons/key-l.png')

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
                lr, fb, ud, yv = 0, 0, 0, 0
                d = 0
                for event in pygame.event.get():
                    pass
                    
                # Leer el estado de los botones
                #! ############ BOTONES PARA CONTROL DE XBOX ################ !#
                for i in range(joystick.get_numbuttons()):
                    if joystick.get_button(i):
                        # Boton A
                        if i == 0:
                            print('Boton A')
                        # Boton B
                        # Camara
                        if i == 1:
                            print('Boton B')
                            if camera == 1:
                                socket.streamoff()
                                camera = 0
                            elif camera == 0:
                                socket.streamon()
                                camera = 1
                        # Boton X
                        # Aterrizar
                        if i == 2:
                            print('Boton X')
                            socket.land()
                            time.sleep(2)
                        # Boton Y
                        # Despegar
                        if i == 3:
                            print('Boton Y')
                            socket.takeoff()
                            time.sleep(0.25)
                        # Boton LB
                        if i == 4:
                            print("Boton LB")
                        # Boton RB
                        # Fotos
                        if i == 5:
                            print('Boton RB')
                            FOLDER = 'Photos/'
                            PICTURE = f'photodrone_{time()}.jpg'
                            if not os.path.exists(FOLDER):
                                os.makedirs(FOLDER)
                            PATH_FILE = os.path.join(os.getcwd(), (FOLDER + PICTURE))
                            # cv2.imwrite(f'Fotografias/fotografiadrone{time()}.jpg', frame)
                            frameCam = socket.get_frame_read().frame
                            cv2.imwrite(PATH_FILE, frameCam)
                            time.sleep(0.2)
                        # Boton Select
                        # Desconectar
                        if i == 6:
                            print("Boton Select")
                            socket.end()
                        # Boton Pause
                        if i == 7:
                            print("Boton Pause")
                            cv2.destroyAllWindows()
                            pygame.display.quit()
                            socket.end()
                            pygame.quit()
                            break
                        # Boton joyStickLC
                        if i == 8:
                            print("Boton joyStickLC")
                        # Boton joyStickRC
                        if i == 9:
                            print("Boton joyStickRC")
                        # Boton Menu
                        if i == 10:
                            print("Boton Menu")
                        # Boton Share
                        if i == 11:
                            print("Boton Share")

                # Leer el estado de los ejes (joysticks)
                left_xJL = joystick.get_axis(0) # Izquierda JL
                left_yJL = joystick.get_axis(1) # Arriba JL
                right_xJL = joystick.get_axis(0) # Derecha JL
                right_yJL = joystick.get_axis(1) # Abajo JL
                left_xJR = joystick.get_axis(2) # Izquierda JR
                left_yJR = joystick.get_axis(3) # Arriba JR
                right_xJR = joystick.get_axis(2) # Derecha JR
                right_yJR = joystick.get_axis(3) # Abajo JR

                # Joysticks izquierdos
                #! Izquierda
                if left_xJL == -1:
                    print("Joystick L Izquierda")
                    lr = -speed
                    d = dInterval
                    a = 180
                #! Derecha
                if right_xJL >= 0.5:
                    print("Joystick L Derecha")
                    lr = speed
                    d = -dInterval
                    a = 180
                #! Abajo
                if right_yJL >= 0.5:
                    print("Joystick L Abajo")
                    fb = -speed
                    d = -dInterval
                    a = -90
                #! Arriba
                if left_yJL == -1:
                    print("Joystick L Arriba")
                    fb = speed
                    d = dInterval
                    a = -90

                #Joystick derechos
                #! Izquierda
                if left_xJR == -1:
                    print("Joystick R Izquierda")
                    yv = -aspeed
                    yaw -= aInterval
                    
                #! Derecha
                if right_xJR >= 0.5:
                    print("Joystick R Derecha")
                    yv = aspeed
                    yaw += aInterval
                    
                #! Abajo
                if right_yJR >= 0.5:
                    print("Joystick R Abajo")
                    ud = -speed
                    
                #! Arriba
                if left_yJR == -1:
                    print("Joystick R Arriba")
                    ud = speed
                    

                time.sleep(interval)

                if yaw > 180:
                    yaw = yaw - 360 * (yaw // 180)
                elif yaw < -180:
                    yaw = yaw + 360 * (-yaw // 180)

                a += yaw

                x += int(d * math.cos(math.radians(a)))

                y += int(d * math.sin(math.radians(a)))

                # Esperar un breve momento
                pygame.time.wait(10)

                vals = [lr, fb, ud, yv]
                pos = (x, y)

                if FLAG_YP == False and FLAG_YM == False and FLAG_XP == False and FLAG_XM == False:
                    [vals, pos, yaw]
                mapeado = np.zeros((500, 500, 3), np.uint8)
                socket.send_rc_control(vals[0], vals[1], vals[2], vals[3])
                
                if camera == 1:
                    frame = socket.get_frame_read().frame
                    frameCam = socket.get_frame_read().frame
                    # img = cv2.resize(frame, (600, 400))
                    # cv2.imshow("DJI TELLO", img)
                    # win.fill((0,0,0))  # Limpiar la pantalla
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame = np.rot90(frame)
                    frame = pygame.surfarray.make_surface(frame)
                    win.blit(frame,(0,0))

                if running_again == True:
                    pos = posNew
                    path = []
                    running_again = False
                    print('Pos Again: ', pos)

                #! Adelante
                if pos[1] <= LIMIT_YP_EXAMPLE:
                    FLAG_YP = True
                #! Atras
                elif pos[1] >= LIMIT_YM_EXAMPLE:
                    FLAG_YM = True
                #! Izquierda
                elif pos[0] <= LIMIT_XP_EXAMPLE:
                    FLAG_XP = True
                #! Derecha
                elif pos[0] >= LIMIT_XM_EXAMPLE:
                    FLAG_XM = True

                if FLAG_YP == True:
                    print("Alcanzo el limite Adelante")
                    # socket.send_rc_control(vals[0], -1, vals[2], vals[3])    
                    print("Pos: ", pos)
                    if flag_dstar == 0:
                        posPath = (pos[0],LIMIT_YP_EXAMPLE)
                    pos = posPath
                    if flag_dstar == 0:
                        n = 0.0
                        z = -1.0
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

                    flag_dstar += 1
                    if flag_dstar % 50 == 0:
                        obstaculos = np.unique(obstaculos, axis=0)
                    lastpos = pos

                    # print(pos)
                    if len(path) == 1 or 0:
                        print("Ha llegado a su destino, aterrice")
                        cv2.destroyAllWindows()
                        points = [(0, 0),(0, 0)]
                        destm = []
                        destpx = []
                        flag_dstar = 0
                        running_again = True
                        FLAG_YP = False
                    else:
                        pos = path[1]
                        posPath = path[1]
                        if len(path) != 1:
                            [vals, posNew, yaw] = simulGetKeyboardInput('DOWN')
                            socket.send_rc_control(vals[0], vals[1], vals[2], vals[3])
                            print("Pos New: ", posNew)
                        if pos[0] > 250 and posNew[0] > 250:
                            [vals, posNew, yaw] = simulGetKeyboardInput('LEFT')
                            socket.send_rc_control(vals[0], vals[1], vals[2], vals[3])
                        if pos[0] < 250 and posNew[0] < 250:
                            [vals, posNew, yaw] = simulGetKeyboardInput('RIGHT')
                            socket.send_rc_control(vals[0], vals[1], vals[2], vals[3])

                elif FLAG_XP == True:
                    print("Alcanzo el limite Izquierda")
                    if flag_dstar == 0:
                        posPath = (LIMIT_XP_EXAMPLE, pos[1])
                    pos = posPath
                    if flag_dstar == 0:
                        n = 1.0
                        z = 0.0
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

                    flag_dstar += 1
                    if flag_dstar % 50 == 0:
                        obstaculos = np.unique(obstaculos, axis=0)
                    lastpos = pos

                    # print(pos)
                    if len(path) == 1 or 0:
                        print("Ha llegado a su destino, aterrice")
                        cv2.destroyAllWindows()
                        points = [(0, 0),(0, 0)]
                        destm = []
                        destpx = []
                        flag_dstar = 0
                        # [vals, pos, yaw] = resetgetkeyboardinput()
                        running_again = True
                        FLAG_XP = False
                    else:
                        pos = path[1]
                        posPath = path[1]
                        if len(path) != 1:
                            [vals, posNew, yaw] = simulGetKeyboardInput('RIGHT')
                            socket.send_rc_control(vals[0], vals[1], vals[2], vals[3])
                            print("Pos New: ", posNew)
                        if pos[1] > 250 and posNew[1] > 250: #(270, 253)
                            [vals, posNew, yaw] = simulGetKeyboardInput('UP')
                            socket.send_rc_control(vals[0], vals[1], vals[2], vals[3])
                        if pos[1] < 250 and posNew[1] < 250:#(270, 230)
                            [vals, posNew, yaw] = simulGetKeyboardInput('DOWN')
                            socket.send_rc_control(vals[0], vals[1], vals[2], vals[3])

                elif FLAG_YM == True:
                    print("Alcanzo el limite Atras")
                    if flag_dstar == 0:
                        posPath = (pos[0],LIMIT_YM_EXAMPLE)
                    pos = posPath
                    if flag_dstar == 0:
                        n = 0.0
                        z = 1.0
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

                    flag_dstar += 1
                    if flag_dstar % 50 == 0:
                        obstaculos = np.unique(obstaculos, axis=0)
                    lastpos = pos

                    # print(pos)
                    if len(path) == 1 or 0:
                        print("Ha llegado a su destino, aterrice")
                        cv2.destroyAllWindows()
                        points = [(0, 0),(0, 0)]
                        destm = []
                        destpx = []
                        flag_dstar = 0
                        # [vals, pos, yaw] = resetgetkeyboardinput()
                        running_again = True
                        FLAG_YM = False
                    else:
                        pos = path[1]
                        posPath = path[1]
                        if len(path) != 1:
                            [vals, posNew, yaw] = simulGetKeyboardInput('UP')
                            socket.send_rc_control(vals[0], vals[1], vals[2], vals[3])
                            print("Pos New: ", posNew)
                        if pos[0] > 250 and posNew[0] > 250:
                            [vals, posNew, yaw] = simulGetKeyboardInput('LEFT')
                            socket.send_rc_control(vals[0], vals[1], vals[2], vals[3])
                        if pos[0] < 250 and posNew[0] < 250:
                            [vals, posNew, yaw] = simulGetKeyboardInput('RIGHT')
                            socket.send_rc_control(vals[0], vals[1], vals[2], vals[3])

                elif FLAG_XM == True:
                    print("Alcanzo el limite Derecha")
                    if flag_dstar == 0:
                        posPath = (LIMIT_XM_EXAMPLE,pos[1])
                    pos = posPath
                    if flag_dstar == 0:
                        n = -1.0
                        z = 0.0
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

                    flag_dstar += 1
                    if flag_dstar % 50 == 0:
                        obstaculos = np.unique(obstaculos, axis=0)
                    lastpos = pos

                    # print(pos)
                    if len(path) == 1 or 0:
                        print("Ha llegado a su destino, aterrice")
                        cv2.destroyAllWindows()
                        points = [(0, 0),(0, 0)]
                        destm = []
                        destpx = []
                        flag_dstar = 0
                        running_again = True
                        FLAG_XM = False
                    else:
                        pos = path[1]
                        posPath = path[1]
                        if len(path) != 1:
                            [vals, posNew, yaw] = simulGetKeyboardInput('LEFT')
                            socket.send_rc_control(vals[0], vals[1], vals[2], vals[3])
                            print("Pos New: ", posNew)
                        if pos[1] > 250 and posNew[1] > 250: #(270, 253)
                            [vals, posNew, yaw] = simulGetKeyboardInput('UP')
                            socket.send_rc_control(vals[0], vals[1], vals[2], vals[3])
                        if pos[1] < 250 and posNew[1] < 250:#(270, 230)
                            [vals, posNew, yaw] = simulGetKeyboardInput('DOWN')
                            socket.send_rc_control(vals[0], vals[1], vals[2], vals[3])
                
                if points[-1][0] != pos[0] or points[-1][1] != pos[1]:
                    points.append(pos)

                # Mapeado
                # drawpoints(mapeado, points, pos, obstaculos, yaw, modo)
                drawpoints(mapeado, points, pos, obstaculos, yaw, 1)
                cv2.imshow('Mapeado', mapeado)

                """
                    #################### MAPEADO ###################
                """
                cv2.waitKey(1)

                # Porcentaje de la bateria
                text = font.render(f"bateria: {socket.get_battery()}%", True, (255,225,255))
                # Posicionar el texto en la esquina superior izquierda (coordenadas 0, 0)
                text_rect = text.get_rect(topleft=(0, 0))
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
            break
        finally:
            # Asegurarse de liberar los recursos
            try:
                socket.end() # Cerrar la conexión con el dron
            except:
                pass  # Si ya estaba desconectado, no se lanzará ninguna excepción


def cameraScreen():
    pygame.init()

    # Display del tamaño de la pantalla
    WIDTH_SCREEN = 800
    HIGTH_SCREEN = 600

    win = pygame.display.set_mode((WIDTH_SCREEN, HIGTH_SCREEN))

    try:
        # Establecer icono para app
        # icon = pygame.image.load("App/Model/images/icon/logodron-1.png")
        icon = pygame.image.load("App/View/images/icon/logodron-1.png")
        pygame.display.set_icon(icon)
    except Exception as e:
        print(e)
        icon = pygame.image.load("App/View/images/icon/logodron-1.png")
        pygame.display.set_icon(icon)
        

    # Nombre de la app
    name_app = "AIC-Drone"
    pygame.display.set_caption(name_app)

    global running_again
    global points
    global FLAG_YP
    global FLAG_YM
    global FLAG_XP
    global FLAG_XM
    global obstaculos
    global lastpos
    global frame, frameCam

    SIZE_WIDTH = 50
    SIZE_HEIGH = 50
    i = 0
    font = ''
    # Mostrar info de la bateria
    font = pygame.font.Font("App/Model/images/icon/sarpanch/Sarpanch-Medium.ttf", 20)

    try:
        # Botones
        # btn_up = pygame.image.load('App/Model/images/buttons/button-up.png')
        # btn_bottom = pygame.image.load('App/Model/images/buttons/button-bottom.png')
        # btn_left = pygame.image.load('App/Model/images/buttons/button-left.png')
        # btn_right = pygame.image.load('App/Model/images/buttons/button-right.png')
        # btn_takeoff = pygame.image.load('App/Model/images/buttons/takeoff-dron.png')
        # btn_land = pygame.image.load('App/Model/images/buttons/land-dron.png')
        # btn_takeoff_key = pygame.image.load('App/Model/images/buttons/key-t.png')
        # btn_land_key = pygame.image.load('App/Model/images/buttons/key-l.png')
        btn_up = pygame.image.load('App/View/images/buttons/button-up.png')
        btn_bottom = pygame.image.load('App/View/images/buttons/button-bottom.png')
        btn_left = pygame.image.load('App/View/images/buttons/button-left.png')
        btn_right = pygame.image.load('App/View/images/buttons/button-right.png')
        btn_takeoff = pygame.image.load('App/View/images/buttons/takeoff-dron.png')
        btn_land = pygame.image.load('App/View/images/buttons/land-dron.png')
        btn_takeoff_key = pygame.image.load('App/View/images/buttons/key-t.png')
        btn_land_key = pygame.image.load('App/View/images/buttons/key-l.png')
    except Exception as e:
        btn_up = pygame.image.load('App/View/images/buttons/button-up.png')
        btn_bottom = pygame.image.load('App/View/images/buttons/button-bottom.png')
        btn_left = pygame.image.load('App/View/images/buttons/button-left.png')
        btn_right = pygame.image.load('App/View/images/buttons/button-right.png')
        btn_takeoff = pygame.image.load('App/Viewimages/buttons/takeoff-dron.png')
        btn_land = pygame.image.load('App/View/images/buttons/land-dron.png')
        btn_takeoff_key = pygame.image.load('App/View/images/buttons/key-t.png')
        btn_land_key = pygame.image.load('App/View/images/buttons/key-l.png')

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
                if FLAG_YP == False and FLAG_YM == False and FLAG_XP == False and FLAG_XM == False:
                    [vals, pos, yaw] = getkeyboardinput()
                mapeado = np.zeros((500, 500, 3), np.uint8)
                socket.send_rc_control(vals[0], vals[1], vals[2], vals[3])
                
                if camera == 1:
                    frame = socket.get_frame_read().frame
                    frameCam = socket.get_frame_read().frame
                    # img = cv2.resize(frame, (600, 400))
                    # cv2.imshow("DJI TELLO", img)
                    # win.fill((0,0,0))  # Limpiar la pantalla
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame = np.rot90(frame)
                    frame = pygame.surfarray.make_surface(frame)
                    win.blit(frame,(0,0))

                if running_again == True:
                    pos = posNew
                    path = []
                    running_again = False
                    print('Pos Again: ', pos)

                #! Adelante
                if pos[1] <= LIMIT_YP_EXAMPLE:
                    FLAG_YP = True
                #! Atras
                elif pos[1] >= LIMIT_YM_EXAMPLE:
                    FLAG_YM = True
                #! Izquierda
                elif pos[0] <= LIMIT_XP_EXAMPLE:
                    FLAG_XP = True
                #! Derecha
                elif pos[0] >= LIMIT_XM_EXAMPLE:
                    FLAG_XM = True

                if FLAG_YP == True:
                    print("Alcanzo el limite Adelante")
                    # socket.send_rc_control(vals[0], -1, vals[2], vals[3])    
                    print("Pos: ", pos)
                    if i == 0:
                        posPath = (pos[0],LIMIT_YP_EXAMPLE)
                    pos = posPath
                    if i == 0:
                        n = 0.0
                        z = -1.0
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
                        FLAG_YP = False
                    else:
                        pos = path[1]
                        posPath = path[1]
                        if len(path) != 1:
                            [vals, posNew, yaw] = simulGetKeyboardInput('DOWN')
                            socket.send_rc_control(vals[0], vals[1], vals[2], vals[3])
                            print("Pos New: ", posNew)
                        if pos[0] > 250 and posNew[0] > 250:
                            [vals, posNew, yaw] = simulGetKeyboardInput('LEFT')
                            socket.send_rc_control(vals[0], vals[1], vals[2], vals[3])
                        if pos[0] < 250 and posNew[0] < 250:
                            [vals, posNew, yaw] = simulGetKeyboardInput('RIGHT')
                            socket.send_rc_control(vals[0], vals[1], vals[2], vals[3])

                elif FLAG_XP == True:
                    print("Alcanzo el limite Izquierda")
                    if i == 0:
                        posPath = (LIMIT_XP_EXAMPLE, pos[1])
                    pos = posPath
                    if i == 0:
                        n = 1.0
                        z = 0.0
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
                        FLAG_XP = False
                    else:
                        pos = path[1]
                        posPath = path[1]
                        if len(path) != 1:
                            [vals, posNew, yaw] = simulGetKeyboardInput('RIGHT')
                            socket.send_rc_control(vals[0], vals[1], vals[2], vals[3])
                            print("Pos New: ", posNew)
                        if pos[1] > 250 and posNew[1] > 250: #(270, 253)
                            [vals, posNew, yaw] = simulGetKeyboardInput('UP')
                            socket.send_rc_control(vals[0], vals[1], vals[2], vals[3])
                        if pos[1] < 250 and posNew[1] < 250:#(270, 230)
                            [vals, posNew, yaw] = simulGetKeyboardInput('DOWN')
                            socket.send_rc_control(vals[0], vals[1], vals[2], vals[3])

                elif FLAG_YM == True:
                    print("Alcanzo el limite Atras")
                    if i == 0:
                        posPath = (pos[0],LIMIT_YM_EXAMPLE)
                    pos = posPath
                    if i == 0:
                        n = 0.0
                        z = 1.0
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
                        FLAG_YM = False
                    else:
                        pos = path[1]
                        posPath = path[1]
                        if len(path) != 1:
                            [vals, posNew, yaw] = simulGetKeyboardInput('UP')
                            socket.send_rc_control(vals[0], vals[1], vals[2], vals[3])
                            print("Pos New: ", posNew)
                        if pos[0] > 250 and posNew[0] > 250:
                            [vals, posNew, yaw] = simulGetKeyboardInput('LEFT')
                            socket.send_rc_control(vals[0], vals[1], vals[2], vals[3])
                        if pos[0] < 250 and posNew[0] < 250:
                            [vals, posNew, yaw] = simulGetKeyboardInput('RIGHT')
                            socket.send_rc_control(vals[0], vals[1], vals[2], vals[3])

                elif FLAG_XM == True:
                    print("Alcanzo el limite Derecha")
                    if i == 0:
                        posPath = (LIMIT_XM_EXAMPLE,pos[1])
                    pos = posPath
                    if i == 0:
                        n = -1.0
                        z = 0.0
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
                        FLAG_XM = False
                    else:
                        pos = path[1]
                        posPath = path[1]
                        if len(path) != 1:
                            [vals, posNew, yaw] = simulGetKeyboardInput('LEFT')
                            socket.send_rc_control(vals[0], vals[1], vals[2], vals[3])
                            print("Pos New: ", posNew)
                        if pos[1] > 250 and posNew[1] > 250: #(270, 253)
                            [vals, posNew, yaw] = simulGetKeyboardInput('UP')
                            socket.send_rc_control(vals[0], vals[1], vals[2], vals[3])
                        if pos[1] < 250 and posNew[1] < 250:#(270, 230)
                            [vals, posNew, yaw] = simulGetKeyboardInput('DOWN')
                            socket.send_rc_control(vals[0], vals[1], vals[2], vals[3])
                
                if points[-1][0] != pos[0] or points[-1][1] != pos[1]:
                    points.append(pos)

                # Mapeado
                # drawpoints(mapeado, points, pos, obstaculos, yaw, modo)
                drawpoints(mapeado, points, pos, obstaculos, yaw, 1)
                cv2.imshow('Mapeado', mapeado)

                """
                    #################### MAPEADO ###################
                """
                cv2.waitKey(1)
                # Porcentaje de la bateria
                text = font.render(f"bateria: {socket.get_battery()}%", True, (255,225,255))
                # Posicionar el texto en la esquina superior izquierda (coordenadas 0, 0)
                text_rect = text.get_rect(topleft=(0, 0))
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
            break
        finally:
            # Asegurarse de liberar los recursos
            try:
                socket.end() # Cerrar la conexión con el dron
            except:
                pass  # Si ya estaba desconectado, no se lanzará ninguna excepción