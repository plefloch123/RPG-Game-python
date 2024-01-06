import pygame
from math import sin

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2(0,0)
    
    def move(self, speed):
		# vector magnitude is normalised to 1 for each directions
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
              
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    # if we are moving right, set the right side of player to the left side of the obstacle we hit
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    # if we are moving left, set our left side of player to the right side of the obstacle we hit
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    # if we are moving down, set the bottom side of player to the top side of the obstacle we hit
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    # if we are moving up, set our top side of player to the bottom side of the obstacle we hit
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0