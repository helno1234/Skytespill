import pygame as pg
from settings import *

class Spillbrett:
    def __init__(self):
        pass



# Initiere pygame
pg.init()

# Lager en overflate vi kan tegne på
overflate = pg.display.set_mode(STØRRELSE)

# Lager en klokke
klokke = pg.time.Clock()

# Variabel som styrer om spillet skal kjøres
kjør = True

# Henter sky-bildet og endrer størrelsen slik at den passer til skjerm, uavhengig av størrelse
himmel_bilde = pg.transform.scale(pg.image.load("himmel_skytespill.jpeg"), (BREDDE, HØYDE))

overflate.blit(himmel_bilde, (0, 0))

# Spill-løkken
while kjør:
    
    # Sørger for at løkken kjører i korrekt hastighet
    klokke.tick(FPS)
  
    # Går gjennom henselser (events)
    for hendelse in pg.event.get():
        # Sjekker om vi ønsker å lukke vinduet
        if hendelse.type == pg.QUIT:
            kjør = False # Spillet skal avsluttes
            
    # "Flipper" displayet for å vise hva vi har tegnet
    pg.display.flip()

pg.quit()
