import pygame as pg
from settings import *

class Spillbrett:
    def __init__(self):
        # Initiere pygame
        pg.init()
        
        # Lager en klokke
        self.klokke = pg.time.Clock()
        
        # Lager en overflate vi kan tegne på
        self.overflate = pg.display.set_mode(STØRRELSE)
        
        # Variabel som styrer om spillet skal kjøres
        self.kjører = True

    def ny(self):
        self.kjør()
    
    def kjør(self):
        self.spiller = True
        
        while self.spiller:
            self.klokke.tick(FPS)
            self.hendelser()
            # self.oppdater()
            self.tegne()
            
    def hendelser(self):       
        # Går gjennom henselser (events)
        for hendelse in pg.event.get():
            # Sjekker om vi ønsker å lukke vinduet
            if hendelse.type == pg.QUIT:
                if self.spiller:
                    self.spiller = False
                self.kjører = False # Spillet skal avsluttes
            
    def tegne(self):
        # Henter sky-bildet og endrer størrelsen slik at den passer til skjerm, uavhengig av størrelse
        himmel_bilde = pg.transform.scale(pg.image.load("himmel_skytespill.jpeg"), (BREDDE, HØYDE))

        # Tegner bakgrunnsbildet på skjermen
        self.overflate.blit(himmel_bilde, (0, 0))
        
        # "Flipper" displayet for å vise hva vi har tegnet
        pg.display.flip()

spillbrett_objekt = Spillbrett()

while spillbrett_objekt.kjører:
    
    spillbrett_objekt.ny()

pg.quit()
