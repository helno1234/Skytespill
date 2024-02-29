import pygame as pg
import time
from settings import *

class Spiller:
    def __init__(self):
        self.bilde = pg.Surface((SPILLER_BREDDE, SPILLER_HØYDE))
        self.bilde.fill(GRØNN)
        self.rect = self.bilde.get_rect()
        self.rect.center = (
            10, 0
        )
        
        self.pos = list(self.rect.center)
        self.fart = [0, 0]
        self.aks = [0, 0]
        
        self.poeng = 0
    
    # Metode for hopping
    def hopp(self):
        self.fart[1] = -20
        
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
    def oppdater(self):
        super().oppdater()
        self.aks = [0, GRAV]
        # Henter tastene fra tastaturet
        keys = pg.key.get_pressed()
        
        if keys[pg.K_j]:
            self.aks[0] = -SPILLER_AKS
            
        if keys[pg.K_l]:
            self.aks[0] = SPILLER_AKS
            
# Klasse for spillobjekt som bruker piltaster
class SpillerV(Spiller):    
    def oppdater(self):
        super().oppdater()
        self.aks = [0, GRAV]
        # Henter tastene fra tastaturet
        keys = pg.key.get_pressed()
        
        if keys[pg.K_a]:
            self.aks[0] = -SPILLER_AKS
            
        if keys[pg.K_d]:
            self.aks[0] = SPILLER_AKS
    

class Platform:
    def __init__(self, x, y, b, h):
        self.bilde = pg.Surface((b, h))
        self.bilde.fill(GRÅ)
        
        self.rect = self.bilde.get_rect()
        
        # Setter x- og y-posisjonen til platformen
        self.rect.x = x
        self.rect.y = y
        
class Kule:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        self.senter = (self.x, self.y)
        self.radius = KULE_RADIUS
        
        self.bredde = self.radius
        self.høyde = self.radius
        
        self.skutt = False
        
        self.rektangel = self.oppdater_rektangel()
        self.venstre = True

    def oppdater_rektangel(self):
         return pg.Rect(self.x, self.y, self.bredde, self.høyde)

    def oppdater(self):
        if self.skutt:
            self.fart = [10,0]
            self.rektangel = pg.Rect(self.senter[0], self.senter[1], self.radius, self.radius)
            if self.venstre == True:
                self.senter = (self.senter[0] - self.fart[0], self.senter[1])
            else:
                self.senter = (self.senter[0] + self.fart[0], self.senter[1])
                self.x += self.fart[0]
                
            self.rektangel = self.oppdater_rektangel()
    
    def kollisjon(self, objekt):
        return self.rektangel.colliderect(objekt.rect)

    
    
    