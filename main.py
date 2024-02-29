import pygame as pg
import random, time
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
        
        self.start_tid = time.time()
        
        self.spiller_spill = True
        
        # Poeng til spiller_1 og spiller_2
        self.poeng_1 = 0
        self.poeng_2 = 0
   
    def ny_runde_innstillinger(self):
        # Hvor mange kuler de kan skyte per runde
        self.ammo_1 = 10
        self.ammo_2 = 10

    def ny(self):
        self.ny_runde_innstillinger()
        # Lager spiller-objekt
        self.spiller_2 = SpillerH()
        self.spiller_1 = SpillerV()
        self.spillere = [self.spiller_1, self.spiller_2]
        
        platform_liste.append(Platform(0, 350, PLATFORM_BREDDE, HØYDE-350-PLATFORM_HØYDE))
        platform_liste.append(Platform(BREDDE-PLATFORM_BREDDE, 350, PLATFORM_BREDDE, HØYDE-350-PLATFORM_HØYDE))
        
        # Lager plattformer
        while len(platform_liste) < 5:
            # Lager ny plattform
            ny_platform = Platform(
                random.randint(PLATFORM_BREDDE, BREDDE-PLATFORM_BREDDE),
                random.randint(150, HØYDE-PLATFORM_HØYDE-50),
                PLATFORM_BREDDE,
                PLATFORM_HØYDE
            )
            
            trygt = True
                
            # Sjekker om den nye plattformen er på er ovenfor hverandre og om de kolliderer med noen av de gamle
            for platform in platform_liste:
                if ny_platform.rect.x > (platform.rect.x - PLATFORM_BREDDE) and ny_platform.rect.x < (platform.rect.x + PLATFORM_BREDDE):
                    trygt = False
                    break
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
        
        ny_tid = time.time()
        #self.spiller_spill = True
        if self.spiller_spill:
            while ny_tid - self.start_tid >= SPILLRUNDER_TID:
                self.overflate.fill((0, 0, 0))
                pg.display.flip()

                for hendelse in pg.event.get():
                    if hendelse.type == pg.KEYDOWN and hendelse.key == pg.K_RETURN:
                        self.start_tid = time.time()
                            # venter_på_enter = False
                
                        self.ny_runde_innstillinger()
            
            while ny_tid - self.start_tid < SPILLRUNDER_TID:
                self.klokke.tick(FPS)
                self.hendelser()
                self.oppdater()
                self.tegne()
                
                ny_tid = time.time()
        
    def hendelser(self):
        # Går gjennom hendelser (events)
        for hendelse in pg.event.get():
            # Sjekker om vi ønsker å lukke vinduet
            if hendelse.type == pg.QUIT:
                if self.spiller_spill:
                    self.spiller_spill = False

                self.kjører = False # Spillet skal avsluttes
                
            if hendelse.type == pg.KEYDOWN:
                # Spilleren skal hoppe hvis vi trykker på mellomromstasten
                if hendelse.key == pg.K_w:
                    if self.spiller_1.fart[1] == 0:
                        self.spiller_1.hopp()
                
                if hendelse.key == pg.K_e:
                    if self.ammo_1 > 0:
                        self.opprett_kule(self.spiller_1)
                        self.ammo_1 -= 1
                    
                if hendelse.key == pg.K_q:
                    if self.ammo_1 > 0:
                        self.opprett_kule(self.spiller_1, høyre = False)
                        self.ammo_1 -= 1
                
                if hendelse.key == pg.K_o:
                    if self.ammo_2 > 0:
                        self.opprett_kule(self.spiller_2)
                        self.ammo_2 -= 1
                    print(f"Ammo 1 = {self.ammo_1}")
                    print(f"Ammo 2 = {self.ammo_2}")
                        
                
                if hendelse.key == pg.K_u:
                    if self.ammo_2 > 0:
                        self.opprett_kule(self.spiller_2, høyre = False)
                        self.ammo_2 -= 1

                if hendelse.key == pg.K_i:
                    if self.spiller_2.fart[1] == 0:
                        self.spiller_2.hopp()
                        
    def opprett_kule(self, spiller, høyre = True):
        ny_kule = Kule(spiller.rect.x + SPILLER_BREDDE, spiller.rect.y + SPILLER_HØYDE//2)
        ny_kule.skutt = True
        if høyre:
            ny_kule.venstre = False
        spiller.kule_liste.append(ny_kule)
        self.kule = spiller.kule_liste[-1]
        
    def oppdater(self):
        self.spiller_1.oppdater()
        self.spiller_2.oppdater()
        
        for kule in self.spiller_1.kule_liste:
            kule.oppdater()
            if kule.senter[0] < 0 or kule.senter[0] > BREDDE:
                self.spiller_1.kule_liste.remove(kule)
                
            if kule.kollisjon(self.spiller_2):
                self.spiller_1.kule_liste.remove(kule)
                self.poeng_1 += 1
                print(f"Spiller 1: {self.poeng_1}. Spiller 2: {self.poeng_2}")
        
        for kule in self.spiller_2.kule_liste:
            kule.oppdater()
            if kule.senter[0] < 0 or kule.senter[0] > BREDDE:
                self.spiller_2.kule_liste.remove(kule)
                
            print(self.spiller_1.rect)
            print(kule.senter)

            if kule.kollisjon(self.spiller_1):
                self.spiller_2.kule_liste.remove(kule)
                self.poeng_2 += 1
                print(f"Spiller 1: {self.poeng_1}. Spiller 2: {self.poeng_2}")
        
        # Sjekker om spillerne faller
        for spiller in self.spillere:
            if spiller.fart[1] > 0:
                kollisjon_spiller_platform = False
            
                # Sjekker om spilleren kolliderer med en plattform
                for p in platform_liste:
                    if pg.Rect.colliderect(spiller.rect, p.rect):
                        kollisjon_spiller_platform = True
                        break
                
                if kollisjon_spiller_platform:
                    spiller.pos[1] = p.rect.y - SPILLER_HØYDE
                    spiller.fart[1] = 0
    
    def tegne(self):
        # Henter sky-bildet og endrer størrelsen slik at den passer til skjerm, uavhengig av størrelse
        himmel_bilde = pg.transform.scale(pg.image.load("himmel_skytespill.jpeg"), (BREDDE, HØYDE))
        
        # Tegner bakgrunnsbildet på skjermen
        self.overflate.blit(himmel_bilde, (0, 0))

        # Tegner plattformene
        for platform in platform_liste:
            self.overflate.blit(platform.bilde, (platform.rect.x, platform.rect.y))
            
        # Tegner spilleren
        self.overflate.blit(self.spiller_1.bilde, self.spiller_1.pos)
        self.overflate.blit(self.spiller_2.bilde, self.spiller_2.pos)
        
        for kule in self.spiller_1.kule_liste:
        # Tegner kule
            pg.draw.circle(self.overflate, SVART, kule.senter, kule.radius)
        
        for kule in self.spiller_2.kule_liste:
        # Tegner kule
            pg.draw.circle(self.overflate, SVART, kule.senter, kule.radius)
        
        # "Flipper" displayet for å vise hva vi har tegnet
        pg.display.flip()

spillbrett_objekt = Spillbrett()

while spillbrett_objekt.kjører:
    
    spillbrett_objekt.ny()

pg.quit()
