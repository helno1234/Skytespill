import pygame
import random

# Initialiser Pygame
pygame.init()

# Opprett et vindu
screen = pygame.display.set_mode((800, 600))

# Opprett et rektangel
rect = pygame.Rect(300, 200, 200, 100)

# Definer en funksjon som "rister" rektangelet
def shake_rect():
    # Lag en tilfeldig offset-verdi for å flytte rektangelet
    offset = random.randint(-5, 5)
    # Endre posisjonen til rektangelet ved å legge til offset-verdien
    rect.move_ip(offset, offset)

# Kjør spillet i en evig løkke
while True:
    # Håndter tastetrykk
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # Rist rektangelet når "r" trykkes
                shake_rect()

    # Tegn rektangelet på skjermen
    pygame.draw.rect(screen, (255, 0, 0), rect)

    # Oppdater skjermen
    pygame.display.flip()