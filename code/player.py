from settings import * 
from utils import get_asset_path, handle_collision

class Player(pygame.sprite.Sprite):
    # Initialize the player with frames, position, movement capabilities,
    # and collision detection. Sets up the player's hitbox smaller than the sprite
 
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.load_images()
        self.state, self.frame_index = 'right', 0
        self.image = self.frames['down'][0]
        self.rect = self.image.get_rect(center = pos)
        self.hitbox_rect = self.rect.inflate(PLAYER_HITBOX_INFLATE)
    
        # movement 
        self.direction = pygame.Vector2()
        self.speed = PLAYER_SPEED
        self.collision_sprites = collision_sprites

         # health system, with 0.5 second invincibility to the player right after damage is taken
        self.max_health = PLAYER_MAX_HEALTH
        self.health = self.max_health
        self.can_take_damage = True
        self.damage_cooldown = PLAYER_DAMAGE_COOLDOWN
        self.damage_time = 0
        
        # Collision tracking of player with enemy. Only after colliding for 1 second or more can the
        # player take damage.
        self.collision_start_time = 0
        self.is_colliding = False
        self.collision_damage_delay = PLAYER_COLLISION_DAMAGE_DELAY

    # Load all player animation frames from the folders for each direction (left, right, up, down).
    # Then stores the images in dictionary
    def load_images(self):
        self.frames = {'left': [], 'right': [], 'up': [], 'down': []}

        for state in self.frames.keys():
            state_path = get_asset_path('images', 'player1', state)

            for folder_path, sub_folders, file_names in walk(state_path):
                if not file_names:
                    continue

                frame_files = [
                    name for name in file_names
                    if name.lower().endswith('.png') and name.split('.')[0].isdigit()
                ]

                for file_name in sorted(frame_files, key=lambda name: int(name.split('.')[0])):
                    full_path = join(folder_path, file_name)
                    surf = pygame.image.load(full_path).convert_alpha()

                    scale_factor = PLAYER_SCALE_FACTOR
                    new_width = int(surf.get_width() * scale_factor)
                    new_height = int(surf.get_height() * scale_factor)
                    surf = pygame.transform.scale(surf, (new_width, new_height))
                    
                    self.frames[state].append(surf)

                   
    # Read keyboard input (arrow keys or WASD) and set the player's movement direction
    # Normalizes diagonal movement so speed is consistent in all directions
    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction

     # Move player based on direction and speed, handling collisions separately for horizontal
    # and vertical movement to prevent getting stuck on corners.
    def move(self, dt):
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center

    # Handle collisions with obstacles by adjusting the player's hitbox position to prevent overlap.
    # Checks collision direction (horizontal or vertical) and adjusts position accordingly.
    def collision(self, direction):
        handle_collision(self.hitbox_rect, self.collision_sprites, direction, self.direction)
    
     # Update the player's appearance based on movement direction. Changes state (left/right/up/down)
    # and cycles through animation frames. Resets to frame 0 when stationary.

    def animate(self, dt):
        # get state 
        if self.direction.x != 0:
            self.state = 'right' if self.direction.x > 0 else 'left'
        if self.direction.y != 0:
            self.state = 'down' if self.direction.y > 0 else 'up'

        # animate
        self.frame_index = self.frame_index + 5 * dt if self.direction else 0
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]
    
    #  update loop, called every frame. Processes input, moves the player, updates animation / visual appearance
    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)
    # Deal damage to player if not in invincibility frames. Returns True if damage was dealt.
    def take_damage(self, amount):
        if self.can_take_damage:
            self.health -= amount
            self.can_take_damage = False
            self.damage_time = pygame.time.get_ticks()
            return True
        return False
    # Update invincibility timer
    def update_damage_timer(self):
        if not self.can_take_damage:
            if pygame.time.get_ticks() - self.damage_time >= self.damage_cooldown:
                self.can_take_damage = True
    #  Reset health to max (for new game)
    def reset_health(self):
        self.health = self.max_health
        self.can_take_damage = True
        self.damage_time = 0
        self.collision_start_time = 0
        self.is_colliding = False