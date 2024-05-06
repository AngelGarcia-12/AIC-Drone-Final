import pygame
import screen_app

# Variables necesarias para el algoritmo D*Lite
destm = []
destpx = []
obstaculos = []

# Inicio de la app
def init():

    # Cargar la ventana de presentacion de la app
    previewWindowLoad()

    # Cargar la ventana principal de la app
    mainWindowApp()
    
# Cargar ventana de presentacion
def previewWindowLoad():
    pygame.init()

    # Display del tamaño de la pantalla
    win = pygame.display.set_mode((800, 500))

    # Establecer icono para app
    icon = pygame.image.load("App/View/images/icon/logodron-1.png")
    pygame.display.set_icon(icon)

    # Nombre de la app
    name_app = "AIC-Drone"
    pygame.display.set_caption(name_app)

    # Imagen de App al cargar
    screen_icon = pygame.image.load("App/View/images/icon/ScreenApp.png")
    win.blit(screen_icon, screen_icon.get_rect())
    pygame.display.update()
    

    # Mostrar imagen por 2 seg
    pygame.time.wait(2000)

    # Cerrar
    pygame.quit()

# Ventana principal de la aplicacion
def mainWindowApp():
    print("""
      ***   ****   ******        ******    *****     ****   **      * ***********
     *   *   **   *      *      *      *   *    *   *    *  * *     * **
    *     *  **   *             *       *  *    *  *      * *  *    * **
    *******  **   *        **** *        * *****   *      * *   *   * *******
    *     *  **   *        **** *        * *    *  *      * *    *  * *******
    *     *  **   *             *       *  *     * *      * *     * * **
    *     *  **   *      *      *      *   *     *  *    *  *      ** **
      ***   ****   ******        ******    *     **  ****   *       * ***********
    """)

    while True:
        try:
            keyboard_joystick_flag = int(input(
            """
            Presiona 1 si quieres usar mando
            Presiona 0 si quieres usar el teclado
            Opcion: """))
            if keyboard_joystick_flag == 0:
                # Funcion para cargar la intefaz principal con teclado
                screen_app.cameraScreen()
                break
            elif keyboard_joystick_flag == 1:
                # Funcion para cargar la interfaz principal con mando
                screen_app.gamepadDrone()
                break
            else:
                print("Opcion no valida, elija una de las opciones")
        except ValueError:
            print("Introduce una opcion que sea un numero")

init()