from settings import * 
from utils import get_asset_path

class Player(pygame.sprite.Sprite):
    # Initialize the player with frames, position, movement capabilities,
    # and collision detection. Sets up the player's hitbox smaller than the sprite
 
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.load_images()
        self.state, self.frame_index = 'right', 0
        self.image = self.frames['down'][0]
        self.rect = self.image.get_rect(center = pos)
        self.hitbox_rect = self.rect.inflate(-60, -90)
    
        # movement 
        self.direction = pygame.Vector2()
        self.speed = 500
        self.collision_sprites = collision_sprites

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

                    scale_factor = 0.2  
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
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top
    
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