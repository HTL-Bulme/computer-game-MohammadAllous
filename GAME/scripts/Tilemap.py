import pygame
import json

NIEGHBOR_OFFSETS  = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,0), (0,1), (1,-1), (1,0), (1,1)]
PHYSIC_TILES = {'grass', 'stone'} #<= schneller als ein Liste


class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {} # mit dem zuarbeiten ist viel effizienter mit teilmap"Buch" als mit liesten 
                        # so muss den abstnd zwischen den tiele nicht ausgefullt werden 
        self.offgrid_tiles = []

        """
        for width in range(20):
            self.tilemap[f'{width};10'] = {'type': "grass", 'variant':0, 'pos':(width, 10)}
        for height in range(10):
            self.tilemap[f'{width};{height + 11}'] = {'type': "grass", 'variant':5, 'pos':(width, 11 + height)}"""

    def extract(self, id_pairs, keep= False):
        matches=[]
        for tile in self.offgrid_tiles.copy():
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                if not keep:
                    self.offgrid_tiles.remove(tile)

        for loc in self.tilemap:
            tile = self.tilemap[loc]
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                matches[-1]['pos'] = matches[-1]['pos'].copy()
                matches[-1]['pos'][0] *= self.tile_size
                matches[-1]['pos'][1] *= self.tile_size
                if not keep:
                    del self.tilemap[loc]
        return matches

    def tiles_around(self, pos):
        tiles =[]
        tile_loc = (int(pos[0] // self.tile_size),int(pos[1] // self.tile_size))
        for offset in NIEGHBOR_OFFSETS:
            check_loc=  f'{tile_loc[0] + offset[0]}'+';'+f'{tile_loc[1] + offset[1]}'
            #check_loc= tile_loc[0] + offset[0],';',tile_loc[1] + offset[1]
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles

    def save (self, path):
        file = open(path, 'w')#w=schreiben
        json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size}, file)
        file.close()

    def load(self, path):
        file = open(path, 'r')#r=lesen
        map_data =json.load(file)
        file.close()

        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']

    def physic_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSIC_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size)) #<= 4 mal weil es ein recht eck ist so bekommt man die große von den tile in px
        return rects 
    

    def render(self, surf, offset):
        for tile in self.offgrid_tiles:
            if tile['type'] in self.game.assets and tile['variant'] < len(self.game.assets[tile['type']]):
                surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))

        for loc in self.tilemap:
            tile = self.tilemap[loc]
            if tile['type'] in self.game.assets and tile['variant'] < len(self.game.assets[tile['type']]):
                surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
    
