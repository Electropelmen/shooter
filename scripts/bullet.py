from .sprite import Sprite

class Bullet(Sprite):
    def update(self):
        self.rect.y -= self.speed