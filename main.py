import pygame as pg

# Variabel som styrer om spillet skal kjøres
run = True

# Spill-løkken
while run:
  
  # Går gjennom henselser (events)
  for event in pg.event.get():
      # Sjekker om vi ønsker å lukke vinduet
      if event.type == pg.QUIT:
          run = False # Spillet skal avsluttes

pg.quit()
