
import pygame 
import sys
from scripts.Entities import PysicEntitiey
from scripts.Utils import load_imge, load_tilemap_imges
from scripts.Tilemap import Tilemap
from scripts.Cloud import Clouds
from scripts.Menu import Menu
from scripts.Coins import Coins, CoinCollector

class Game:
    def __init__(self): 
        pygame.init() 
        pygame.display.set_caption("Ludo Anni")
        self.Width=1280
        self.Height=960
        self.score= 0
        self.screen = pygame.display.set_mode((self.Width, self.Height))
        self.display = pygame.Surface(((self.Width/2),(self.Height/2)))
        self.clock = pygame.time.Clock()
        self.movement =[False,False]
        self.assets = {
            'decor': load_tilemap_imges('tiles/decor'),            
            'grass': load_tilemap_imges('tiles/grass'),
            'stone': load_tilemap_imges('tiles/stone'),
            'cloud': load_tilemap_imges('clouds'),

            'menu_background': load_imge('entities/player.png'),
            'coin': load_imge('entities/coin.png'),
            'player': load_imge('entities/player.png'),
        }
        self.clouds = Clouds(self.assets['cloud'], count=24)
        self.player = PysicEntitiey(self, 'player',(250,150),(16,16))
        self.coin = Coins(self, 'coin',(0,0), (15,16))
        self.coin_collector = CoinCollector(self.player, [self.coin], self.score) 
        self.tilemap = Tilemap(self, tile_size=16)
        self.tilemap.load('map.json')
        #self.coin_collector = CoinCollector(self.Width,self.Height) 
        #self.coin = CoinCollector(self.Width, self.Height)
        
        self.scroll = [0,0]
        self.music_enabled= False

        coin1 = Coins(self, 'coin', (80, 0), (15,16))
        coin2 = Coins(self, 'coin', (200, -20), (15,16))
        coin3 = Coins(self, 'coin', (280, 0),(15,16))
        coin4 = Coins(self, 'coin', (350, 0),(15,16))
        coin5 = Coins(self, 'coin', (500, 0),(15,16))
        self.coin_collector.add_coin(coin1)
        self.coin_collector.add_coin(coin2)
        self.coin_collector.add_coin(coin3)
        self.coin_collector.add_coin(coin4)
        self.coin_collector.add_coin(coin5)

        self.font_score =  pygame.font.SysFont("Bauhaus 93", 60)
        self.text_col_score = (0,0,0)
    
    def score_text(self,text,font,text_col,pos_x,pos_y):
        img = font.render(text,True,text_col)
        self.display.blit(img,(pos_x,pos_y))
    


    def start_game(self):
        while True:
            self.score = self.coin_collector.score
            self.display.fill((14, 186, 250))
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30  
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            self.score= self.coin_collector.score
            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)

            self.tilemap.render(self.display, offset=render_scroll)

            for coin in self.coin_collector.coins:
                pygame.draw.rect(self.screen, (255, 0, 0), coin.rect())

            if self.coin_collector.update(self.player.collisions) == False:
                for coin in self.coin_collector.coins:
                    coin.render(self.display, offset=render_scroll, coin=coin)
                    coin.update(self.tilemap, (self.movement[1], 0))

            if self.coin_collector.score == 5 and self.player.pos[1]==-64 :
                Game.finish(self)

            ''' self.score_text('X' + str(self.coin_collector.score), self.font_score, self.text_col_score, (self.Width//2), (self.Height//2))
            print(self.coin_collector.score)'''

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)

            if self.player.pos[1] > 250:
                self.player.pos[0] = 250
                self.player.pos[1] = 150
    

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Game.paus(self)
                        
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.movement[1] = True    
                    if event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_SPACE:
                        if self.player.jump == 1:
                            self.player.velocity[1] = -3.5
                            self.player.jump -= 1 

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.movement[1] = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))  
            pygame.display.update()
            self.clock.tick(60)


    def Music(self):
        options = ["Music On", "Music Off", "Back"]
        menu = Menu(options, 1280, 960)
        selected_option = menu.display(self.screen)
        if selected_option == "Music On":
            pygame.mixer.music.load('data/sinnesloschen-beam-117362.mp3')
            pygame.mixer.music.play(-1)
            pygame.mixer.music.unpause()
            self.music_enabled = True
            Game.run(self)
        elif selected_option == "Music Off":
            pygame.mixer.music.pause()
            self.music_enabled = False
            Game.run(self)
        elif selected_option == "Back":
            Game.run(self)

    def run(self):
        options = ["Start", "Settings", "Exit"]
        menu = Menu(options, 1280, 960)
        selected_option = menu.display(self.screen)
        print("Selected Option:", selected_option)
        if selected_option == "Start":
            self.start_game()
        if selected_option == "Settings":
            self.Music()
        if selected_option == "Exit":
            pygame.quit()
            sys.exit()
    def paus(self):
        options = ["Restart", "Contineu", "Settings", "Exit"]
        menu = Menu(options, 1280, 960)
        selected_option = menu.display(self.screen)
        print("Selected Option:", selected_option)
        if selected_option == "Restart":
            pass
        if selected_option == "Contineu":
            self.start_game()
        if selected_option == "Settings":
            self.Music()
        if selected_option == "Exit":
            pygame.quit()
            sys.exit()
    def finish(self):
        options = ["Exit"]
        menu = Menu(options, 1280, 960)
        selected_option = menu.display(self.screen)
        print("Selected Option:", selected_option)
        if selected_option == "Exit":
            pygame.quit()
            sys.exit()
    

if __name__ == "__main__":
    Game().run()