import pygame


class Coins:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.pos = list(pos)
        self.type = e_type
        self.size= size
        self.count = 0
        self.velocity = [0, 0]


    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1]) 

    # Override the update method to remove movement for the enemy
    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {'top': False, 'bottom': False, 'left': False, 'right': False}
        # No movement for the enemy
        frame_movement = (0,self.velocity[1])
        self.pos[1] += frame_movement[1]
        
        entity_rect = self.rect()
        for rect in tilemap.physic_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['bottom'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['top'] = True
                self.pos[1] = entity_rect.y

        for rect in tilemap.physic_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x
        
        self.velocity[1] = min(4, self.velocity[1] + 0.1)
        
        if self.collisions['bottom'] or self.collisions['top']:
            self.velocity[1] = 0

    def render(self, surf, offset,coin):
        
        surf.blit(self.game.assets['coin'],(self.pos[0]- offset[0], self.pos[1]- offset[1]))

class CoinCollector:
    def __init__(self, player, coins, score):
        self.player = player
        self.coins = []
        self.dead = False
        self.score = score

    def add_coin(self, coin):
        self.coins.append(coin)

    def check_collisions(self ,player_rect):
        player_rect = self.player.rect()
         
        for coin in self.coins[:]:
            coins_rect = coin.rect()
            if player_rect.colliderect(coins_rect):
                self.coins.remove(coin)  
                self.score += 1
                self.dead=True
                return

    def update(self,player_rect):
        self.check_collisions(player_rect) 
        result = self.dead
        self.dead= False
        return result