import pygame as pg

pg.init()

# Konstanter
BREDDE = 1200
HØYDE = 600

# Størrelsen til vinduet
STØRRELSE = (BREDDE, HØYDE)

# Frames per second (bilder per sekund)
FPS = 60

# Farger (RGB)
SVART = (0, 0, 0)
HVIT = (255, 255, 255)
GRÅ = (50, 50, 50)
LYSE_GRÅ = (150, 150, 150)
GRØNN = (0, 255, 0)
RØD = (255, 0, 0)

# Platformer
PLATFORM_HØYDE = 25
PLATFORM_BREDDE = 200

GRAV = 0.8

# Innstillinger til spilleren
SPILLER_BREDDE = 75
SPILLER_HØYDE = 110
SPILLER_AKS = 0.4
SPILLER_FRIKSJON = -0.10

# Innstillinger til oppdateringsbokser
BOKS_HØYDE = 50
BOKS_AVSTAND = 10

# Innstillinger til kule
# KULE_RADIUS = 10

# Spillrunder (sek)
SPILLRUNDER_TID = 2

# Fonter til skrift
FONT1 = pg.font.Font(None, 36)
FONT2 = pg.font.Font(None, 24)
