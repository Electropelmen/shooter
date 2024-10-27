import pygame
import os
import sys
def load_image(*paths, size, colorkey):
    'path: путь к картинке'
    'size: размер картинки'
    'colorkey: цвет, который отвечает за прозрачность'
    path = get_path(*paths)
    image = pygame.image.load(path).convert()
    image = pygame.transform.scale(image, size)
    image.set_colorkey(colorkey)
    return image

base_path = getattr(sys, '_MEYPASS', os.path.abspath(os.path.dirname('main.py')))
def get_path(*paths):
    path = os.path.join(base_path , *paths)
    return path