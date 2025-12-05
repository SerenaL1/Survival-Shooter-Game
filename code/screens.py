import pygame
import pygame.freetype
from pygame.sprite import Sprite
from pygame.sprite import RenderUpdates
from enum import Enum
from settings import *
from utils import get_asset_path


# Some definitions for RGB colors used in the game
BLUE = (106, 159, 181)
WHITE = (255, 255, 255)
GREEN = (50, 150, 50)
DARK_GREEN = (70, 200, 70)
RED = (150, 50, 50)
DARK_RED = (200, 70, 70)

# A function that creates text surfaces with a specific style by first creating a font object, then rendering the text onto a surface.
def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()

# A user interface element that can be added to a surface. This creates interactive buttons 
# That can change appearance when the user's mouse hovers over them. It also triggers actions if clicked.
class UIElement(Sprite):

    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):
        self.mouse_over = False

        default_image = create_surface_with_text(
            text=text, font_size=font_size, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        highlighted_image = create_surface_with_text(
            text=text, font_size=int(font_size * 1.2), text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        self.images = [default_image, highlighted_image]

        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position),
        ]

        self.action = action

        super().__init__()

    # This is a property that return the current image based on the state of mouse_over variable. 
    # If mouse is over the button, return highlighted image. otherwise, return normal image.
    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    # Returns either the highlighted rect or default rect at index 0, also based on state of mouse_over.
    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]
   
    # If mouse collides with the button, set the mouse_over state to true. If mouse_up, meaning the mouse 
    # button was just released, then return the action associated with the button.
    
    def update(self, mouse_pos, mouse_up):
        
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    # Draws element onto a pygame surface at the current rect position.
    def draw(self, surface):
        """Draws element onto a surface"""
        surface.blit(self.image, self.rect)

# Defines the possible actions that can result from user interacting with menu screens. 
# User can either start the game, play again, or quit the game.
class ScreenAction(Enum):
    """Actions that can be returned by screens"""
    START_GAME = 1
    PLAY_AGAIN = 2
    QUIT = 3

# Initialize the start screen containing the rules and play button.
class StartScreen:
    def __init__(self, display_surface, clock):
        self.display_surface = display_surface
        self.clock = clock
        self.title_font = pygame.font.Font(None, 80)
        self.text_font = pygame.font.Font(None, 40)
    
    def _draw_rules(self):
        # Title of game
        title = self.title_font.render("Help Susie Get Home", True, WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 100))
        self.display_surface.blit(title, title_rect)
        
        # Rules
        rules = [
            "Susie got lost in the forest, help her find her way back home!",
            "",
            "Arrow Keys - Move",
            "Left Click - Shoot laser",
            "",
            "Avoid monsters or shoot them, but don't let them get too close",
            "You have 5 hearts",
            "There are health packs hidden around the forest"
     ]
        
        y_offset = 200
        for line in rules:
            text = self.text_font.render(line, True, WHITE)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, y_offset))
            self.display_surface.blit(text, text_rect)
            y_offset += 40
    # Show the start screen, creates the play button, and return action when button is clicked
    def show(self):
        # Create buttons
        play_btn = UIElement(
            center_position=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 150),
            font_size=40,
            bg_rgb=GREEN,
            text_rgb=WHITE,
            text="PLAY",
            action=ScreenAction.START_GAME,
        )
        
        buttons = RenderUpdates(play_btn)
        
        return self._game_loop(buttons)
    
    # This runs a loop that handles events like mouse clicks, draws the screen, update the buttons
    # and returns an action when the user clicks on the button. 
    def _game_loop(self, buttons):
        while True:
            mouse_up = False
            for event in pygame.event.get():
                # Look at all the events that happened in a frame. If user clicked close the window, 
                # quit the game.
                if event.type == pygame.QUIT:
                    return ScreenAction.QUIT
                
                # If the left mouse button was released,set mouse_up to true.
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_up = True
            
            # draw background and rules
            self.display_surface.fill((20, 20, 40))
            self._draw_rules()
            
            # update and draw buttons by going through each buttom, and if it was clicked on, get its action.
            for button in buttons:
                ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
                if ui_action is not None:
                    return ui_action
            # Draw all butotons to display surface and update the display.
            buttons.draw(self.display_surface)
            pygame.display.flip()
            self.clock.tick(60)

