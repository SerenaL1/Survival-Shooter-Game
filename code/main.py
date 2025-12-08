from settings import *
from player import Player
from sprites import GroundSprite, CollisionSprite, Gun, Bullet, Enemy, Home, HealthPack
from pytmx.util_pygame import load_pygame
from random import randint, choice
from groups import AllSprites
from utils import get_asset_path 
from screens import StartScreen, WinScreen, GameOverScreen, ScreenAction



import os

class Game:
    def __init__(self):
        #Initializes the library, creates the game window, and sets the game loop flag to true
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Help Susie Get Home')
        self.clock = pygame.time.Clock()
        self.running = True

        # UI font
        self.wave_text_font = pygame.font.Font(None, 40)
        
        # Adds sprite objects into groups, which are pygame containers
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.home_sprite = pygame.sprite.GroupSingle()
        self.health_pack_sprites = pygame.sprite.Group()

        # laser beam timer
        self.can_shoot = True
        self.shoot_time = 0 
        self.gun_cooldown = GUN_COOLDOWN


        # Initializing the number of waves 
        self.wave_number = 1
        self.enemies_killed = 0
        self.enemies_per_wave = INITIAL_ENEMIES_PER_WAVE

        # game state
        self.game_won = False

        # Spawn enemy ever 2 seconds. Use the spawn_positions list to store enemy spawn positions. 
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, INITIAL_SPAWN_INTERVAL)
        self.spawn_positions = []

        # Load in all images and sprites and set up the game.
        self.load_images()
        self.setup()

    # Function that loads all images. Sets the bullet image to a scaled size. 
    def load_images(self):
        bullet_original = pygame.image.load(get_asset_path('images', 'gun', 'laser.png')).convert_alpha()
        bullet_size = BULLET_SIZE
        self.bullet_surf = pygame.transform.scale(bullet_original, (bullet_size, bullet_size))

    # Stores the heart images in a dictionary with keys being the number of hearts (0 to 5 hearts)
    # in the image (to reflect health level)
        self.heart_images = {}
        scale_factor = HEART_SCALE_FACTOR
        for i in range(1, 6): 
            heart_path = get_asset_path('images', 'ui', f'hearts_{i}-removebg-preview.png')
            heart_surf = pygame.image.load(heart_path).convert_alpha()
            new_width = int(HEART_ORIGINAL_WIDTH * scale_factor)
            new_height = int(HEART_ORIGINAL_HEIGHT * scale_factor)

            # Scale down each heart image
            self.heart_images[i] = pygame.transform.scale(heart_surf, (new_width, new_height))

        # Load enemy frames for each enemy type by looping through the folder storing each enemy type
        # and initializing an empty list fo rall frames of a specific type of enemy
        enemies_path = get_asset_path('images', 'enemies') 
        folders = list(walk(enemies_path))[0][1]
        self.enemy_frames = {}
        for folder in folders:
            folder_full_path = os.path.join(enemies_path, folder)
            for folder_path, _, file_names in walk(folder_full_path):
                self.enemy_frames[folder] = []
                for file_name in sorted(file_names, key=lambda name: int(name.split('.')[0])):
                    full_path = join(folder_path, file_name)
                    surf = pygame.image.load(full_path).convert_alpha()
                    self.enemy_frames[folder].append(surf)
    # Handle player shooting input. If the left mouse is pressed and shooting is allowed, then 
    # calculate the spawn position of bullet as 50 pixels in front of the laser shooter, in the 
    # direction of the player. Then create a bullet sprite with this information. 
    # Disable shooting ability until the cooldown is over
    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            pos = self.gun.rect.center + self.gun.player_direction * BULLET_OFFSET
            Bullet(self.bullet_surf, pos, self.gun.player_direction, (self.all_sprites, self.bullet_sprites))
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

    # Manage shooting cooldown using a timer
    def gun_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.gun_cooldown:
                self.can_shoot = True 

        
    # Sets up the game by loading the map.  Then for each layer in the map, loop through each object
    # in that layer, and create a sprite for each object.
    def setup(self):
        tmx_path = get_asset_path("data", "maps", "world.tmx")
        map = load_pygame(tmx_path)
        
        # Store the possible home spawning positions
        home_spawn_positions = []
        
        # Creating sprites for each ground tile.
        for x, y, image in map.get_layer_by_name('Ground').tiles():
            GroundSprite((x * TILE_SIZE,y * TILE_SIZE), image, self.all_sprites)
        
        # Creating the visible object sprites, such as the trees and rocks. 
        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

        # Contains all the invisible rectangles on the border of the map to prevent player from going off the map
        # thus this is only added to the collision_sprites, not to all_sprites (otherwise it would not be invisible)
        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

        # Load health packs from the Health layer
        for obj in map.get_layer_by_name('Health'):
            HealthPack((obj.x, obj.y), obj.image, (self.all_sprites, self.health_pack_sprites))

        #Loop through each object in the entities layer. If the entity is player, then create the player
        # sprite at the specified position. Create laser shooter sprite next to the player. 
        # It also collects all the spawn positions for home in a list. 
        # Otherwise, the remaining entites are all enemy spawn points, so add them to a list
        # of enemy spawn locations. 
        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x,obj.y), self.all_sprites, self.collision_sprites)
                self.gun = Gun(self.player, self.all_sprites)
            elif obj.name == 'Home':  
                home_spawn_positions.append((obj.x, obj.y))
            else:
                self.spawn_positions.append((obj.x, obj.y))
        # Randomly chooses one home spawn position and render the home image there
        if home_spawn_positions:
            home_pos = choice(home_spawn_positions)
            Home(home_pos, (self.all_sprites, self.home_sprite))
    
    # Checks if bullets and enemies are colliding. If so, call the destory method on the enemy sprite 
    # that was hit, and remove the bullet from the game.
    # Also, if the bullet collides with a tree, rock, or any other static sprite, it is also killed 
    # this is to simulate the tree, rock, etc blocking the bullet's path.
    def bullet_collision(self):
        if self.bullet_sprites:
            for bullet in self.bullet_sprites:
                collision_sprites = pygame.sprite.spritecollide(bullet, self.enemy_sprites, False, pygame.sprite.collide_mask)
                if collision_sprites:
                    for sprite in collision_sprites:
                        sprite.destroy()
                        if sprite.death_time > 0:  # Enemy actually died
                            self.enemies_killed += 1
                            self.check_wave_complete()
                    bullet.kill()
                # Check collision with obstacles (trees, rocks, borders)
                elif pygame.sprite.spritecollide(bullet, self.collision_sprites, False):
                    bullet.kill()
    def check_wave_complete(self):
        if self.enemies_killed >= self.enemies_per_wave:
            self.wave_number += 1
            self.enemies_killed = 0
            self.enemies_per_wave += ENEMIES_INCREMENT_PER_WAVE # More enemies each wave
            # Spawn enemies faster
            new_interval = max(MIN_SPAWN_INTERVAL, INITIAL_SPAWN_INTERVAL - (self.wave_number * SPAWN_INTERVAL_DECREASE))
            pygame.time.set_timer(self.enemy_event, new_interval)
    
    # Function that handles collisions between player and enemy.
    def player_collision(self):
        current_time = pygame.time.get_ticks()

        # Check if player is colliding with any enemy and start tracking the start time for collision
        colliding_enemies = pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask)
        if colliding_enemies:
            if not self.player.is_colliding:
                self.player.is_colliding = True
                self.player.collision_start_time = current_time
            
            # if collision lasted long enough, player will take damage
            if self.player.is_colliding and self.player.can_take_damage:
                collision_duration = current_time - self.player.collision_start_time
                if collision_duration >= self.player.collision_damage_delay:
                    # Get the first colliding enemy and use its damage value
                    enemy = colliding_enemies[0]
                    self.player.take_damage(enemy.damage)
                    self.player.collision_start_time = current_time
                    
                    if self.player.health <= 0:
                        self.running = False
         # if player isn't colliding with enemy anymore, reset the timer as well
        else:
            self.player.is_colliding = False
            self.player.collision_start_time = 0
        

    # Function that handles player collision with the home sprite. If collides, set the game state to won and end the game.
    def home_collision(self):
        if self.home_sprite.sprite: 
            if self.player.rect.colliderect(self.home_sprite.sprite.rect):
                self.game_won = True
                self.running = False  

    # Function that handles player collision with health packs. If player's health isn't at max health and player collids with
    # health pack, increment 1 to the player's current health and remove the colliding health pack from game.
    def health_pack_collision(self):
        collided_health_packs = pygame.sprite.spritecollide(self.player, self.health_pack_sprites, False)
        for health_pack in collided_health_packs:
            if self.player.health < self.player.max_health:
                self.player.health += 1
                health_pack.kill() 

    # Function that manages player invinsibility. Only after the damage cooldown time from the last time the player took damage 
    # can the player take damage again.
    def damage_timer(self):
        self.player.update_damage_timer()

    # Render the player's health as long as player isn't at 0 health. 
    def draw_ui(self):
        if self.player.health > 0:
            heart_bar = self.heart_images[self.player.health]
            x = 10
            y = WINDOW_HEIGHT - heart_bar.get_height() - 10
            self.display_surface.blit(heart_bar, (x, y))
            
            #Also display the wave number
            self.display_surface.blit(self.wave_text_font.render(f"Wave: {self.wave_number}", True, (255, 255, 255)), (10, 10))
    # Game loop that runs the game. 
    def run(self):
        start_screen = StartScreen(self.display_surface, self.clock)
        action = start_screen.show()
        
        # If user quit from start screen, exit
        if action != ScreenAction.START_GAME:
            pygame.quit()
            return
        
        while self.running:
            dt = self.clock.tick() / 1000
        # If user clicks the button that closes the window, quit the game. 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Generate an enemy at one of the spawn positions 
                if event.type == self.enemy_event:
                        enemy_type = choice(['normal', 'fast', 'tank'])  # More normals than special
                        Enemy(choice(self.spawn_positions), choice(list(self.enemy_frames.values())), 
                            (self.all_sprites, self.enemy_sprites), self.player, self.collision_sprites, enemy_type)
            # update game states
            self.gun_timer()
            self.damage_timer() 
            self.input()
            self.all_sprites.update(dt)
            self.bullet_collision()
            self.player_collision()
            self.home_collision()
            self.health_pack_collision()

            # draw
            self.display_surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            self.draw_ui()
            pygame.display.update()
        
        # If game_won is true, display the won screen. Otherwise, show the game over screen
        # Also check if player wants to play again, and start a new game if so.
        if self.game_won:
            win_screen = WinScreen(self.display_surface, self.clock)
            play_again = win_screen.show()
        else:
            game_over_screen = GameOverScreen(self.display_surface, self.clock)
            play_again = game_over_screen.show()

        if play_again:
            self.reset_game()
            self.run()
        else:
            pygame.quit()
    
    # Function that resets the game variables for a new game.
    def reset_game(self):
        self.all_sprites.empty()
        self.collision_sprites.empty()
        self.bullet_sprites.empty()
        self.enemy_sprites.empty()
        self.home_sprite.empty()
        self.health_pack_sprites.empty()

        self.game_won = False
        self.running = True
        
        self.can_shoot = True
        self.shoot_time = 0

        # Reset wave system
        self.wave_number = 1
        self.enemies_killed = 0
        self.enemies_per_wave = INITIAL_ENEMIES_PER_WAVE
        # Reset enemy spawn timer to initial 2 seconds
        pygame.time.set_timer(self.enemy_event, INITIAL_SPAWN_INTERVAL)

        self.spawn_positions = []
        
        self.setup()


if __name__ == '__main__':
    game = Game()
    game.run() 