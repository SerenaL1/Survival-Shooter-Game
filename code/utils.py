import os

# Get absolute path to asset files relative to the project root. Usage: get_asset_path('images', 'player', 'down', '0.png')
def get_asset_path(*path_parts):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, '..', *path_parts)
    return os.path.normpath(full_path)
