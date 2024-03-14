import pygame 
import sys

from scripts.Entities import PysicEntitiey
from scripts.utils import load_imge, load_tilemap_imges
from scripts.Tilemap import Tilemap

class Game: #Classen einbauen wird einfacher zu erwitern 
    def __init__(self): 
        """
        self.img = pygame.image.load('data/images/clouds/cloud_1.png') # Bild auswählen 
        self.img.set_colorkey((0,0,0)) # die ausgewelten farbe wird durchsichtig // 0,0,0 ist schwarz        
        self.img_pos = [180,250]
        self.collision_area = pygame.Rect(50,30,300,50) # 
        """
        pygame.init() 
        pygame.display.set_caption("Game_Lerning") #Name fon programm 
        self.screen = pygame.display.set_mode((800, 600)) # screen große einsetzten 
        self.display = pygame.Surface((400,300)) #zoom

        self.clock = pygame.time.Clock()

        self.movement =[False,False]


        self.assets = {#das ist ein liste mit allen bildern//entities
            'decor': load_tilemap_imges('tiles/decor'),            
            'large_decor': load_tilemap_imges('tiles/large_decor'),
            'stone': load_tilemap_imges('tiles/stone'),

            'grass': load_tilemap_imges('tiles/grass'),
            'player': load_imge('entities/player.png') #hier wierd den path für den spieler gegeben (den utils.py datie verwendet )
        }

        self.player = PysicEntitiey(self, 'player',(50,50), (8,15))

        self.tilemap = Tilemap(self, tile_size=16)

    def run(self): #Funktion zum rufen 
        while True: #einfach wie Loop das die spiele Funktion 
            """       
            self.img_pos[1] += (self.movement[1] - self.movement[0])*5 # boolen werden in int um gewandelt so dass di ekeiden knopf gedrukt wirden, es wird sich nix bewegen 
            self.screen.blit(self.img, self.img_pos) #
           
            img_rect = pygame.Rect(self.img_pos[0], self.img_pos[1], self.img.get_width(), self.img.get_height()) # hier wird den Hitbox erstellt 
            if img_rect.colliderect(self.collision_area):
                pygame.draw.rect(self.screen, (100,50,73), self.collision_area) # hier wird den hitbox auf den screen gezeichnet mit "(100,50,73)" diesem farbe 
            else:
                pygame.draw.rect(self.screen, (200,50,73), self.collision_area)
            """
            self.display.fill((14,186,250)) # hier wird den hintergrund farbe gesetzt 

            self.tilemap.render(self.display)

            self.player.update((self.movement[1] - self.movement[0],0))
            self.player.render(self.display)

            for event in pygame.event.get(): # mit dem können wir den programm zum laufen bringen ohne das windows es schließt 
                if event.type == pygame.QUIT: # hier wir den "x" von spiel funktion gergeben 
                    pygame.quit() # mit dem wird nur pygame geschloßen 
                    sys.exit()  # mit dem wird windows den programm schließen 
                
                if event.type == pygame.KEYDOWN: # Wenn der knopf gedrukt wird // fallender Flanke 
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.movement[1] = True     
                if event.type == pygame.KEYUP: # Wenn der knopf los gelassen wird // steigneder Flanke
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.movement[1] = False

            #self.screen.blit(self.display, (0,0))  <- wie es ausschaut ohne tensform.scale
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))  

            pygame.display.update() #das ist für programm zu zeigen 
            self.clock.tick(60)	# das ist um FPS fix zu stellen 

Game().run() 
