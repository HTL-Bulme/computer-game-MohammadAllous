import pygame

#git status 
#git add .\<folder name>\<Datai name>
#git commit -m "<änderungen Namen>"
#git status 
#git push 
#git status 

class PysicEntitiey:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.pos = list(pos)
        self.type = e_type
        self.size= size
        self.velocity = [0, 0]
        self.jump = 1
        self.collisions ={'up': False, 'down': False, 'left': False, 'right': False} #von welche seite hat den spieler kontankt mit ...
        self.speed = 2

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1]) 

    def update(self, tilemap,movement= (0, 0)):
        self.collisions ={'top': False, 'bottom': False, 'left': False, 'right': False}

        frame_movement = ((movement[0]*self.speed) + self.velocity[0]), (movement[1] + (self.velocity[1]))

        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physic_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right  = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left  = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physic_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom  = rect.top
                    self.collisions['bottom'] = True
                    self.jump = 1
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['top'] = True
                self.pos[1] = entity_rect.y

        self.velocity[1] = min(5, self.velocity[1] + 0.1) # hier wird ein max für die grawitation gesetzt (5)


        if self.collisions['bottom'] or self.collisions['top']: # um den gravitation zruck zu setzten 
            self.velocity[1] = 0

    def render(self, surf, offset):
        surf.blit(self.game.assets['player'],(self.pos[0]- offset[0], self.pos[1]- offset[1]))