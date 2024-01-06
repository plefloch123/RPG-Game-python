import pygame 
from settings import *

# Inherit the sprite class
class Tile(pygame.sprite.Sprite):
	# Takes the position and the groups it belongs to
	def __init__(self,pos,groups, sprite_type, surface = pygame.Surface((TILESIZE,TILESIZE))):
		super().__init__(groups)
		self.sprite_type = sprite_type
		y_offset = HIBOX_OFFSET[sprite_type]
		self.image = surface
		# correct if the image is not the same size as the tile
		if sprite_type == 'object':
			# do an offset for the object tiles
			self.rect = self.image.get_rect(topleft = (pos[0],pos[1] - self.image.get_height() + TILESIZE))
		else:
			self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0,y_offset) # make the hitbox smaller than the image