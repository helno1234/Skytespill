import pygame as pg
import time
from settings import *

class Spiller:
    def __init__(self):
        # self.bilde = pg.Surface((SPILLER_BREDDE, SPILLER_HØYDE))
        self.bilde = pg.transform.scale(pg.image.load("mario.png"), (SPILLER_BREDDE, SPILLER_HØYDE))
        # self.bilde.fill(GRØNN)
        self.rect = self.bilde.get_rect()
        self.rect.center = (
            10, 0
        )
        
        self.bilde_logo = pg.Surface((30, 50))
        self.bilde_logo.fill(RØD)
        
        
        self.pos = list(self.rect.center)
        self.fart = [0, 0]
        self.aks = [0, 0]
        
        self.retning_venstre = True
        
        # Tom liste for oppgraderinger
        self.oppgraderingsliste = []
        
        self.gyldig_pris_ammo = 0
        
        self.mulige_granater = 3
        
        self.granater = []
        self.eksplosjoner = []
        
        self.ammo_pris = "1"
        self.kule_pris = "1"
        self.kule_fart_pris = "5"
        self.stjele_pris = "10"
        
        self.ammo = 20
        
        self.kule_radius = 7
        
        self.kule_fart = 7
    
        # Tom liste til å legge inn kule_objekter
        self.kule_liste = []
        
        # Hvilken oppgradering som er "gyldig"
        self.gyldig = 0
        
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
        

# Klasse for spillobjekt som bruker piltaster
class SpillerH(Spiller):
    def __init__(self):
        super().__init__()
        self.rect.center = (
        BREDDE - SPILLER_BREDDE - 10,
        10
        )
        
        self.pos = list(self.rect.center)
        
        self.bilde_logo.fill(GRØNN)
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
        # self.bilde = pg.transform.scale(pg.image.load("murstein.jpeg"), (b,h))
        self.bilde = pg.Surface((b, h))
        self.bilde.fill(GRÅ)
        
        self.rect = self.bilde.get_rect()
        
        # Setter x- og y-posisjonen til platformen
        self.rect.x = x
        self.rect.y = y
        
        
class Kule:
    def __init__(self, x, y, r, fart):
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

    def oppdater_rektangel(self):
         return pg.Rect(self.x, self.y, self.bredde, self.høyde)

    def oppdater(self):
        if self.skutt:
            self.fart = [self.farten, 0]
            self.rektangel = pg.Rect(self.senter[0], self.senter[1], self.radius, self.radius)
            if self.venstre == True:
                self.senter = (self.senter[0] - self.fart[0], self.senter[1])
                self.x -= self.fart[0] # HER
            else:
                self.senter = (self.senter[0] + self.fart[0], self.senter[1])
                self.x += self.fart[0]
                
            self.rektangel = self.oppdater_rektangel()
    
    def kollisjon(self, objekt):
        return self.rektangel.colliderect(objekt.rect)
    
class Oppgraderings_boks:
    def __init__(self):
        self.x = BREDDE//2 - BREDDE//4
        self.y = HØYDE//3
        
        self.b = 200
        self.h = BOKS_HØYDE
        
        self.bilde = pg.Surface((100, 50))
        self.bilde.fill(GRØNN)
        
        self.tekst = FONT2.render("TESTING", True, HVIT)


# Penge klasse for penge_objekter som "powerups"
class Penge:
    def __init__(self, x, y):
        self.bilde = pg.Surface((PENGE_BREDDE, PENGE_HØYDE))
        self.bilde.fill(GUL)
    
        self.rect = self.bilde.get_rect()
        self.rect.center = (
            BREDDE/2 + PENGE_BREDDE, HØYDE - PLATFORM_HØYDE
        )
        
        self.rect.x = x
        self.rect.y = y
        
class Tast_startskjerm:
    def __init__(self, x, y):
        self.bredde = TAST_BREDDE
        self.høyde = TAST_HØYDE
        self.x = x
        self.y = y
        
        
class Granat:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.fart = [7,-11]
      
        self.skutt = False
        
        self.venstre = True
        
        self.bilde = pg.Surface((PENGE_BREDDE, PENGE_HØYDE))
        self.bilde.fill(GRØNN)
        
        self.rect = self.bilde.get_rect()
        self.rect.center = (self.rect.x,self.rect.y)
        
        self.senter = (self.x, self.y)
        
        self.bredde = GRANAT_RADIUS
        self.høyde = GRANAT_RADIUS
        
        self.truffet_bakken = False
        self.eksplosjon = False

    def oppdater_rektangel(self):
         return pg.Rect(self.x, self.y, GRANAT_RADIUS, GRANAT_RADIUS)

    def oppdater(self):
        if self.skutt:
            if self.y >= HØYDE - PLATFORM_HØYDE - GRANAT_RADIUS and not self.truffet_bakken:
                self.truffet_bakken = True
                self.start_tiden = time.time()
                self.y = HØYDE - PLATFORM_HØYDE - GRANAT_RADIUS
                
                self.senter = (self.x, self.y)
            elif self.truffet_bakken:
                self.ny_tid = time.time()
                if self.ny_tid - self.start_tiden >= VENTE_EKSPLOSJON:
                    eksplosjon_lyd = pg.mixer.Sound("eksplosjon_lydeffekt_2.mp3")
                    eksplosjon_lyd.set_volume(0.5)
                    eksplosjon_lyd.play()
                    self.eksplosjon = True
            else:
                self.fart[1] += GRAV
                self.rektangel = pg.Rect(self.senter[0], self.senter[1], GRANAT_RADIUS, GRANAT_RADIUS)
                
                if self.venstre:
                    self.x -= self.fart[0]
                else:
                    self.x += self.fart[0]
                    
                self.y += self.fart[1]
                    
                self.fart[1] += GRAV
                    
                self.senter = (self.x, self.y)
            
class Eksplosjon:
    def __init__(self, x, y, overflate):        
        self.x = x
        self.y = y
        
        self.senter = (self.x, self.y)
        
        self.bilde_farger = [RØD, ORANSJE, GUL]
        
        self.teller = 0
        
        self.radius = GRANAT_RADIUS
        
        self.indeks = 0
        
        self.eksplosjon_ferdig = False
        
        self.truffet_spiller = False
        
        self.radius_økning = 5
        
        self.bredde = GRANAT_RADIUS + 4*self.radius_økning
        
        self.rektangel = pg.Rect(self.x - self.bredde/2, self.y - self.bredde/2, self.bredde, self.bredde)
        
        self.farge = self.bilde_farger[self.indeks]
        
    def oppdater(self):
        self.farge = self.bilde_farger[self.indeks]
        
        self.teller += 1
        
        if self.teller >= 5:
            self.teller = 0
            self.indeks += 1
            self.radius += self.radius_økning
        
        if self.indeks >= 3:
            self.eksplosjon_ferdig = True
            
    def kollisjon(self, objekt):
        return self.rektangel.colliderect(objekt.rect)

            
            
            
            
            
            
            
        
        
        
    