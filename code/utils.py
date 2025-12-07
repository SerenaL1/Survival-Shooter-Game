import os
import pygame

# Get absolute path to asset files relative to the project root. Usage: get_asset_path('images', 'player', 'down', '0.png')
def get_asset_path(*path_parts):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, '..', *path_parts)
    return os.path.normpath(full_path)

# Handle collision between a moving rectangle and static collision sprites
# This function is used by both Player and Enemy to avoid code duplication
def handle_collision(moving_rect, collision_sprites, direction, direction_vector):
    for sprite in collision_sprites:
        if sprite.rect.colliderect(moving_rect):
            if direction == 'horizontal':
                if direction_vector.x > 0:
                    moving_rect.right = sprite.rect.left
                if direction_vector.x < 0:
                    moving_rect.left = sprite.rect.right
            else:
                if direction_vector.y < 0:
                    moving_rect.top = sprite.rect.bottom
                if direction_vector.y > 0:
                    moving_rect.bottom = sprite.rect.top
