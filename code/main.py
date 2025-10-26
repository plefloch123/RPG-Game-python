import pygame, sys
from settings import *
from debug import debug
from level import Level

class Game:
	def __init__(self):
		  
		# general setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
		pygame.display.set_caption('Zelda')
		self.clock = pygame.time.Clock()

		self.level = Level()

		# sound
		main_sound = pygame.mixer.Sound('../audio/main.ogg')
		main_sound.play(-1)
		main_sound.set_volume(0.1)
	
	# Event loop
	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_m:
						self.level.toggle_menu()

				# handle game over button clicks
				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1 and getattr(self.level, 'game_over', False):
						pos = event.pos
						# protect against missing ui (should exist)
						if hasattr(self.level, 'ui'):
							ui = self.level.ui
							# Try Again -> recreate the level
							if hasattr(ui, 'try_again_rect') and ui.try_again_rect.collidepoint(pos):
								self.level = Level()
							# Exit -> quit
							if hasattr(ui, 'exit_rect') and ui.exit_rect.collidepoint(pos):
								pygame.quit()
								sys.exit()

			self.screen.fill(WATER_COLOR)
			self.level.run()
			pygame.display.update()
			self.clock.tick(FPS)
 
if __name__ == '__main__':
	game = Game()
	game.run()