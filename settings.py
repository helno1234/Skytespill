import pygame as pg

pg.init()

# Konstanter
BREDDE = 1200
HØYDE = 600

# Størrelsen til vinduet
STØRRELSE = (BREDDE, HØYDE)

# Frames per second (bilder per sekund)
FPS = 120

# Farger (RGB)
SVART = (0, 0, 0)
HVIT = (255, 255, 255)
GRÅ = (30, 30, 30)
LYSE_GRÅ = (150, 150, 150)
GRØNN = (0, 255, 0)
RØD = (200, 0, 0)
MØRKE_RØD = (100, 0, 0)
MØRKEBLÅ = (70, 70, 120)
GUL = (255, 255, 0)
ORANSJE = (255, 140, 0)

# Platformer
PLATFORM_HØYDE = 25
PLATFORM_BREDDE = 130

GRAV = 0.4

# Innstillinger til spilleren
SPILLER_BREDDE = 75
SPILLER_HØYDE = 110
SPILLER_AKS = 0.2
SPILLER_FRIKSJON = -0.10

# Innstillinger til oppdateringsbokser
BOKS_HØYDE = 50
BOKS_AVSTAND = 10

# Innstillinger til peneobjektet
PENGE_BREDDE = 30
PENGE_HØYDE = 30

# Spillrunder (sek)
SPILLRUNDER_TID = 30

# Bredde og høyde for taster (startskjerm)
TAST_BREDDE = 40
TAST_HØYDE = TAST_BREDDE

TAST_AVSTAND = 10

GRANAT_RADIUS = 10
VENTE_EKSPLOSJON = 1




# Fonter til skrift
FONT1 = pg.font.Font(None, 36)
FONT2 = pg.font.Font(None, 24)
STOR_FONT = pg.font.Font(None, 100)
LITT_STOR_FONT = pg.font.Font(None, 70)
