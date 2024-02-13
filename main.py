import pygame as pg


# Konstanter
WIDTH = 400
HEIGHT = 600

# Størrelsen til vinduet
SIZE = (WIDTH, HEIGHT)

# Frames per second (bilder per sekund)
FPS = 60

# Farger (RGB)
WHITE = (255, 255, 255)

# Initiere pygame
pg.init()

# Lager en overflate (surface) vi kan tegne på
surface = pg.display.set_mode(SIZE)

# Lager en klokke
clock = pg.time.Clock()





# Variabel som styrer om spillet skal kjøres
run = True

# Spill-løkken
while run:
    
    # Sørger for at løkken kjører i korrekt hastighet
    clock.tick(FPS)
    
    surface.fill(WHITE)
  
    # Går gjennom henselser (events)
    for event in pg.event.get():
        # Sjekker om vi ønsker å lukke vinduet
        if event.type == pg.QUIT:
            run = False # Spillet skal avsluttes
            
    # "Flipper" displayet for å vise hva vi har tegnet
    pg.display.flip()

pg.quit()
