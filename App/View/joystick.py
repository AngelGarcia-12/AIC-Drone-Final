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
            left_x = joystick.get_axis(0)
            left_y = joystick.get_axis(1)
            right_x = joystick.get_axis(3)
            right_y = joystick.get_axis(4)

            # Joysticks izquierdos
            if left_x == 0 or left_x == 1 or left_x == -1:
                print("Joystick Izquierdo - X:", left_x)
                return left_x
            if left_y == 0 or left_y == 1 or left_y == -1:
                print("Joystick Izquierdo - Y:", left_y)
                return left_y
            #Joystick derechos
            if right_x == 0 or right_x == 1 or right_x == -1:
                print("Joystick Derecho - X:", right_x)
                return right_x
            if right_y == 0 or right_y == 1 or right_y == -1:
                print("Joystick Derecho - Y:", right_y)
                return right_y

            # Esperar un breve momento
            pygame.time.wait(10)

    finally:
        # Cerrar pygame
        pygame.quit()

joystickDrone()