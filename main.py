import pygame
from random import randint
from time import time
from scripts.player import Player
from scripts.functions import load_image
from scripts.bullet import Bullet
from scripts.enemy import Enemy


flags = pygame.RESIZABLE | pygame.SCALED
window = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

FPS = 60


background = load_image('images\\background.png', (800, 600), None)
bullet_image = load_image('images\\bullet.png', (50, 40), (255, 255, 255))
enemy_image = load_image('images\\enemy.png', (90, 90), (0, 0, 0))
player_image = load_image('images\\player.png', (90, 90), (255,255,255))
player = Player(400, 550, player_image, 5)
bullets = list()
enemies = list()

spawn_delta = 3.5
timer = time()

game = True

while game:
    #Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(Bullet(player.rect.centerx, player.rect.y, bullet_image, 10))

    #Обновление объектов
    player.update()
    for bullet in bullets:
        bullet.update()
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    
    delta = time() - timer
    if delta >= spawn_delta:
        timer = time()
        x = randint(enemy_image.get_width()//2, 800 - enemy_image.get_width()//2)
        y = enemy_image.get_height() // 2
        speed = randint(5000, 7000)/1000
        health = randint(1, 3)
        enemies.append(Enemy(x, y, enemy_image, speed, health))
    for enemy in enemies:
        enemy.update()
        for bullet in bullets:
            if enemy.is_collide(bullet):
                bullets.remove(bullet)
                enemy.get_damage()
        if enemy.health <= 0:
            enemies.remove(enemy)
    

    #Отриисовка объектов
    window.blit(background, (0,0))
    player.render(window)
    for enemy in enemies:
        enemy.render(window)
    for bullet in bullets:
        bullet.render(window)
        
    pygame.display.update()
    clock.tick(60)
    