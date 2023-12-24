import pygame
from time import sleep, time
from djitellopy import tello
import cv2

socket = tello.Tello()
global frame

def loadScreenApp(win):
    font = pygame.font.Font("Model/images/icon/sarpanch/Sarpanch-Medium.ttf", 60)
    loading_text = font.render('Estableciendo conexion', True, (255, 255, 255))
    dot_count = 0
    dot_animation_timer = pygame.time.get_ticks()

    # Cargar una imagen
    image = pygame.image.load('Model/images/icon/ScreenAppLoading.png')

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
        text_with_dots = font.render('Cargando' + loading_dots, True, (255, 255, 255))
    
        # Centrar el texto en la pantalla
        text_rect = text_with_dots.get_rect(center=win.get_rect().center)
        win.blit(text_with_dots, text_rect.topleft)
    
        pygame.display.flip()
        clock.tick(20)  # Controlar la velocidad de la animación

        flag += 1

        if flag == 80: # Si pasaron 3 seg
            running = False

pygame.quit()

# Pantalla de la app donde mostrar informacion sobre bateria, botones, etc.
# def infoScreen(win):
#     SIZE_WIDTH = 50
#     SIZE_HEIGH = 50
#     # Mostrar info de la bateria
#     font = pygame.font.Font("Model/images/icon/sarpanch/Sarpanch-Medium.ttf", 20)

#     # Botones
#     btn_up = pygame.image.load('Model/images/buttons/button-up.png')
#     btn_bottom = pygame.image.load('Model/images/buttons/button-bottom.png')
#     btn_left = pygame.image.load('Model/images/buttons/button-left.png')
#     btn_right = pygame.image.load('Model/images/buttons/button-right.png')
#     btn_takeoff = pygame.image.load('Model/images/buttons/takeoff-dron.png')
#     btn_land = pygame.image.load('Model/images/buttons/land-dron.png')
#     btn_takeoff_key = pygame.image.load('Model/images/buttons/key-t.png')
#     btn_land_key = pygame.image.load('Model/images/buttons/key-l.png')

#     # Cambiar tamano
#     icon_btn_up = pygame.transform.scale(btn_up, (SIZE_WIDTH, SIZE_HEIGH))
#     icon_btn_bottom = pygame.transform.scale(btn_bottom, (SIZE_WIDTH, SIZE_HEIGH))
#     icon_btn_left = pygame.transform.scale(btn_left, (SIZE_WIDTH, SIZE_HEIGH))
#     icon_btn_right = pygame.transform.scale(btn_right, (SIZE_WIDTH, SIZE_HEIGH))
#     icon_btn_takeoff = pygame.transform.scale(btn_takeoff, (SIZE_WIDTH+20, SIZE_HEIGH+20))
#     icon_btn_land = pygame.transform.scale(btn_land, (SIZE_WIDTH, SIZE_HEIGH))
#     icon_btn_takeoff_key = pygame.transform.scale(btn_takeoff_key, (SIZE_WIDTH+48, SIZE_HEIGH+8))# 40px de diferencia
#     icon_btn_land_key = pygame.transform.scale(btn_land_key, (SIZE_WIDTH-12, SIZE_HEIGH-12))

#     # Obtener los rectángulos de las imágenes para su posicionamiento
#     button_up_rect = icon_btn_up.get_rect()
#     button_down_rect = icon_btn_bottom.get_rect()
#     button_left_rect = icon_btn_left.get_rect()
#     button_right_rect = icon_btn_right.get_rect()
#     buttom_takeoff_rect = icon_btn_takeoff.get_rect()
#     buttom_land_rect = icon_btn_land.get_rect()
#     buttom_takeoff_key_rect = icon_btn_takeoff_key.get_rect()
#     buttom_land_key_rect = icon_btn_land_key.get_rect()

#     # Posicionar los botones en la esquina inferior derecha
#     button_down_rect.bottomright = (800 - 60, 600 - 20)
#     button_right_rect.bottomright = (800 - 20, 600 - 60)
#     button_up_rect.bottomright = (800 - 60, 600 - 100)
#     button_left_rect.bottomright = (800 - 100, 600 - 60)
#     buttom_takeoff_rect.center = (350, 20)
#     buttom_land_rect.center = (450, 20)
#     buttom_takeoff_key_rect.center = (350, 20)
#     buttom_land_key_rect.center = (450, 20)

#     # Hacer que parpadee el boton al pulsarlo
#     clock = pygame.time.Clock()
#     visible = True
#     interval = 500  # Intervalo de tiempo para el parpadeo en milisegundos
#     last_toggle = pygame.time.get_ticks()

#     # Bucle principal
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()

#         # Porcentaje de la bateria
#         text = font.render(f"bateria: {socket.get_battery()}%", True, (0,0,0))

