import pygame as pg
from settings import *

class Platform:
    def __init__(self, x, y, b, h):
        self.bilde = pg.Surface((b, h))
        self.bilde.fill(GRÅ)
        
        self.rect = self.bilde.get_rect()
        # Setter x- og y-posisjonen til platformen
        self.rect.x = x
        self.rect.y = y