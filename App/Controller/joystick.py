import pygame

def joystickDrone():
    # Inicializar pygame
    pygame.init()

    # Inicializar el joystick
    pygame.joystick.init()

    # Comprobar si hay joysticks disponibles
    if pygame.joystick.get_count() == 0:
        print("No se encontraron joysticks disponibles.")
        return

    # Seleccionar el primer joystick disponible
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    print("Nombre del joystick:", joystick.get_name())

    pygame.display.set_mode((200, 200))

    try:
        while True:
            for event in pygame.event.get():
               if event.type == pygame.QUIT:
                   pygame.quit()
                   return
               
            # Leer el estado de los botones
            #! ############ BOTONES PARA CONTROL DE XBOX ################ !#
            for i in range(joystick.get_numbuttons()):
                if joystick.get_button(i):
                    # Boton A
                    if i == 0:
                        print('Boton A')
                    # Boton B
                    if i == 1:
                        print('Boton B')
                    # Boton X
                    if i == 2:
                        print('Boton X')
                    # Boton Y
                    if i == 3:
                        print('Boton Y')
                    # Boton LB
                    if i == 4:
                        print("Boton LB")
                    # Boton RB
                    if i == 5:
                        print('Boton RB')
                    # Boton Select
                    if i == 6:
                        print("Boton Select")
                    # Boton Pause
                    if i == 7:
                        print("Boton Pause")
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
                # print("Joystick Izquierdo - X:", left_x)
                print("Joystick L Izquierda")
            #! Derecha
            if right_xJL >= 0.5:
                # print("Joystick Izquierdo - X:", right_x)
                print("Joystick L Derecha")
            #! Abajo
            if right_yJL >= 0.5:
                # print("Joystick Izquierdo - Y:", right_y)
                print("Joystick L Abajo")
            #! Arriba
            if left_yJL == -1:
                # print("Joystick Izquierdo - Y:", left_y)
                print("Joystick L Arriba")

            #Joystick derechos
            #! Izquierda
            if left_xJR == -1:
                # print("Joystick Izquierdo - X:", left_x)
                print("Joystick R Izquierda")
                # return left_x
            #! Derecha
            if right_xJR >= 0.5:
                # print("Joystick Izquierdo - X:", right_x)
                print("Joystick R Derecha")
                # return left_x
            #! Abajo
            if right_yJR >= 0.5:
                # print("Joystick Izquierdo - Y:", right_y)
                print("Joystick R Abajo")
                # return left_y
            #! Arriba
            if left_yJR == -1:
                # print("Joystick Izquierdo - Y:", left_y)
                print("Joystick R Arriba")
                # return left_y

            # Esperar un breve momento
            pygame.time.wait(10)

            pygame.display.update()

    finally:
        # Cerrar pygame
        pygame.quit()

joystickDrone()