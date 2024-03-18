import pygame as pg
import time
from settings import *

class Spiller:
    def __init__(self):        
        self.bilde_logo = pg.Surface((30, 50))
        self.bilde_logo.fill(RØD)
        
        self.fart = [0, 0]
        self.aks = [0, 0]
        
        self.retning_venstre = True
        
        self.gyldig_pris_ammo = 0
        
        self.mulige_granater = 3
        
        # Prisene for oppgraderinger
        self.ammo_pris = "1"
        self.kule_pris = "1"
        self.kule_fart_pris = "5"
        self.stjele_pris = "10"
        
        self.ammo = 20
        
        self.kule_radius = 7
        
        self.kule_fart = 7
    
        # Tom lister
        self.oppgraderingsliste = []
        self.granater = []
        self.eksplosjoner = []
        self.kule_liste = []
        
        # Hvilken oppgradering som er "gyldig"
        self.gyldig = 0
        
        # Oppgraderingen som er gyldig er grønn
        self.gyldig_farge = GRØNN
    
    # Metode for hopping
    def hopp(self):
        self.fart[1] = -13
        
    def oppdater(self):
        # Friksjon
        self.aks[0] += self.fart[0]*SPILLER_FRIKSJON
                
        # Bevegelseslikning i x-retning
        self.fart[0] += self.aks[0]
        self.pos[0] += self.fart[0] + 0.5*self.aks[0]
        
        # Sjekker om spilleren er utenfor spillbrettet 
        if self.pos[0] < 0:
            self.pos[0] = 0
            self.fart[0] = 0

        if self.pos[0] > BREDDE - SPILLER_BREDDE:
            self.pos[0] = BREDDE - SPILLER_BREDDE
            self.fart[0] = 0
        
        if self.pos[1] < 0:
            self.pos[1] = 0
            self.fart[1] = 0
        
        # Sjekker om spilleren er ved siden av platformene på siden av spillebrettet
        if self.pos[0] < PLATFORM_BREDDE and self.pos[1] > 475:
            self.pos[0] = PLATFORM_BREDDE
            self.fart[0] = 0
        if self.pos[0] > BREDDE - PLATFORM_BREDDE - SPILLER_BREDDE and self.pos[1] > 475:
            self.pos[0] = BREDDE - PLATFORM_BREDDE - SPILLER_BREDDE
            self.fart[0] = 0
        
        # Bevegelseslikning i y-retning
        self.fart[1] += self.aks[1]
        self.pos[1] += self.fart[1] + 0.5*self.aks[1]
        
        # Oppdaterer spillerens posisjon
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

# Subklasse for spillobjekt som bruker piltaster
class SpillerH(Spiller):
    def __init__(self):
        super().__init__()

        self.bilde = pg.transform.scale(pg.image.load("Luigi.png"), (SPILLER_BREDDE, SPILLER_HØYDE))
        
        self.rect = self.bilde.get_rect()
    
        self.rect.center = (
        BREDDE - SPILLER_BREDDE - 10,
        10
        )
        self.pos = list(self.rect.center)
        
    def oppdater(self):
        super().oppdater()
        self.aks = [0, GRAV]
        
        # Henter tastene fra tastaturet
        keys = pg.key.get_pressed()
        if keys[pg.K_j]:
            self.aks[0] = -SPILLER_AKS
            self.retning_venstre = True
        if keys[pg.K_l]:
            self.aks[0] = SPILLER_AKS
            self.retning_venstre = False
                 
# Klasse for spillobjekt som bruker piltaster
class SpillerV(Spiller):
    def __init__(self):
        super().__init__()
        self.bilde = pg.transform.scale(pg.image.load("mario.png"), (SPILLER_BREDDE, SPILLER_HØYDE))
        self.rect = self.bilde.get_rect()
        self.rect.center = (
            10, 0
        )
        self.pos = list(self.rect.center)
        
    def oppdater(self):
        super().oppdater()
        self.aks = [0, GRAV]
        
        # Henter tastene fra tastaturet
        keys = pg.key.get_pressed() 
        if keys[pg.K_a]:
            self.aks[0] = -SPILLER_AKS
            self.retning_venstre = True 
        if keys[pg.K_d]:
            self.aks[0] = SPILLER_AKS
            self.retning_venstre = False 

class Platform:
    def __init__(self, x, y, b, h):
        self.bilde = pg.Surface((b, h))
        self.bilde.fill(GRÅ)
        
        self.rect = self.bilde.get_rect()
        
        # Setter x- og y-posisjonen til platformen
        self.rect.x = x
        self.rect.y = y
        
class Kule:
    def __init__(self, x:float, y:float, r:float, fart:int):
        self.x = x
        self.y = y
        self.farten = fart
        
        self.senter = (self.x, self.y)
        self.radius = r
        
        self.bredde = self.radius
        self.høyde = self.radius
        
        self.skutt = False
        
        self.rektangel = self.oppdater_rektangel()
        self.venstre = True
    
    # Rektangel som følger kulen, slik blir det enklere med kollisjoner
    def oppdater_rektangel(self):
         return pg.Rect(self.x, self.y, self.bredde, self.høyde)

    def oppdater(self):
        if self.skutt:
            self.rektangel = pg.Rect(self.senter[0], self.senter[1], self.radius, self.radius)
            if self.venstre == True:
                self.senter = (self.senter[0] - self.farten, self.senter[1])
                self.x -= self.farten # HER
            else:
                self.senter = (self.senter[0] + self.farten, self.senter[1])
                self.x += self.farten
                
            self.rektangel = self.oppdater_rektangel()
    
    def kollisjon(self, objekt):
        return self.rektangel.colliderect(objekt.rect)
    
