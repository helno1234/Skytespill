import pygame as pg
import random, time
from settings import *
from sprites import *

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
        
        self.gyldig_startskjerm = True
        
        # Poeng til spiller_1 og spiller_2
        self.poeng_1 = 20
        self.poeng_2 = 20
        
        self.oppgraderings_boks = oppgraderings_boks()
        
        # Lager spiller-objekt
        self.spiller_2 = SpillerH()
        self.spiller_1 = SpillerV()
        
        self.priser_1 = [self.spiller_1.ammo_pris, self.spiller_1.kule_pris, self.spiller_1.kule_fart_pris, self.spiller_1.stjele_pris]
        self.priser_2 = [self.spiller_2.ammo_pris, self.spiller_2.kule_pris, self.spiller_2.kule_fart_pris, self.spiller_2.stjele_pris]
        
        self.spillere = [self.spiller_1, self.spiller_2]

        self.penge_x = random.randint(PLATFORM_BREDDE + 50, BREDDE-PLATFORM_BREDDE - 50)
        
        pg.mixer.music.load("battle-music.mp3")
        pg.mixer.music.set_volume(0.6)
        pg.mixer.music.play(fade_ms = 10000, loops=10)
        
    def ny(self):
        self.penge_objekt = Penge(self.penge_x, HØYDE-PLATFORM_HØYDE-PENGE_HØYDE)
        
        self.kjør()
        
    
    def kjør(self):        
        # Ingen har tatt pengen 
        self.penge_tatt = False
    
        # Lager en liste til platformene, og legger til bakken
        self.platform_liste = [Platform(0, HØYDE-PLATFORM_HØYDE, BREDDE, PLATFORM_HØYDE)]

        # Nye platformer
        self.platform_liste.append(Platform(0, 350, PLATFORM_BREDDE, HØYDE-350-PLATFORM_HØYDE))
        self.platform_liste.append(Platform(BREDDE-PLATFORM_BREDDE, 350, PLATFORM_BREDDE, HØYDE-350-PLATFORM_HØYDE))
        
        # Lager plattformer
        while len(self.platform_liste) < 7:
            # Lager ny plattform
            ny_platform = Platform(
                random.randint(PLATFORM_BREDDE, BREDDE-PLATFORM_BREDDE),
                random.randint(150, HØYDE-PLATFORM_HØYDE-50),
                PLATFORM_BREDDE,
                PLATFORM_HØYDE
            )
            
            trygt = True
                
            # Sjekker om den nye plattformen er på er ovenfor hverandre og om de kolliderer med noen av de gamle
            for platform in self.platform_liste:
                # Om de er ovenfor hverandre
                if ny_platform.rect.x > (platform.rect.x - PLATFORM_BREDDE) and ny_platform.rect.x < (platform.rect.x + PLATFORM_BREDDE):
                    trygt = False
                    break
                # Om de er oppå hverandre
                if pg.Rect.colliderect(ny_platform.rect, platform.rect):
                    trygt = False
                    break
                
                
            if trygt:
                # Legger platformen til i lista
                self.platform_liste.append(ny_platform)
            else:
                print("Plattformen kolliderte, prøver på nytt") 
        
        
        while self.gyldig_startskjerm:
            for hendelse in pg.event.get():
                if hendelse.type == pg.QUIT:
                    self.gyldig_startskjerm = False
                    self.spiller_spill = False
                    self.kjører = False
                if hendelse.type == pg.KEYDOWN:
                    if hendelse.key == pg.K_RETURN:
                        self.gyldig_startskjerm = False
    
            
                self.startskjerm()
                pg.display.flip()

        # Setter ny_tid
        ny_tid = time.time()
        
        if self.spiller_spill:
            
            # Når spillerunden er ferdig
            while ny_tid - self.start_tid >= SPILLRUNDER_TID and self.spiller_spill:
                for hendelse in pg.event.get():
                    if hendelse.type == pg.QUIT:
                        self.spiller_spill = False
                        self.kjører = False
                        
                # Setter ned volum på bakgrunnsmusikken
                pg.mixer.music.set_volume(0.3)
                
                self.tegne_pause("Spiller 1", "Spiller 2", self.spiller_1.ammo, self.spiller_2.ammo)
                
                # Lager lister med 4 oppgraderingsbokser til hver spiller
                for i in range(4):
                    self.spiller_1.oppgraderingsliste.append([self.oppgraderings_boks.x, self.oppgraderings_boks.y + (BOKS_HØYDE + BOKS_AVSTAND)*i, self.oppgraderings_boks.b, self.oppgraderings_boks.h])
                    self.spiller_2.oppgraderingsliste.append([self.oppgraderings_boks.x + 400, self.oppgraderings_boks.y + (BOKS_HØYDE + BOKS_AVSTAND)*i, self.oppgraderings_boks.b, self.oppgraderings_boks.h])
        
                self.tegne_oppgraderinger(self.spiller_1, self.priser_1, spiller_1 = True)
                self.tegne_oppgraderinger(self.spiller_2, self.priser_2)
                
                pg.display.flip()
                
                # Ordbok med spiller og poeng:
                self.spiller_poeng_ordbok = {
                    self.spiller_1: 1,
                    self.spiller_2: 2
                    }
            
            
            # I spillet, dersom spillrunden ikke er ferdig
            while ny_tid - self.start_tid < SPILLRUNDER_TID and self.spiller_spill:
                
                ny_tid = time.time()
                
                if self.poeng_1 >= 50:
                    self.spiller_spill = False
                    self.vinner = "Spiller 1"
                    self.vinner_poeng = f"Med {self.poeng_1} poeng!"
                    self.vinner_farge = RØD
                elif self.poeng_2 >= 50:
                    self.vinner = "Spiller 2"
                    self.vinner_poeng = f"Med {self.poeng_2} poeng!"
                    self.vinner_farge = GRØNN
                    self.spiller_spill = False
                    
                
                pg.mixer.music.set_volume(1.0)
                    
                self.klokke.tick(FPS)
                
                self.hendelser()
                self.oppdater()
                self.tegne()
                
                # Ordbok med spiller og poeng:
                self.spiller_poeng_ordbok = {
                    self.spiller_1: 1,
                    self.spiller_2: 2
                    }
                
                for hendelse in pg.event.get():
                    if hendelse.type == pg.QUIT:
                        self.spiller_spill = False
                        self.kjører = False
            
            
            if self.kjører:
                # Ferdig med å spille: avslutningsskjerm
                while not self.spiller_spill:
                    self.avslutningsskjerm(self.vinner, self.vinner_poeng, self.vinner_farge)
                    for hendelse in pg.event.get():
                        if hendelse.type == pg.QUIT:
                            self.gyldig_startskjerm = False
                            self.spiller_spill = True
                            self.kjører = False
                    pg.display.flip()
                    
            print(ny_tid)
            
                    
    def hendelser(self):
        # Går gjennom hendelser (events)
        for hendelse in pg.event.get():
                
            if hendelse.type == pg.KEYDOWN:
                # Spiller 1 skal hoppe hvis vi trykker på mellomromstasten
                if hendelse.key == pg.K_w:
                    # Kan kun hoppe dersom spilleren er nede på bakken
                    if self.spiller_1.fart[1] == 0:
                        self.spiller_1.hopp()
                
                # Spiller 2 skal hoppe hvis vi trykker på mellomromstasten
                if hendelse.key == pg.K_i:
                    # Kan kun hoppe dersom spilleren er nede på bakken
                    if self.spiller_2.fart[1] == 0:
                        self.spiller_2.hopp()
                
                if hendelse.key == pg.K_e:
                    # Spiller 1 skyter kule mot venstre
                    if self.spiller_1.ammo > 0:
                        self.opprett_kule(self.spiller_1, self.spiller_1.kule_radius, 1)
                        self.spiller_1.ammo -= 1
                    
                if hendelse.key == pg.K_q:
                    # Spiller 1 skyter kule mot høyre
                    if self.spiller_1.ammo > 0:
                        self.opprett_kule(self.spiller_1, self.spiller_1.kule_radius, høyre = False)
                        self.spiller_1.ammo -= 1
                
                if hendelse.key == pg.K_o:
                    # Spiller 2 skyter kule mot venstre
                    if self.spiller_2.ammo > 0:
                        self.opprett_kule(self.spiller_2, self.spiller_2.kule_radius, 1)
                        self.spiller_2.ammo -= 1
                
                if hendelse.key == pg.K_u:
                    # Spiller 2 skyter kule mot høyre
                    if self.spiller_2.ammo > 0:
                        self.opprett_kule(self.spiller_2, self.spiller_2.kule_radius, høyre = False)
                        self.spiller_2.ammo -= 1
             
             
    def opprett_kule(self, spiller, radius, i = 0, høyre = True):
        # Lager skudd-lyd når det blir skutt en kule
        skudd_lyd = pg.mixer.Sound("skudd.mp3")
        skudd_lyd.set_volume(0.1)
        skudd_lyd.play()
        
        ny_kule = Kule(spiller.rect.x + (SPILLER_BREDDE)*i, spiller.rect.y + SPILLER_HØYDE//2, radius, spiller.kule_fart)
        ny_kule.skutt = True
        if høyre:
            ny_kule.venstre = False
        # Legger til kule i spilleren sin liste
        spiller.kule_liste.append(ny_kule)
        self.kule = spiller.kule_liste[-1]
        
        
    def oppdater(self):
        self.spiller_1.oppdater()
        self.spiller_2.oppdater()
        
        # Sjekker om spillerne lander oppå hverandre
        if self.spiller_1.rect.colliderect(self.spiller_2.rect) and self.spiller_1.rect.y < self.spiller_2.rect.y:
            self.spiller_1.fart[1] = -self.spiller_1.fart[1]
            
        elif self.spiller_1.rect.colliderect(self.spiller_2.rect) and self.spiller_2.rect.y < self.spiller_1.rect.y:
            self.spiller_2.fart[1] = -self.spiller_2.fart[1]
            
        # Sjekker om spillerne kolliderer
        elif self.spiller_1.rect.colliderect(self.spiller_2.rect) and self.spiller_1.rect.y >= self.spiller_2.rect.y:        
                # Hvis de kolliderer, får de en motsatt x-fart
                self.spiller_1.fart[0] = -self.spiller_1.fart[0]*2
                self.spiller_2.fart[0] = -self.spiller_2.fart[0]*2
            
        # Sjekker kollisjon med penge_objekt og spillerobjektene
        if not self.penge_tatt:
            if self.spiller_1.rect.colliderect(self.penge_objekt.rect):
                # Spiller "penge"-lyd som symboliserer at en spiller har tatt pengen
                skudd_lyd = pg.mixer.Sound("ta_penge.mp3")
                skudd_lyd.set_volume(0.7)
                skudd_lyd.play()
                
                self.poeng_1 += 5
                self.penge_tatt = True
                
            if self.spiller_2.rect.colliderect(self.penge_objekt.rect):
                # Spiller "penge"-lyd som symboliserer at en spiller har tatt pengen
                skudd_lyd = pg.mixer.Sound("ta_penge.mp3")
                skudd_lyd.set_volume(0.7)
                skudd_lyd.play()
                
                self.poeng_2 += 5
                self.penge_tatt = True
        
        for kule in self.spiller_1.kule_liste:
            kule.oppdater()
            # Sjekker kollisjon med kule_objektene og veggene på spillbrettet
            if kule.senter[0] < 0 or kule.senter[0] > BREDDE:
                self.spiller_1.kule_liste.remove(kule)
                
            # Sjekker kollisjon med kule_objektene og spillerobjektene
            if kule.kollisjon(self.spiller_2):
                self.spiller_1.kule_liste.remove(kule)
                self.poeng_1 += 1
        
        for kule in self.spiller_2.kule_liste:
            kule.oppdater()
            if kule.senter[0] < 0 or kule.senter[0] > BREDDE:
                self.spiller_2.kule_liste.remove(kule)

            if kule.kollisjon(self.spiller_1):
                print("Treffer spiller 1")
                self.spiller_2.kule_liste.remove(kule)
                self.poeng_2 += 1
                
        # Sjekker om spillerne faller
        for spiller in self.spillere:
            if spiller.fart[1] > 0:
                kollisjon_spiller_platform = False
            
                # Sjekker om spilleren kolliderer med en plattform
                for p in self.platform_liste:
                    if pg.Rect.colliderect(spiller.rect, p.rect):
                        kollisjon_spiller_platform = True
                        break
                
                if kollisjon_spiller_platform:
                    spiller.pos[1] = p.rect.y - SPILLER_HØYDE
                    spiller.fart[1] = 0
            
            # Går ikke gjennom de store platformene på siden
            if spiller.pos[0] < PLATFORM_BREDDE or spiller.pos[0] > BREDDE - PLATFORM_BREDDE - SPILLER_BREDDE:
                if spiller.pos[1] > 350:
                    spiller.fart[0] = -spiller.fart[0]*1.5
                    
        
    def tegne(self):     
        himmel = pg.Surface((BREDDE, HØYDE))
        himmel.fill(MØRKEBLÅ)
        
        # Tegner bakgrunnsbildet på skjermen
        self.overflate.blit(himmel, (0, 0))

        # Tegner plattformene
        for platform in self.platform_liste:
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
        
        # Tegner penge_objektet:
        if not self.penge_tatt:
            self.overflate.blit(self.penge_objekt.bilde, (self.penge_objekt.rect.x, self.penge_objekt.rect.y))
            
        # Tegner poeng og ammo øverst i hjørnet, slik at de som spiller kan se det samtidig
        self.hjørne_informasjon(self.spiller_1, 10, self.poeng_1, self.spiller_1.ammo, i = 1, j = 0)
        self.hjørne_informasjon(self.spiller_2, BREDDE - 40, self.poeng_2, self.spiller_2.ammo)

        # "Flipper" displayet for å vise hva vi har tegnet
        pg.display.flip()
        
        
    def hjørne_informasjon(self, spiller, x_bilde, poeng, ammo, i = 0, j = 1):
        self.overflate.blit(spiller.bilde_logo, (x_bilde, 10))
        self.overflate.blit(FONT2.render(f"Poeng: {poeng}", True, HVIT),
            (50 * i + (BREDDE - 50 - FONT2.size(f"Poeng: {poeng}")[0]) * j, 12))
        self.overflate.blit(FONT2.render(f"Ammunisjon: {ammo}", True, HVIT),
            (50 * i + (BREDDE - 50 - FONT2.size(f"Ammunisjon: {ammo}")[0]) * j, 42))
        
    
    def startskjerm(self):
        self.overflate.fill(SVART) 
        pg.draw.rect(self.overflate, GRÅ, [200, 20, BREDDE-400, HØYDE-40])
        
        # Stripe for å skille mellom tekster
        # pg.draw.rect(self.overflate, LYSE_GRÅ, [250, 120, BREDDE-500, 2])
        pg.draw.rect(self.overflate, LYSE_GRÅ, [BREDDE/2, 130, 2, HØYDE - 300])

        self.tegne_info_oppe(FONT1, f"Spiller 1", 140, gyldig = True)
        self.tegne_info_oppe(FONT1, f"Spiller 2", 140)
        
        self.overflate.blit(FONT2.render("Skyte:", True, HVIT), (self.sentrere_tekst(FONT2.render("Skyte:", True, HVIT), gyldig = True), 210))
        self.overflate.blit(FONT2.render("Bevegelse:", True, HVIT), (self.sentrere_tekst(FONT2.render("Bevegelse:", True, HVIT), gyldig = True), 310))
        
        self.overflate.blit(FONT2.render("Skyte:", True, HVIT), (self.sentrere_tekst(FONT2.render("Skyte:", True, HVIT), gyldig = False), 210))
        self.overflate.blit(FONT2.render("Bevegelse:", True, HVIT), (self.sentrere_tekst(FONT2.render("Bevegelse:", True, HVIT), gyldig = False), 310))
            
        self.tegne_taster_startskjerm()
        
        self.tegne_info_nede(f"The shooter", 40, font = FONT1)
        self.tegne_info_nede(f"Mål: førstemann til 100 poeng", 80)

        self.tegne_info_nede(f" +1 poeng for å skyte den andre spilleren", 460)
        self.tegne_info_nede(f" +5 poeng for å plukke opp pengen", 490)
        self.tegne_info_nede(f"Hver spillrunde varer i {SPILLRUNDER_TID} sekunder, deretter kan dere kjøpe oppgraderinger", 520)
        self.tegne_info_nede(f"Trykk 'Enter' for å starte", 560)
        
        
    def avslutningsskjerm(self, vinner, poeng, farge):
        self.overflate.fill(SVART)
        pg.draw.rect(self.overflate, GRÅ, [200, 20, BREDDE-400, HØYDE-40])
        
        self.overflate.blit(STOR_FONT.render("VINNEREN ER:", True, HVIT),
            (BREDDE/2 - STOR_FONT.size("VINNEREN ER:")[0]/2, 150))
        
        self.overflate.blit(LITT_STOR_FONT.render(vinner, True, farge),
            (BREDDE/2 - LITT_STOR_FONT.size(vinner)[0]/2, HØYDE/2 - FONT1.size(vinner)[1]/2))
        
        self.overflate.blit(FONT1.render(poeng, True, HVIT),
            (BREDDE/2 - FONT1.size(poeng)[0]/2, HØYDE/2 - FONT1.size(vinner)[1]/2 + 100))
        
    def tegne_taster_startskjerm(self):
        
        def taste_teksten(tast, bokstav):
            self.overflate.blit(FONT1.render(bokstav, True, GRÅ),
            (tast.x + TAST_BREDDE/2 - FONT1.size(bokstav)[0]/2, tast.y + TAST_HØYDE/2 - FONT1.size(bokstav)[1]/2))
            
            
        def taster_i_listen(i,j,k, y_pos, gyldighet = False):
            tast = Tast_startskjerm(self.sentrere_tekst(FONT1.render("Spiller 1", True, HVIT), gyldig=gyldighet) + FONT1.size("Spiller 1")[0]/2 + i * (TAST_BREDDE * (1/2 + j) + TAST_AVSTAND * k), y_pos)
            taster.append(tast)
        
        taster = []
        bokstaver = ["q", "u", "e", "o", "w", "i", "s", "k", "d", "l", "a", "j"]
    
        for i in range(1,7):
            if i == 2 or i == 5:
                tall_1 = 1
            else:
                tall_1 = -1
            
            if i == 1 or i == 6:
                tall_2 = 1
            else:
                tall_2 = 0
            
            if i == 3 or i == 4:
                tall_3 = 0
            else:
                tall_3 = 1
            
            if i == 1 or i == 2:
                tall_4 = 240
            elif i == 3:
                tall_4 = 340
            else:
                tall_4 = 390
            
            taster_i_listen(tall_1, tall_2, tall_3, tall_4, gyldighet = True)
            taster_i_listen(tall_1, tall_2, tall_3, tall_4, gyldighet = False)
        
        for i in range(len(taster)):
            pg.draw.rect(self.overflate, LYSE_GRÅ, (taster[i].x, taster[i].y, taster[i].bredde, taster[i].høyde), 0, 4)
            taste_teksten(taster[i], bokstaver[i])
        
        
    def tegne_pause(self, spiller_1, spiller_2, ammo_1, ammo_2):
        self.overflate.fill(SVART)
        
        pg.draw.rect(self.overflate, GRÅ, [200, 20, BREDDE-400, HØYDE-40])
        
        # Stripe for å skille mellom spiller 1 og 2
        pg.draw.rect(self.overflate, LYSE_GRÅ, [BREDDE//2, 20, 2, HØYDE-150])
        
        # Skriver informasjon oppe om de ulike spillerne
        self.tegne_info_oppe(FONT1, f"{spiller_1}", 50, gyldig = True, fargen = RØD)
        self.tegne_info_oppe(FONT1, f"{spiller_2}", 50, fargen = GRØNN)
        self.tegne_info_oppe(FONT2, f"Antall poeng: {self.poeng_1}", 100, gyldig = True)
        self.tegne_info_oppe(FONT2, f"Antall poeng: {self.poeng_2}", 100)
        self.tegne_info_oppe(FONT2, f"Ammo igjen: {ammo_1}", 125, gyldig = True)
        self.tegne_info_oppe(FONT2, f"Ammo igjen: {ammo_2}", 125)
        
        # Skriver informasjonen nede om hvilke taster man kan trykke
        self.tegne_info_nede("Trykk på 'Enter' for å starte spillet igjen.", 500)
        self.tegne_info_nede("Spiller 1 kan trykke 's', og spiller 2 kan trykke 'k' til å gå gjennom oppgraderingene.", 525)
        self.tegne_info_nede("Spiller 1 betaler ved å trykke 'w', og spiller 2 bruker 'i' til å betale.", 550)
        
        
    def tegne_info_oppe(self, font, tekst, y_pos, gyldig = False, fargen = HVIT):
        teksten = font.render(tekst, True, fargen)
        
        if gyldig:
            self.overflate.blit(teksten, (self.sentrere_tekst(teksten, gyldig = True), y_pos))
        else:
            self.overflate.blit(teksten, (self.sentrere_tekst(teksten), y_pos))
            
            
    def tegne_info_nede(self, tekst, y_pos, font = FONT2):
        teksten = font.render(tekst, True, HVIT)
        self.overflate.blit(teksten, (BREDDE//2 - teksten.get_rect().width//2, y_pos))
        
        
    def tegne_oppgraderinger(self, spiller, priser, spiller_1 = False):
        self.priser_1 = [self.spiller_1.ammo_pris, self.spiller_1.kule_pris, self.spiller_1.kule_fart_pris, self.spiller_1.stjele_pris]
        self.priser_2 = [self.spiller_2.ammo_pris, self.spiller_2.kule_pris, self.spiller_2.kule_fart_pris, self.spiller_2.stjele_pris]
        
        for oppgradering in spiller.oppgraderingsliste:
            
            # Sjekker at variabel er mindre enn lengden på listene
            if spiller.gyldig < 4:         
                if oppgradering == spiller.oppgraderingsliste[spiller.gyldig]:
                    pg.draw.rect(self.overflate, spiller.gyldig_farge, oppgradering, 0, 4)
                else:
                    pg.draw.rect(self.overflate, LYSE_GRÅ, oppgradering, 0, 4)
                
            else:
                spiller.gyldig = 0
            
            
            if spiller_1:
                ganging = 0
            else:
                ganging = 1
                
            for i in range(4):
                    self.overflate.blit(FONT1.render(priser[i], True, HVIT),
                      (self.oppgraderings_boks.x + self.oppgraderings_boks.b - 50 + (400*ganging), self.oppgraderings_boks.y + BOKS_HØYDE/2 - 10 + (BOKS_HØYDE + BOKS_AVSTAND)*i))
            
        for hendelse in pg.event.get():
            # Sjekker om vi ønsker å lukke vinduet
            if hendelse.type == pg.KEYDOWN:
                if hendelse.key == pg.K_s:
                    self.spiller_1.gyldig += 1
                    self.spiller_1.gyldig_farge = GRØNN
                    
                if hendelse.key == pg.K_k:
                    self.spiller_2.gyldig += 1
                    self.spiller_2.gyldig_farge = GRØNN
                    
                if hendelse.type == pg.QUIT:
                    if self.spiller_spill == True:
                        self.spiller_spill = False
                        
                    self.kjører = False # Spillet skal avsluttes
                    
                    
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
                            
                        spiller.kule_liste = []
                        
                    self.spiller_1.gyldig_farge = GRØNN
                    self.spiller_2.gyldig_farge = GRØNN
                    
                    self.penge_x = random.randint(PLATFORM_BREDDE + 50, BREDDE-PLATFORM_BREDDE - 50)
                    
                    self.start_tid = time.time()
                    self.gyldig_spilling = True
    
    
                if hendelse.key == pg.K_w:
                    self.kjøpe_oppgraderinger(self.spiller_1, self.priser_1, self.poeng_1)
                    
                if hendelse.key == pg.K_i:
                    self.kjøpe_oppgraderinger(self.spiller_2, self.priser_2, self.poeng_2)
        
        # Liste med oppgraderingstekster
        oppgraderingstekster = ["+ 10 ammo", "Større kule", "Øke skuddfart", "Ta poeng"]
        
        # Tegner oppgraderingstekstene
        for i in range(4):
            self.oppgraderingstekst(oppgraderingstekster[i], i)
            self.oppgraderingstekst(oppgraderingstekster[i], i, spiller_1 = False)


    def kjøpe_oppgraderinger(self, spiller, priser, poeng):
        
        if poeng < int(priser[spiller.gyldig]):
            spiller.gyldig_farge = RØD
        else:
            skudd_lyd = pg.mixer.Sound("kjøpe_oppgradering.mp3")
            skudd_lyd.set_volume(0.5)
            skudd_lyd.play()
        
            gyldig_betaling = True
            if spiller.gyldig == 0:
                spiller.ammo += 10
                print(spiller.ammo_pris)
                spiller.ammo_pris = str(int(spiller.ammo_pris)*2)
                print(spiller.ammo_pris)
                            
            if spiller.gyldig == 1:
                spiller.kule_radius += 1
                spiller.kule_pris = str(int(spiller.kule_pris)*2)
                
            if spiller.gyldig == 2:
                spiller.kule_fart += 3
                print(spiller.kule_fart_pris)
                spiller.kule_fart_pris = str(int(spiller.kule_fart_pris)*2)
                print(spiller.kule_fart_pris)
               
            if spiller.gyldig == 3:
                print(self.spiller_poeng_ordbok[spiller])
                if self.spiller_poeng_ordbok[spiller] == 1:
                    if self.poeng_2 > 1:
                        self.poeng_2 = self.poeng_2//2
                        self.spiller_1.stjele_pris = str(int(self.spiller_1.stjele_pris)*2)
                    else:
                        gyldig_betaling = False

                else:
                    if self.poeng_1 > 1:
                        self.poeng_1 = self.poeng_1//2
                        self.spiller_2.stjele_pris = str(int(self.spiller_2.stjele_pris)*2)
                    else:
                        gyldig_betaling = False
                        
            if gyldig_betaling:
                if self.spiller_poeng_ordbok[spiller] == 1:
                    self.poeng_1 -= int(self.priser_1[self.spiller_1.gyldig])
                else:
                    self.poeng_2 -= int(self.priser_2[self.spiller_2.gyldig])
            else:
                spiller.gyldig_farge = RØD
    
    
    def oppgraderingstekst(self, tekst, i, spiller_1 = True):
        if spiller_1:
            gange = 0
        else:
            gange = 1
        
        self.overflate.blit(FONT2.render(tekst, True, HVIT),
            (self.oppgraderings_boks.x + 20 + (400*gange), self.oppgraderings_boks.y + BOKS_HØYDE/2 + (BOKS_HØYDE + BOKS_AVSTAND)*i - 5))
            
                
            
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