from settings import * 
from math import atan2, degrees
from utils import get_asset_path

# Sets up sprite with an image and position,
#  marks it as a ground layer sprite for rendering order
class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.ground = True

# Sprite class for objects that block movement (trees, rocks, map borders)
# These sprites have collision detection but could be invisible
class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)

#  laser gun sprite, follows player and rotates to point at the mouse cursor
 # Positioned at a fixed distance from the player in the direction of the mouse
class Gun(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        # player connection 
        self.player = player 
        self.distance = 140
        self.player_direction = pygame.Vector2(0,1)

        # sprite setup 
        super().__init__(groups)

        lasergun_original = pygame.image.load(get_asset_path('images', 'gun', 'lasergun.png')).convert_alpha()
        # Scale down the image of laser gun
        lasergun_size = 150  
        self.gun_surf = pygame.transform.scale(lasergun_original, (lasergun_size, lasergun_size))

        self.image = self.gun_surf
        self.rect = self.image.get_rect(center = self.player.rect.center + self.player_direction * self.distance)
    
    # Calculate the direction from player to the mouse cursor
    # Uses screen center as player position since the camera follows the player
    def get_direction(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        player_pos = pygame.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.player_direction = (mouse_pos - player_pos).normalize()

    # rotate gun image to point in the direction of the mouse cursor.
    # flips gun vertically when pointing left
    def rotate_gun(self):
        angle = degrees(atan2(self.player_direction.x, self.player_direction.y)) - 90
        if self.player_direction.x > 0:
            self.image = pygame.transform.rotozoom(self.gun_surf, angle, 1)
        else:
            self.image = pygame.transform.rotozoom(self.gun_surf, abs(angle), 1)
            self.image = pygame.transform.flip(self.image, False, True)
    
    # update the position and rotation of gun (for every frame)
    def update(self, _):
        self.get_direction()
        self.rotate_gun()
        self.rect.center = self.player.rect.center + self.player_direction * self.distance
# bullet is fired by the player's gun. Travels in a straight line and
# automatically kills itself after 1 sec
class Bullet(pygame.sprite.Sprite):
    def __init__(self, surf, pos, direction, groups):
        super().__init__(groups)
        self.image = surf 
        self.rect = self.image.get_rect(center = pos)
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 1000

        self.direction = direction 
        self.speed = 1200 
    
    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt

        if pygame.time.get_ticks() - self.spawn_time >= self.lifetime:
            self.kill()

# Enemy sprite. chase the player
 # while avoiding collision with obstacles.
class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, player, collision_sprites, enemy_type='normal'):
        super().__init__(groups)
        self.player = player
        self.enemy_type = enemy_type

        # image 
        self.frames, self.frame_index = frames, 0 
        self.image = self.frames[self.frame_index]
        self.animation_speed = 6

        # rect 
        self.rect = self.image.get_rect(center = pos)
        self.hitbox_rect = self.rect.inflate(-90,-90)
        self.collision_sprites = collision_sprites
        self.direction = pygame.Vector2()

        # There are three different enemy types, they move with different speed and can do different amounts of damage on player.
        if enemy_type == 'fast':
            self.speed = 350  
            self.health = 1
            self.damage = 1  # Fast enemies deal 1 damage
        elif enemy_type == 'tank':
            self.speed = 100 
            self.health = 1
            self.damage = 2  # Tank enemies deal 2 damage (more punishing)
        else:  # normal
            self.speed = 200
            self.health = 1
            self.damage = 1

        # timer 
        self.death_time = 0
        self.death_duration = 400
    
    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]

    # Calculate direction toward player and move the enemy, handling collisions with obstacles.
    # Checks for zero-length vector to prevent errors when enemy is on top of player.
    
    def move(self, dt):
        # get direction 
        player_pos = pygame.Vector2(self.player.rect.center)
        enemy_pos = pygame.Vector2(self.rect.center)
        direction_vector = player_pos - enemy_pos
        if direction_vector.length() > 0:  # ADD THIS CHECK
            self.direction = direction_vector.normalize()
        else:
            self.direction = pygame.Vector2(0, 0)  # Stay still if on top of player
        
        # update the rect position + collision
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center

    # Handle enemy collision with obstacles by preventing overlap
    # Adjusts hitbox position based on collision direction (horizontal or vertical)
    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top

    def destroy(self):
        self.health -= 1
        if self.health <= 0:
            self.death_time = pygame.time.get_ticks()
            surf = pygame.mask.from_surface(self.frames[0]).to_surface()
            surf.set_colorkey('black')
            self.image = surf
    
    # Remove the enemy sprite after the death animation duration has elapsed.
    def death_timer(self):
        if pygame.time.get_ticks() - self.death_time >= self.death_duration:
            self.kill()
   
   # Update enemy behavior each frame. If alive, move and animate. If dead, run death timer.
    def update(self, dt):
        if self.death_time == 0:
            self.move(dt)
            self.animate(dt)
        else:
            self.death_timer()
    
 #  home sprite. Loads and scales the home image to appropriate size.
class Home(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        home_original = pygame.image.load(get_asset_path('images', 'home', 'home.png')).convert_alpha()
        
        home_size = (384, 384)  
        self.image = pygame.transform.scale(home_original, home_size)
        self.rect = self.image.get_rect(center=pos)

 # Health sprite that restores one heart to the player when collected.
    # Placed throughout the map for players to find and use.
class HealthPack(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)