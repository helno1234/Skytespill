import pygame as pg
import random
from settings import *
from sprites import *

# Lager en liste til platformene, og legger til bakken
platform_liste = [Platform(0, HØYDE-PLATFORM_HØYDE, BREDDE, PLATFORM_HØYDE)]

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
        
        # Lager plattformer
        while len(platform_liste) < 5:
            print("1")
            # Lager ny plattform
            ny_platform = Platform(
                random.randint(10, BREDDE-PLATFORM_BREDDE-10),
                random.randint(50, HØYDE-PLATFORM_HØYDE-50),
                PLATFORM_BREDDE,
                PLATFORM_HØYDE
            )
            
            trygt = True
                
            # Sjekker om den nye plattformen kolliderer med noen av de gamle
            for platform in platform_liste:
                if pg.Rect.colliderect(ny_platform.rect, platform.rect):
                    trygt = False
                    break
                
            if trygt:
                # Legger i lista
                platform_liste.append(ny_platform)
            else:
                print("Plattformen kolliderte, prøver på nytt") 
            
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

        # Tegner plattformene
        for platform in platform_liste:
            self.overflate.blit(platform.bilde, (platform.rect.x, platform.rect.y))
        
        # "Flipper" displayet for å vise hva vi har tegnet
        pg.display.flip()

spillbrett_objekt = Spillbrett()

while spillbrett_objekt.kjører:
    
    spillbrett_objekt.ny()

pg.quit()
