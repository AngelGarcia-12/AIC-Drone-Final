import pygame
from View import screen_app

# Inicio de la app
def init():

    # Cargar la ventana de presentacion de la app
    # previewWindowLoad()

    # Cargar la ventana principal de la app
    mainWindowApp()
    
# Cargar ventana de presentacion
def previewWindowLoad():
    pygame.init()

    # Display del tamaño de la pantalla
    win = pygame.display.set_mode((800, 500))

    # Establecer icono para app
    icon = pygame.image.load("App/Model/images/icon/logodron 1.png")
    pygame.display.set_icon(icon)

    # Nombre de la app
    name_app = "AIC-Drone"
    pygame.display.set_caption(name_app)

    # Imagen de App al cargar
    show_image = True
    screen_icon = pygame.image.load("App/Model/images/icon/ScreenApp.png")
    win.blit(screen_icon, screen_icon.get_rect())
    pygame.display.update()

    # Mostrar imagen por 2 seg
    pygame.time.wait(2000)

    # Cerrar ventana
    pygame.quit()

# Ventana principal de la aplicacion
def mainWindowApp():
    
    # Mostrar nueva ventana para cargar app
    pygame.init()

    # Display del tamaño de la pantalla
    win = pygame.display.set_mode((800, 600))

    # Establecer icono para app
    icon = pygame.image.load("App/Model/images/icon/logodron 1.png")
    pygame.display.set_icon(icon)

    # Nombre de la app
    name_app = "AIC-Drone"
    pygame.display.set_caption(name_app)

    screen_app.cameraScreen(win)

    # pygame.display.update() 

init()