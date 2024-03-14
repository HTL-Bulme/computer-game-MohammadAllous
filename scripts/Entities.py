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

    def update(self, movement= (0, 0)):
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.pos[0] += frame_movement[0]
        self.pos[1] += frame_movement[1]

        self.velocity[1] = min(5, self.velocity[1] + 0.1) # hier wird ein max für die grawitation gesetzt (5)
    
    def render(self, surf):
        surf.blit(self.game.assets['player'],self.pos)
