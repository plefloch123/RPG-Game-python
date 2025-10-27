import pygame
import sys
from settings import *
from debug import debug
from level import Level


class Game:
    def __init__(self):

        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption('Zelda')
        self.clock = pygame.time.Clock()

        # create level immediately so the game is visible behind the intro overlay
        self.level = Level()
        # menu / intro state: show animated title image, press SPACE to unpause
        self.menu_active = True

        # load menu image and prepare animation

        menu_img = pygame.image.load('../graphics/ui/main_menu/legend_of_python.png').convert_alpha()
        sw, sh = self.screen.get_size()
        # scale menu image to ~70% width
        target_w = int(sw * 0.7)
        mw, mh = menu_img.get_size()
        scale_h = int(mh * (target_w / mw))
        self.menu_surf = pygame.transform.smoothscale(menu_img, (target_w, scale_h))
        self.menu_start_time = pygame.time.get_ticks()
        # make the intro animation slower and start from slightly below center (not the very bottom)
        self.menu_anim_duration = 1600  # ms (slower)
        # initial positions for animation: start a bit down the screen and move to near-top
        self.menu_start_y = int(sh * 0.60)
        self.menu_target_y = int(sh * 0.04)

        # sound (optional)
        try:
            main_sound = pygame.mixer.Sound('../audio/main.ogg')
            main_sound.play(-1)
            main_sound.set_volume(0.1)
        except Exception:
            pass

    # Event loop
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m and self.level:
                        self.level.toggle_menu()
                    # start game (unpause) on space when menu active
                    if event.key == pygame.K_SPACE and self.menu_active:
                        self.menu_active = False
                # handle game over button clicks
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if getattr(self.level, 'game_over', False):
                        pos = event.pos
                        if hasattr(self.level, 'ui'):
                            ui = self.level.ui
                            # Try Again -> recreate the level
                            if hasattr(ui, 'try_again_rect') and ui.try_again_rect.collidepoint(pos):
                                self.level = Level()
                            # Exit -> quit the game
                            if hasattr(ui, 'exit_rect') and ui.exit_rect.collidepoint(pos):
                                pygame.quit()
                                sys.exit()

            # draw
            self.screen.fill(WATER_COLOR)

            # if menu active, let the world keep updating but disable player control, then animate the menu image on top
            if self.menu_active:
                # disable player control but keep world updates
                if self.level and hasattr(self.level, 'player'):
                    self.level.player.can_control = False
                # run one frame of the level (updates + draw)
                if self.level:
                    self.level.run()
                now = pygame.time.get_ticks()
                elapsed = now - self.menu_start_time
                t_raw = min(1.0, elapsed / self.menu_anim_duration)
                # ease-out cubic for a smoother, slower finish
                t = 1 - (1 - t_raw) ** 3
                y = int(self.menu_start_y + (self.menu_target_y - self.menu_start_y) * t)
                # fade follows eased progress for nicer effect
                alpha = max(0, min(255, int(255 * t)))
                # blit menu image with alpha (no dim overlay so game remains fully visible)
                img = self.menu_surf.copy()
                img.set_alpha(alpha)
                rect = img.get_rect(midtop=(self.screen.get_width() // 2, y))
                self.screen.blit(img, rect)
                # small prompt
                font = pygame.font.Font(UI_FONT, 26)
                prompt = font.render('Press SPACE to start', True, (255, 255, 255))
                p_rect = prompt.get_rect(center=(self.screen.get_width() // 2, rect.bottom + 40))
                self.screen.blit(prompt, p_rect)

            else:
                # run the level once started
                if self.level:
                    self.level.run()

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()