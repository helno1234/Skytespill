import pygame as pg
import time
from settings import *

class Spiller:
    def __init__(self):
        self.bilde = pg.Surface((SPILLER_BREDDE, SPILLER_HØYDE))
        self.bilde.fill(GRØNN)
        self.rect = self.bilde.get_rect()
        self.rect.center = (
            10, 10
        )
        
        self.pos = list(self.rect.center)
        self.fart = [0, 0]
        self.aks = [0, 0]
        
        self.poeng = 0
        
        #print(self.rect)
    
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
            
        # print(self.pos[1])
        
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
        
        # Oppdaterer rektangelets posisjon
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        
        

# Klasse for spillobjekt som bruker piltaster
class SpillerPiler(Spiller):
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
        
        if keys[pg.K_LEFT]:
            self.aks[0] = -SPILLER_AKS
            
        if keys[pg.K_RIGHT]:
            self.aks[0] = SPILLER_AKS
            
# Klasse for spillobjekt som bruker piltaster
class SpillerTaster(Spiller):    
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
    def __init__(self):
        self.senter = (30, 500)
        self.radius = 10
        
        # Til "rektangelet"
        self.x = self.senter[0]
        self.y = self.senter[1]
        self.bredde = self.radius
        self.høyde = self.radius
        
        self.skutt = False
        
        self.fart = [0,0]
        
        self.rektangel = self.oppdater_rektangel()

    def oppdater_rektangel(self):
         return pg.Rect(self.x, self.y, self.bredde, self.høyde)

    def oppdater(self):
        if self.skutt:
            self.rektangel = pg.Rect(self.senter[0], self.senter[1], self.radius, self.radius)
            self.fart = [5, 0]
            tid = 1  # Endre tidssteg etter behov
            self.senter = (self.senter[0] + self.fart[0] * tid, self.senter[1])
            
            # Sjekk om kulen er utenfor skjermen
            if self.senter[0] < 0 or self.senter[0] > BREDDE:
                self.radius = 0	# Kulern blir borte
                self.skutt = False
              
            self.x += self.fart[0]
            self.rektangel = self.oppdater_rektangel()
    
    def kollisjon(self, objekt):
        return self.rektangel.colliderect(objekt.rect)

    
    
    