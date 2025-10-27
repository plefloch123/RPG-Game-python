import pygame
from settings import *

class UI:
    def __init__(self):
        
        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        # convert weapon dictionary
        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)

        # convert magic dictionary
        self.magic_graphics = []
        for magic in magic_data.values():
            path = magic['graphic']
            magic = pygame.image.load(path).convert_alpha()
            self.magic_graphics.append(magic)

        # preload game over graphic and button images
        self.game_over_surf = pygame.image.load('../graphics/ui/game_over/game_over.png').convert_alpha()
        self.try_again_surf = pygame.image.load('../graphics/ui/game_over/try_again.png').convert_alpha()
        self.exit_surf = pygame.image.load('../graphics/ui/game_over/exit.png').convert_alpha()

    def show_bar(self, current, max_amount, bg_rect, color):
        # draw background
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # converting sytat to pixel
        ratio = current / max_amount
        current_width = bg_rect.width * ratio # 200 * ratio (example at half life ratio = 0.5 so current width = 100)
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # drawing the bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright = (x, y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)

    def selection_box(self, left, top, has_switched):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 1)
        return bg_rect
    
    def weapon_overlay(self, weapon_index, has_switched):
        bg_rect = self.selection_box(10, 630, has_switched) # weapon
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center = bg_rect.center)
        self.display_surface.blit(weapon_surf, weapon_rect)

    def magic_overlay(self, magic_index, has_switched):
        bg_rect = self.selection_box(80, 635, has_switched) # weapon
        magic_surf = self.magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center = bg_rect.center)
        self.display_surface.blit(magic_surf, magic_rect)

    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)
        
        # show experience bar
        self.show_exp(player.exp)

        # weapon and magic box
        self.weapon_overlay(player.weapon_index, not player.can_switch_weapon)
        self.magic_overlay(player.magic_index, not player.can_switch_magic)

    def show_game_over(self):
        # draw the game over image near the top center (scaled down) and render two image-buttons below it
        ds_rect = self.display_surface.get_rect()
        center_x = ds_rect.centerx

        # scale the image to at most 70% of width and 50% of height (make it noticeably bigger)
        max_width = int(ds_rect.width * 0.85)
        max_height = int(ds_rect.height * 0.85)
        orig_w, orig_h = self.game_over_surf.get_size()
        # fit to width first
        scale_w = min(orig_w, max_width)
        scale_h = int(orig_h * (scale_w / orig_w))
        # if height exceeds cap, fit to height instead
        if scale_h > max_height:
            scale_h = max_height
            scale_w = int(orig_w * (scale_h / orig_h))
        scaled_surf = pygame.transform.smoothscale(self.game_over_surf, (scale_w, scale_h))

        # position the game over image at middle-top (a bit lower than the absolute top)
        top_margin = 10
        go_rect = scaled_surf.get_rect(midtop=(center_x, top_margin))

        # dim the full screen slightly
        overlay = pygame.Surface(self.display_surface.get_size()).convert_alpha()
        overlay.fill((0, 0, 0, 160))
        self.display_surface.blit(overlay, (0, 0))

        # blit the scaled image
        self.display_surface.blit(scaled_surf, go_rect)

        # buttons: Try Again and Exit, centered under the image using image assets
        spacing = 12
        # place buttons a short distance below the image so gap is small
        buttons_y = go_rect.bottom - 150

        # button max width percent
        max_button_w = int(ds_rect.width * 0.18)

        def scaled_button_surf(surf, hover=False):
            ow, oh = surf.get_size()
            scale_w = min(ow, max_button_w)
            scale_h = int(oh * (scale_w / ow))
            if hover:
                # grow a bit more on hover for better feedback
                scale_w = int(scale_w * 1.12)
                scale_h = int(scale_h * 1.12)
            return pygame.transform.smoothscale(surf, (scale_w, scale_h))

        mouse_pos = pygame.mouse.get_pos()

        # initial scaled (non-hover) surfaces
        ta_s = scaled_button_surf(self.try_again_surf)
        ex_s = scaled_button_surf(self.exit_surf)

        ta_rect = ta_s.get_rect()
        ex_rect = ex_s.get_rect()

        total_w = ta_rect.width + ex_rect.width + spacing
        start_x = center_x - total_w // 2

        # compute center positions for each button so scaling preserves centroid
        ta_center = (start_x + ta_rect.width // 2, buttons_y + ta_rect.height // 2)
        ex_center = (start_x + ta_rect.width + spacing + ex_rect.width // 2, buttons_y + ex_rect.height // 2)

        # set rects centered at those positions
        ta_rect = ta_s.get_rect(center=ta_center)
        ex_rect = ex_s.get_rect(center=ex_center)

        # hover: if mouse over, re-scale and update rect but keep the same center
        if ta_rect.collidepoint(mouse_pos):
            ta_s = scaled_button_surf(self.try_again_surf, hover=True)
            ta_rect = ta_s.get_rect(center=ta_center)
        if ex_rect.collidepoint(mouse_pos):
            ex_s = scaled_button_surf(self.exit_surf, hover=True)
            ex_rect = ex_s.get_rect(center=ex_center)

        # store rects so the main loop can check clicks
        self.try_again_rect = ta_rect
        self.exit_rect = ex_rect

        # blit buttons
        self.display_surface.blit(ta_s, ta_rect)
        self.display_surface.blit(ex_s, ex_rect)