#         # Posicionar el texto en la esquina superior izquierda (coordenadas 0, 0)
#         text_rect = text.get_rect(topleft=(0, 0))
#         # win.blit(text, text_rect)  # Mostrar el texto en la posición especificada

#         current_time = pygame.time.get_ticks()
#         if current_time - last_toggle > interval:
#             visible = not visible
#             last_toggle = current_time

#         win.fill((255,255,255))  # Limpiar la pantalla

#         # Mostrar u ocultar la imagen dependiendo del estado visible
#         if visible and getKey('UP'):
#             win.blit(icon_btn_up, button_up_rect)
#         elif visible and getKey('DOWN'):
#             win.blit(icon_btn_bottom, button_down_rect)
#         elif visible and getKey('LEFT'):
#             win.blit(icon_btn_left, button_left_rect)
#         elif visible and getKey('RIGHT'):
#             win.blit(icon_btn_right, button_right_rect)
#         elif visible and getKey('t'):
#             win.blit(icon_btn_takeoff, buttom_takeoff_rect)
#         elif visible and getKey('l'):
#             win.blit(icon_btn_land, buttom_land_rect)
#         else:
#             win.blit(icon_btn_up, button_up_rect)
#             win.blit(icon_btn_bottom, button_down_rect)
#             win.blit(icon_btn_left, button_left_rect)
#             win.blit(icon_btn_right, button_right_rect)
#             win.blit(icon_btn_takeoff_key, buttom_takeoff_key_rect)
#             win.blit(icon_btn_land_key, buttom_land_key_rect)

#         win.blit(text, text_rect)  # Mostrar el texto en la posición especificada

#         pygame.display.flip() 
#         clock.tick(20)  # Controlar la velocidad del bucle
    
# pygame.quit()

def cameraScreen(win):
    SIZE_WIDTH = 50
    SIZE_HEIGH = 50
    # Mostrar info de la bateria
    font = pygame.font.Font("Model/images/icon/sarpanch/Sarpanch-Medium.ttf", 20)

    # Botones
    btn_up = pygame.image.load('Model/images/buttons/button-up.png')
    btn_bottom = pygame.image.load('Model/images/buttons/button-bottom.png')
    btn_left = pygame.image.load('Model/images/buttons/button-left.png')
    btn_right = pygame.image.load('Model/images/buttons/button-right.png')
    btn_takeoff = pygame.image.load('Model/images/buttons/takeoff-dron.png')
    btn_land = pygame.image.load('Model/images/buttons/land-dron.png')
    btn_takeoff_key = pygame.image.load('Model/images/buttons/key-t.png')
    btn_land_key = pygame.image.load('Model/images/buttons/key-l.png')

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
                vals=getkeyboardinput()
                socket.send_rc_control(vals[0], vals[1], vals[2], vals[3])
                sleep(0.15)
                if camera == 1:
                    frame = socket.get_frame_read().frame
                    img = cv2.resize(frame, (600, 400))
                    cv2.imshow("DJI TELLO", img)

                cv2.waitKey(1)

                # Porcentaje de la bateria
                text = font.render(f"bateria: {socket.get_battery()}%", True, (0,0,0))

                # Posicionar el texto en la esquina superior izquierda (coordenadas 0, 0)
                text_rect = text.get_rect(topleft=(0, 0))
                # win.blit(text, text_rect)  # Mostrar el texto en la posición especificada

                current_time = pygame.time.get_ticks()
                if current_time - last_toggle > interval:
                    visible = not visible
                    last_toggle = current_time

                win.fill((255,255,255))  # Limpiar la pantalla

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
        else:
            print("Conexion establecida")

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

def getkeyboardinput():
    lr, fb, ud, yv = 0, 0, 0, 0  # left-right forward-backward up-down yaw-velocity
    global camera
    speed = 20  # cm/s

    aspeed = 70  # degrees/s 45 gira  cada vez

    if getKey('LEFT'):

        lr = -speed


    elif getKey('RIGHT'):

        lr = speed

    if getKey('UP'):

        fb = speed

    elif getKey('DOWN'):

        fb = -speed


    if getKey('w'):

        ud = speed

    elif getKey('s'):

        ud = -speed

    if getKey('a'):

        yv = -aspeed

    elif getKey('d'):

        yv = aspeed

    if getKey('l'):
        socket.land()
        sleep(2)

    elif getKey('t'):
        socket.takeoff()
        sleep(0.25)

    elif getKey('c'):
        if camera == 1:
            socket.streamoff()
            camera = 0
        elif camera == 0:
            socket.streamon()
            camera = 1

    elif getKey('f'):
        cv2.imwrite(f'Fotografias/fotografiadrone{time()}.jpg', frame)
        sleep(0.2)

    elif getKey('q'):
        socket.end()
    
    elif getKey('e'):
        pygame.quit()

    sleep(0.25)

    return [lr, fb, ud, yv]