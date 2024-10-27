import pygame
from random import randint
from time import time
from scripts.player import Player
from scripts.functions import load_image
from scripts.bullet import Bullet
from scripts.enemy import Enemy

pygame.init()


flags = pygame.RESIZABLE | pygame.SCALED
window = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)
big_font = pygame.font.Font(None, 64)


FPS = 60


background = load_image('images','background.png', size=(800, 600), colorkey=None)
bullet_image = load_image('images','bullet.png', size=(50, 40), colorkey=(255, 255, 255))
enemy_image = load_image('images','enemy.png', size=(90, 90), colorkey=(0, 0, 0))
player_image = load_image('images','player.png', size=(90, 90), colorkey=(255,255,255))
player = Player(400, 550, player_image, 6, 3)
bullets = list()
enemies = list()

spawn_delta = 3.5
timer = time()
score = 0

game = True
died = False

while game:
    #Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            if died:
                died = False
                bullets.clear()
                enemies.clear()
                player.health = 3
                player.rect.center = (400, 550)
                score = 0
            if event.key == pygame.K_SPACE and not died:
                bullets.append(Bullet(player.rect.centerx, player.rect.y, bullet_image, 10))

    #Обновление объектов
    

    if not died:
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
            if enemy.is_collide(player):
                player.get_damage()
                enemies.remove(enemy)
                died = player.health <= 0
            elif enemy.health <= 0:
                score += 1
                enemies.remove(enemy)
        

    #Отриисовка объектов
    window.blit(background, (0,0))
    player.render(window)
    for enemy in enemies:
        enemy.render(window)
    for bullet in bullets:
        bullet.render(window)
    
    text = 'Очки: '+ str (score)    
    image_text = font.render(text, True, (255,255,255))
    image_rect = image_text.get_rect(midtop = (400, 0))
    window.blit(image_text, image_rect)

    text_hp = 'Жизни: '+ str (player.health)    
    image_text_hp = font.render(text_hp, True, (255,255,255))
    image_rect_hp = image_text.get_rect(topleft = (0, 0))
    window.blit(image_text_hp, image_rect_hp)
    if died:
        text_die = 'YOU DIED!!!'
        image_text_die = big_font.render(text_die, True, (255, 50, 50))
        image_rect_die = image_text_die.get_rect(center = (400, 300))
        window.blit(image_text_die, image_rect_die)

        text_die = 'Нажмите любую клавишу, чтобы начать заново'
        image_text_die = font.render(text_die, True, (255, 255, 255))
        image_rect_die = image_text_die.get_rect(center = (400, 400))
        window.blit(image_text_die, image_rect_die)        
    pygame.display.update()
    clock.tick(60)
    