# The win screen. Loads the win image and renters both a play_again and a quit button.
class WinScreen:
    """Win screen with play again button"""
    def __init__(self, display_surface, clock):
        self.display_surface = display_surface
        self.clock = clock
        self.title_font = pygame.font.Font(None, 80)
        self.text_font = pygame.font.Font(None, 40)
        
        # Load win image
        try:
            self.win_img = pygame.image.load(get_asset_path('images', 'ui', 'you_win.png')).convert_alpha()
            self.win_img = pygame.transform.scale(self.win_img, (WINDOW_WIDTH, WINDOW_HEIGHT))
            self.has_win_img = True
        except:
            self.has_win_img = False
    
    def show(self):
        # Create buttons for play_again and quit.
        play_again_btn = UIElement(
            center_position=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 150),
            font_size=35,
            bg_rgb=GREEN,
            text_rgb=WHITE,
            text="PLAY AGAIN",
            action=ScreenAction.PLAY_AGAIN,
        )
        
        quit_btn = UIElement(
            center_position=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 70),
            font_size=30,
            bg_rgb=RED,
            text_rgb=WHITE,
            text="QUIT",
            action=ScreenAction.QUIT,
        )
        # Create a sprite gorup that contain both buttoms. Then use that as input in the screen loop to get the action from the button
        buttons = RenderUpdates(play_again_btn, quit_btn)
        action = self._game_loop(buttons)

        # If user indciates play_again, return True. otherwise return Flase 
        return action == ScreenAction.PLAY_AGAIN
    # Makes sure there is a screen loop happening in the background
    def _game_loop(self, buttons):
        """Handles screen loop until an action is returned by a button"""
        while True:
            mouse_up = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return ScreenAction.QUIT
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_up = True
            
            # Draw background
            self.display_surface.fill((0, 50, 0))  # Dark green
            
            if self.has_win_img:
                self.display_surface.blit(self.win_img, (0, 0))
            else:
                win_text = self.title_font.render("YOU WIN!", True, (255, 215, 0))
                win_rect = win_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))
                self.display_surface.blit(win_text, win_rect)
                
                subtitle = self.text_font.render("You made it home!", True, WHITE)
                subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
                self.display_surface.blit(subtitle, subtitle_rect)
            
            # Update and draw buttons
            for button in buttons:
                ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
                if ui_action is not None:
                    return ui_action
            
            buttons.draw(self.display_surface)
            pygame.display.flip()
            self.clock.tick(60)


class GameOverScreen:
    """Game over screen with play again button"""
    def __init__(self, display_surface, clock):
        self.display_surface = display_surface
        self.clock = clock
        self.title_font = pygame.font.Font(None, 80)
        self.text_font = pygame.font.Font(None, 40)
        
        # Load game over image
        try:
            self.game_over_img = pygame.image.load(get_asset_path('images', 'ui', 'game_over.png')).convert_alpha()
            # Scale to fit width while maintaining aspect ratio
            target_width = int(WINDOW_WIDTH * 0.8)
            aspect_ratio = self.game_over_img.get_height() / self.game_over_img.get_width()
            target_height = int(target_width * aspect_ratio)
            self.game_over_img = pygame.transform.scale(self.game_over_img, (target_width, target_height))
            self.has_game_over_img = True
        except:
            self.has_game_over_img = False
    
    def show(self):
        """Display game over screen and return whether to play again"""
        # Create buttons
        play_again_btn = UIElement(
            center_position=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 150),
            font_size=35,
            bg_rgb=RED,
            text_rgb=WHITE,
            text="PLAY AGAIN",
            action=ScreenAction.PLAY_AGAIN,
        )
        
        quit_btn = UIElement(
            center_position=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 70),
            font_size=30,
            bg_rgb=(100, 100, 100),
            text_rgb=WHITE,
            text="QUIT",
            action=ScreenAction.QUIT,
        )
        
        buttons = RenderUpdates(play_again_btn, quit_btn)
        
        action = self._game_loop(buttons)
        return action == ScreenAction.PLAY_AGAIN
    
    def _game_loop(self, buttons):
        """Handles screen loop until an action is returned by a button"""
        while True:
            mouse_up = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return ScreenAction.QUIT
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_up = True
            
            # Draw background
            self.display_surface.fill((40, 20, 20))  # Dark red
            
            if self.has_game_over_img:
                img_rect = self.game_over_img.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
                self.display_surface.blit(self.game_over_img, img_rect)
            else:
                game_over_text = self.title_font.render("GAME OVER", True, (255, 50, 50))
                text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))
                self.display_surface.blit(game_over_text, text_rect)
                
                subtitle = self.text_font.render("You ran out of hearts!", True, WHITE)
                subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
                self.display_surface.blit(subtitle, subtitle_rect)
            
            # Update and draw buttons
            for button in buttons:
                ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
                if ui_action is not None:
                    return ui_action
            
            buttons.draw(self.display_surface)
            pygame.display.flip()
            self.clock.tick(60)