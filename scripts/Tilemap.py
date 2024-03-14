class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {} # mit dem zuarbeiten ist viel effizienter mit teilmap"Buch" als mit liesten 
                        # so muss den abstnd zwischen den tiele nicht ausgefullt werden 
        self.offgrid_tiles = []


        for width in range(30):
            self.tilemap[f'{width};10'] = {'type': "grass", 'variant':1, 'pos':(width, 10)}
            for height in range(10):
                self.tilemap[f'{width}; {height + 11}'] = {'type': "grass", 'variant':5, 'pos':(width, 11 + height)}
        for i in range(15):
            #self.tilemap['10;' + str(i + 5)] = {'type': "stone", 'variant':1, 'pos':(10, 5 + i)}
            pass

    
    def render(self, surf):
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], tile['pos'])

        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0]* self.tile_size, tile['pos'][1]* self.tile_size))
        