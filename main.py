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
        self.poeng_1 = 40
        self.poeng_2 = 40
        
        self.oppdaterings_boks = Oppdaterings_boks()
        
        # Lager spiller-objekt
        self.spiller_2 = SpillerH()
        self.spiller_1 = SpillerV()
        
        self.spillere = [self.spiller_1, self.spiller_2]


    def ny(self):
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
        if self.spiller_spill:
            while ny_tid - self.start_tid >= SPILLRUNDER_TID:

                self.tegne_pause("Spiller 1", "Spiller 2", self.spiller_1.ammo, self.spiller_2.ammo)
                
                for i in range(4):
                    self.spiller_1.oppdateringsliste.append([self.oppdaterings_boks.x, self.oppdaterings_boks.y + (BOKS_HØYDE + BOKS_AVSTAND)*i, self.oppdaterings_boks.b, self.oppdaterings_boks.h])
                    self.spiller_2.oppdateringsliste.append([self.oppdaterings_boks.x + 400, self.oppdaterings_boks.y + (BOKS_HØYDE + BOKS_AVSTAND)*i, self.oppdaterings_boks.b, self.oppdaterings_boks.h])
        
                self.tegne_oppdateringer(self.spiller_1, spiller_1 = True)
                self.tegne_oppdateringer(self.spiller_2)
                
                pg.display.flip()
            
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
                print("HALO")
                if self.spiller_spill:
                    self.spiller_spill = False

                self.kjører = False # Spillet skal avsluttes
                
            if hendelse.type == pg.KEYDOWN:
                # Spilleren skal hoppe hvis vi trykker på mellomromstasten
                if hendelse.key == pg.K_w:
                    if self.spiller_1.fart[1] == 0:
                        self.spiller_1.hopp()
                
                if hendelse.key == pg.K_e:
                    if self.spiller_1.ammo > 0:
                        # print(f"Ammo 1 = {self.spiller_1.ammo}")
                        self.opprett_kule(self.spiller_1, self.spiller_1.kule_radius, 1)
                        self.spiller_1.ammo -= 1
                    
                if hendelse.key == pg.K_q:
                    if self.spiller_1.ammo > 0:
                        self.opprett_kule(self.spiller_1, self.spiller_1.kule_radius, høyre = False)
                        self.spiller_1.ammo -= 1
                
                if hendelse.key == pg.K_o:
                    if self.spiller_2.ammo > 0:
                        self.opprett_kule(self.spiller_2, self.spiller_2.kule_radius, 1)
                        self.spiller_2.ammo -= 1
                    print(f"Ammo 2 = {self.spiller_2.ammo}")
                        
                
                if hendelse.key == pg.K_u:
                    if self.spiller_2.ammo > 0:
                        self.opprett_kule(self.spiller_2, self.spiller_2.kule_radius, høyre = False)
                        self.spiller_2.ammo -= 1

                if hendelse.key == pg.K_i:
                    if self.spiller_2.fart[1] == 0:
                        self.spiller_2.hopp()
             
             
    def opprett_kule(self, spiller, radius, i = 0, høyre = True):
        ny_kule = Kule(spiller.rect.x + (SPILLER_BREDDE)*i, spiller.rect.y + SPILLER_HØYDE//2, radius)
        ny_kule.skutt = True
        if høyre:
            ny_kule.venstre = False
        spiller.kule_liste.append(ny_kule)
        self.kule = spiller.kule_liste[-1]
        
        
    def oppdater(self):
        self.spiller_1.oppdater()
        self.spiller_2.oppdater()
        
         # Sjekker om spillerne kolliderer
        if self.spiller_1.rect.colliderect(self.spiller_2.rect):
            # Hvis de kolliderer, får de en motsatt x-fart
            self.spiller_1.fart[0] = -self.spiller_1.fart[0]*2
            self.spiller_2.fart[0] = -self.spiller_2.fart[0]*2
        
        
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

            if kule.kollisjon(self.spiller_1):
                print("Treffer spiller 1")
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
        himmel = pg.Surface((BREDDE, HØYDE))
        himmel.fill(MØRKEBLÅ)
        
        # Tegner bakgrunnsbildet på skjermen
        self.overflate.blit(himmel, (0, 0))

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

        # Tegner rektangelet rundt spiller 1
        pg.draw.rect(self.overflate, RØD, (self.spiller_1.rect), 2)
        # rect.
        pg.draw.rect(self.overflate, GRØNN, (self.spiller_2.rect), 2)
        
        
        # "Flipper" displayet for å vise hva vi har tegnet
        pg.display.flip()
        
        
        
    def tegne_pause(self, spiller_1, spiller_2, ammo_1, ammo_2):
        self.overflate.fill(SVART)
        
        pg.draw.rect(self.overflate, GRÅ, [200, 20, BREDDE-400, HØYDE-40])
        
        # Stripe for å skille mellom spiller 1 og 2
        pg.draw.rect(self.overflate, LYSE_GRÅ, [BREDDE//2, 20, 2, HØYDE-150])
        
        # Skriver informasjon oppe om de ulike spillerne
        self.tegne_info_oppe(FONT1, f"{spiller_1}", 50, gyldig = True)
        self.tegne_info_oppe(FONT1, f"{spiller_2}", 50)
        self.tegne_info_oppe(FONT2, f"Antall poeng: {self.poeng_1}", 100, gyldig = True)
        self.tegne_info_oppe(FONT2, f"Antall poeng: {self.poeng_2}", 100)
        self.tegne_info_oppe(FONT2, f"Ammo igjen: {ammo_1}", 125, gyldig = True)
        self.tegne_info_oppe(FONT2, f"Ammo igjen: {ammo_2}", 125)
        
        # Skriver informasjonen nede om hvilke taster man kan trykke
        self.tegne_info_nede("Trykk på 'Enter' for å starte spillet igjen.", 500)
        self.tegne_info_nede("Spiller 1 kan trykke 's', og spiller 2 kan trykke 'k' til å gå gjennom oppdateringene.", 525)
        self.tegne_info_nede("Spiller 1 betaler ved å trykke 'w', og spiller 2 bruker 'i' til å betale.", 550)
        
        
    def tegne_info_oppe(self, font, tekst, y_pos, gyldig = False):
        teksten = font.render(tekst, True, HVIT)
        
        if gyldig:
            self.overflate.blit(teksten, (self.sentrere_tekst(teksten, gyldig = True), y_pos))
        else:
            self.overflate.blit(teksten, (self.sentrere_tekst(teksten), y_pos))
            
            
    def tegne_info_nede(self, tekst, y_pos):
        teksten = FONT2.render(tekst, True, HVIT)
        self.overflate.blit(teksten, (BREDDE//2 - teksten.get_rect().width//2, y_pos))
        
        
    def tegne_oppdateringer(self, spiller, spiller_1 = False):
        
        for oppdatering in spiller.oppdateringsliste:
            
            # Sjekker at variabel er mindre enn lengden på listene
            if spiller.gyldig < 4:         
                if oppdatering == spiller.oppdateringsliste[spiller.gyldig]:
                    pg.draw.rect(self.overflate, spiller.gyldig_farge, oppdatering, 0, 4)
                else:
                    pg.draw.rect(self.overflate, LYSE_GRÅ, oppdatering, 0, 4)
                
            else:
                spiller.gyldig = 0
            
            
            if spiller_1:
                ganging = 0
            else:
                ganging = 1
                
            for i in range(4):
                    self.overflate.blit(FONT1.render(spiller.priser[i], True, HVIT),
                      (self.oppdaterings_boks.x + self.oppdaterings_boks.b - 50 + (400*ganging), self.oppdaterings_boks.y + BOKS_HØYDE/2 - 10 + (BOKS_HØYDE + BOKS_AVSTAND)*i))
            
        for hendelse in pg.event.get():
            # Sjekker om vi ønsker å lukke vinduet
            if hendelse.type == pg.KEYDOWN:
                if hendelse.key == pg.K_s:
                    self.spiller_1.gyldig += 1
                    self.spiller_1.gyldig_farge = GRØNN
                    
                if hendelse.key == pg.K_k:
                    self.spiller_2.gyldig += 1
                    self.spiller_2.gyldig_farge = GRØNN
                    
                if hendelse.key == pg.K_RETURN:
                    self.spiller_1.rect.center = (
                        10, 0
                    )
                    self.spiller_2.rect.center = (
                        BREDDE - SPILLER_BREDDE - 10,
                        10
                    )
                    for spiller in self.spillere:
                        spiller.pos = list(spiller.rect.center)
                        
                        # Dersom spilleren har mindre enn 10 i ammo, skal spilleren få starte med 10 i ammo
                        if spiller.ammo < 10:
                            spiller.ammo = 10
                            
                        # self.spiller_2.pos = list(self.spiller_2.rect.center)
                        spiller.kule_liste = []
                        # self.spiller_2.kule_liste = []    
                        
                    self.spiller_1.gyldig_farge = GRØNN
                    self.spiller_2.gyldig_farge = GRØNN
                    
                    self.start_tid = time.time()
                    
                if hendelse.type == pg.QUIT:
                    self.kjører = False # Spillet skal avsluttes
    
    
                if hendelse.key == pg.K_w:
                    self.kjøpe_oppdateringer(self.spiller_1, self.poeng_1)
                    
                if hendelse.key == pg.K_i:
                    self.kjøpe_oppdateringer(self.spiller_2, self.poeng_2)
        
        # Liste med oppdateringstekster
        oppdateringstekster = ["+ 10 ammo", "Større kule", "TESTING", "STJELE ???"]
        
        # Tegner oppdateringstekstene
        for i in range(4):
            self.oppdateringstekst(oppdateringstekster[i], i)
            self.oppdateringstekst(oppdateringstekster[i], i, spiller_1 = False)

    def kjøpe_oppdateringer(self, spiller, poeng):
        # Ordbok med spiller og poeng:
        spiller_poeng_ordbok = {
            self.spiller_1: self.poeng_1,
            self.spiller_2: self.poeng_2
            }
        
        if poeng < int(spiller.priser[spiller.gyldig]):
            spiller.gyldig_farge = RØD
        else:
            gyldig_betaling = True
                
            if spiller.gyldig == 0:
                spiller.ammo += 10
                spiller.ammo_pris = str(int(spiller.ammo_pris) + 5)
                            
            if spiller.gyldig == 1:
                spiller.kule_radius += 1
                spiller.kule_pris = str(int(spiller.kule_pris) + 5)
               
            if spiller.gyldig == 3:
                if spiller_poeng_ordbok[spiller] == self.poeng_1:
                    if self.poeng_2 > 1:
                        self.poeng_2 = self.poeng_2//2
                    else:
                        gyldig_betaling = False
                else:
                    if self.poeng_1 > 1:
                        self.poeng_1 = self.poeng_1//2
                    else:
                        gyldig_betaling = False
                        
                        
            if gyldig_betaling:
                if spiller_poeng_ordbok[spiller] == self.poeng_1:
                    print(self.poeng_1)
                    self.poeng_1 -= int(self.spiller_1.priser[self.spiller_1.gyldig])
                else:
                    self.poeng_2 -= int(self.spiller_2.priser[self.spiller_2.gyldig])
            else:
                spiller.gyldig_farge = RØD
    
    def oppdateringstekst(self, tekst, i, spiller_1 = True):
        if spiller_1:
            gange = 0
        else:
            gange = 1
        
        self.overflate.blit(FONT2.render(tekst, True, HVIT),
            (self.oppdaterings_boks.x + 20 + (400*gange), self.oppdaterings_boks.y + BOKS_HØYDE/2 + (BOKS_HØYDE + BOKS_AVSTAND)*i - 5))
            
                
            
    def sentrere_tekst(self, tekst, gyldig = False):
        if gyldig:
            tallet = 500
        else:
            tallet = 100
        return BREDDE//2 - tallet + BREDDE/4 - (tekst.get_rect().width//2)


spillbrett_objekt = Spillbrett()

while spillbrett_objekt.kjører:
    
    spillbrett_objekt.ny()

pg.quit()