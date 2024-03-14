import pygame
import os

BASE_IMG_PATH = 'data/images/'

def load_imge(path): 
    img = pygame.image.load(BASE_IMG_PATH + path).convert() #convert() verbesert die bilder so wie quality 
    img.set_colorkey((0,0,0)) 
    return img

def load_tilemap_imges(path):
    imges = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)): #dass tut die ganzen tile in diesm folder losten
        imges.append(load_imge(path+ '/'+ img_name))
    return imges