class Oppgraderings_boks:
    def __init__(self):
        self.x = BREDDE//2 - BREDDE//4
        self.y = HØYDE//3
        
        self.b = 200
        self.h = BOKS_HØYDE
        
        self.tekst = FONT2.render("TESTING", True, HVIT)

# Penge klasse for penge_objekt som "powerup"
class Penge:
    def __init__(self, x:float, y:float):
        self.bilde = pg.Surface((PENGE_BREDDE, PENGE_HØYDE))
        self.bilde_logo = pg.Surface((PENGE_BREDDE/2, PENGE_HØYDE/2))
        self.bilde.fill(GUL)
        self.bilde_logo.fill(GUL)
        self.rect = self.bilde.get_rect()
        self.rect.center = (
            BREDDE/2 + PENGE_BREDDE, HØYDE - PLATFORM_HØYDE
        )
        
        self.rect.x = x
        self.rect.y = y
        
class Tast_startskjerm:
    def __init__(self, x:float, y:float):
        self.bredde = TAST_BREDDE
        self.høyde = TAST_HØYDE
        self.x = x
        self.y = y
        
        
class Granat:
    def __init__(self, x:float, y:float):
        self.x = x
        self.y = y
        self.fart = [5,-7]
        
        self.bilde = pg.Surface((PENGE_BREDDE, PENGE_HØYDE))
        self.rect = self.bilde.get_rect()
        self.senter = (self.x, self.y)
        
        # Startverdier
        self.skutt = False
        self.venstre = True
        self.truffet_bakken = False
        self.eksplosjon = False

    # Et rektangel som følger granaten
    def oppdater_rektangel(self):
         return pg.Rect(self.x, self.y, GRANAT_RADIUS, GRANAT_RADIUS)

    def truffet_platform(self, y):
        self.truffet_bakken = True
        self.start_tiden = time.time()
        self.y = y
        
        self.senter = (self.x, self.y)
    
    def oppdater(self):
        if self.skutt:
            # Hvis granat treffer platformene på sidene
            if self.x <= PLATFORM_BREDDE and self.y >= STOR_PLATFORM_FRA_TAK and not self.truffet_bakken:
                self.truffet_platform(STOR_PLATFORM_FRA_TAK)
                
            elif self.x >= BREDDE - PLATFORM_BREDDE and self.y >= STOR_PLATFORM_FRA_TAK and not self.truffet_bakken:
                self.truffet_platform(STOR_PLATFORM_FRA_TAK)
                
            # Hvis granat treffer bakken
            elif self.y >= HØYDE - PLATFORM_HØYDE - GRANAT_RADIUS and not self.truffet_bakken:
                self.truffet_platform(HØYDE - PLATFORM_HØYDE - GRANAT_RADIUS)
                
            elif self.truffet_bakken:
                self.ny_tid = time.time()
                if self.ny_tid - self.start_tiden >= VENTE_EKSPLOSJON:
                    eksplosjon_lyd = pg.mixer.Sound("eksplosjon_lydeffekt_2.mp3")
                    eksplosjon_lyd.set_volume(0.5)
                    eksplosjon_lyd.play()
                    # Klar for å eksplodere
                    self.eksplosjon = True
            
            else:
                granat_går = True
                
                if self.y >= STOR_PLATFORM_FRA_TAK and self.x <= PLATFORM_BREDDE:
                    self.fart[0] = 0
                    granat_går = False
                
                if self.y >= STOR_PLATFORM_FRA_TAK and self.x >= BREDDE - PLATFORM_BREDDE:
                    self.fart[0] = 0
                    granat_går = False
                
                if self.x <= 0 or self.x >= BREDDE:
                    self.fart[0] = 0
                    granat_går = False
                    
                if granat_går:
                    if self.venstre:
                        self.x -= self.fart[0]
                    else:
                        self.x += self.fart[0]
                    
                self.fart[1] += GRAV
                self.rektangel = pg.Rect(self.senter[0], self.senter[1], GRANAT_RADIUS, GRANAT_RADIUS)
                self.y += self.fart[1]
                self.fart[1] += GRAV
                self.senter = (self.x, self.y)
            
class Eksplosjon:
    def __init__(self, x:int, y:int):        
        self.x = x
        self.y = y
        
        self.senter = (self.x, self.y)
        
        self.bilde_farger = [RØD, ORANSJE, GUL]
        
        self.teller = 0
        
        self.indeks = 0
        
        self.eksplosjon_ferdig = False
        self.truffet_spiller = False
        
        self.radius = GRANAT_RADIUS
        
        self.radius_økning = 5
        
        self.bredde = GRANAT_RADIUS + 4*self.radius_økning
        
        # Rektangel over granat, enklere med kollisjon
        self.rektangel = pg.Rect(self.x - self.bredde/2, self.y - self.bredde/2, self.bredde, self.bredde)
        
        self.farge = self.bilde_farger[self.indeks]
        
    # Går gjennom fargene i bilde_farger lista, slik at det ser ut som en eksplosjon
    def oppdater(self):
        self.farge = self.bilde_farger[self.indeks]
        
        self.teller += 1
        
        if self.teller >= 6:
            self.teller = 0
            self.indeks += 1
            self.radius += self.radius_økning
        
        if self.indeks >= 3:
            self.eksplosjon_ferdig = True
            
    def kollisjon(self, objekt):
        return self.rektangel.colliderect(objekt.rect)