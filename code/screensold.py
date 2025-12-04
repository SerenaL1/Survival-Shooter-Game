from settings import *
from utils import get_asset_path

class Screen:
    """Base class for all screens"""
    def __init__(self, display_surface, clock):
        self.display_surface = display_surface
        self.clock = clock
        self.button_font = pygame.font.Font(None, 50)
        self.title_font = pygame.font.Font(None, 80)
        self.text_font = pygame.font.Font(None, 40)
    
    def create_button(self, text, x, y, width, height, color, hover_color):
        """Helper method to create and draw a button"""
        button_rect = pygame.Rect(x, y, width, height)
        mouse_pos = pygame.mouse.get_pos()
        mouse_hover = button_rect.collidepoint(mouse_pos)
        
        # Draw button
        current_color = hover_color if mouse_hover else color
        pygame.draw.rect(self.display_surface, current_color, button_rect, border_radius=10)
        pygame.draw.rect(self.display_surface, (255, 255, 255), button_rect, 3, border_radius=10)
        
        # Draw text
        button_text = self.button_font.render(text, True, (255, 255, 255))
        button_text_rect = button_text.get_rect(center=button_rect.center)
        self.display_surface.blit(button_text, button_text_rect)
        
        return button_rect, mouse_hover


class StartScreen(Screen):
    """Start screen with game rules and play button"""
    def show(self):
        # Try to load start screen image
        try:
            start_img = pygame.image.load(get_asset_path('images', 'ui', 'start_screen.png')).convert_alpha()
            start_img = pygame.transform.scale(start_img, (WINDOW_WIDTH, WINDOW_HEIGHT))
            has_start_img = True
        except:
            has_start_img = False
        
        # Button setup
        button_width, button_height = 200, 80
        button_x = WINDOW_WIDTH // 2 - button_width // 2
        button_y = WINDOW_HEIGHT - 150
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if pygame.Rect(button_x, button_y, button_width, button_height).collidepoint(mouse_pos):
                        waiting = False
            
            # Draw background
            if has_start_img:
                self.display_surface.blit(start_img, (0, 0))
            else:
                self.display_surface.fill((20, 20, 40))
                self._draw_rules()
            
            # Draw play button
            self.create_button("PLAY", button_x, button_y, button_width, button_height, 
                             (50, 150, 50), (70, 200, 70))
            
            pygame.display.update()
            self.clock.tick(60)
    
    def _draw_rules(self):
        """Draw game rules on start screen"""
        # Title
        title = self.title_font.render("SURVIVOR", True, (255, 255, 255))
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 100))
        self.display_surface.blit(title, title_rect)
        
        # Rules
        rules = [
            "OBJECTIVE:",
            "Find your way HOME in the forest!",
            "",
            "CONTROLS:",
            "WASD or Arrow Keys - Move",
            "Left Click - Shoot laser",
            "",
            "RULES:",
            "• Avoid monsters or shoot them",
            "• You have 5 hearts",
            "• Find the HOME to win!"
        ]
        
        y_offset = 200
        for line in rules:
            if line in ["OBJECTIVE:", "CONTROLS:", "RULES:"]:
                text = self.text_font.render(line, True, (255, 200, 100))
            else:
                text = self.text_font.render(line, True, (255, 255, 255))
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, y_offset))
            self.display_surface.blit(text, text_rect)
            y_offset += 40


class WinScreen(Screen):
    """Win screen with play again button"""
    def show(self):
        # Load win image - FILL THE ENTIRE SCREEN
        try:
            win_img = pygame.image.load(get_asset_path('images', 'ui', 'you_win.png')).convert_alpha()
            # Scale to fill the entire window
            win_img = pygame.transform.scale(win_img, (WINDOW_WIDTH, WINDOW_HEIGHT))
            has_win_img = True
        except:
            has_win_img = False
        
        # Button setup
        button_width, button_height = 250, 80
        button_x = WINDOW_WIDTH // 2 - button_width // 2
        button_y = WINDOW_HEIGHT - 150
        
        waiting = True
        play_again = False
        
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if pygame.Rect(button_x, button_y, button_width, button_height).collidepoint(mouse_pos):
                        waiting = False
                        play_again = True
            
            # ALWAYS clear the screen first
            self.display_surface.fill((0, 50, 0))  # Dark green
            
            # Draw win image
            if has_win_img:
                # Draw the full-screen image
                self.display_surface.blit(win_img, (0, 0))
            else:
                # Fallback text
                win_text = self.title_font.render("YOU WIN!", True, (255, 215, 0))
                win_rect = win_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))
                self.display_surface.blit(win_text, win_rect)
                
                subtitle = self.text_font.render("You made it home!", True, (255, 255, 255))
                subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
                self.display_surface.blit(subtitle, subtitle_rect)
            
            # Draw play again button on top
            self.create_button("PLAY AGAIN", button_x, button_y, button_width, button_height,
                             (50, 150, 50), (70, 200, 70))
            
            pygame.display.update()
            self.clock.tick(60)
        
        # Clear the screen before returning to ensure clean transition
        self.display_surface.fill((0, 0, 0))
        pygame.display.update()
        
        return play_again


class GameOverScreen(Screen):
    """Game over screen with play again button"""
    def show(self):
        # Load game over image - scale to fit most of the screen
        try:
            game_over_img = pygame.image.load(get_asset_path('images', 'ui', 'game_over.png')).convert_alpha()
            # Scale to fit width while maintaining aspect ratio
            target_width = int(WINDOW_WIDTH * 0.8)  # 80% of screen width
            aspect_ratio = game_over_img.get_height() / game_over_img.get_width()
            target_height = int(target_width * aspect_ratio)
            game_over_img = pygame.transform.scale(game_over_img, (target_width, target_height))
            has_game_over_img = True
        except:
            has_game_over_img = False
        
        # Button setup
        button_width, button_height = 250, 80
        button_x = WINDOW_WIDTH // 2 - button_width // 2
        button_y = WINDOW_HEIGHT - 150
        
        waiting = True
        play_again = False
        
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if pygame.Rect(button_x, button_y, button_width, button_height).collidepoint(mouse_pos):
                        waiting = False
                        play_again = True
            
            # Draw background
            self.display_surface.fill((40, 20, 20))  # Dark red
            
            # Draw game over image or text
            if has_game_over_img:
                img_rect = game_over_img.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
                self.display_surface.blit(game_over_img, img_rect)
            else:
                game_over_text = self.title_font.render("GAME OVER", True, (255, 50, 50))
                text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))
                self.display_surface.blit(game_over_text, text_rect)
                
                subtitle = self.text_font.render("You ran out of hearts!", True, (255, 255, 255))
                subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
                self.display_surface.blit(subtitle, subtitle_rect)
            
            # Draw ONLY the play again button
            self.create_button("PLAY AGAIN", button_x, button_y, button_width, button_height,
                             (150, 50, 50), (200, 70, 70))
            
            pygame.display.update()
            self.clock.tick(60)
        
        return play_again