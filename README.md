# Project README

Project Video:
[https://youtu.be/LF20n24ZtN8]

Overview:

Help Susie Get Home is a survival shooter game built with Python and Pygame. The player controls Susie, who is spawned in a forest with quickly approaching monsters. The player’s objective is to navigate through the forest and reach the home, while avoiding taking on too much damage. The game has the following main components:

Enemies come in waves, with each wave being more difficult than the previous. Therefore, it’s in the player’s best interest to find the home as fast as possible.
Some enemies move faster than others, and some deal more damage.
There are health packs scattered around the forest, which the player can pick up to regain health.
The player can shoot at enemies by left clicking the mouse. However, the player must properly aim the gun in the enemy’s direction in order to kill the enemy.
The player can only see a small chunk of the map at a time, so where the home is located is not immediately obvious.

Part 1: Installation:

Python:

On Windows:
Press Windows Key + R
Type cmd and press Enter
In the black window that appears, type: python --version
Press Enter

On macOS:
Press Command + Space to open Spotlight
Type terminal and press Enter
In the terminal window, type: python3 --version
Press Enter

On Linux:
Open Terminal (usually Ctrl + Alt + T)
Type: python3 --version
Press Enter

If you see an error or a Python version lower than 3.7, continue below to install Python.

Windows:
Go to [https://www.python.org/downloads/]
Click the big yellow button that says "Download Python 3.x.x"
Run the downloaded installer (.exe file)
IMPORTANT: Check the box that says "Add Python to PATH" at the bottom of the installer
Click "Install Now"
Wait for installation to complete
Click "Close"
Verify installation by opening Command Prompt and typing: python --version

macOS:
Go to [https://www.python.org/downloads/]
Click "Download Python 3.x.x"
Open the downloaded .pkg file
Follow the installation wizard (click Continue, Agree, Install)
Enter your Mac password when prompted
Wait for installation to complete
Verify by opening Terminal and typing: python3 --version

Linux (Ubuntu/Debian):
Open Terminal
Update package list: sudo apt update
Install Python: sudo apt install python3 python3-pip
Enter your password when prompted
Verify: python3 --version

Pip:

Pip is installed with Python, but you can run the following to check:

Windows: python -m pip --version
macOS/Linux: python3 -m pip --version

If pip is installed: pip 24.0 from ... (version number may vary)
If you get an error, retry installing Python.

Part 2: Download the Project from Github and Open in VS Code
Go to [https://github.com/SerenaL1/Survival-Shooter-Game]
Look for the green button that says "Code" (near the top right)
Click the "Code" button, and click "Download ZIP"
Your browser will download a file called Survival-Shooter-Game-main.zip
Extract/Unzip the file
You should now have a folder called Survival-Shooter-Game-main

Next, open the folder in VS Code

Part 3: Install Game Dependencies:
This step, you will install pygame and pytmx, which are the libraries the game needs to run.
Open the terminal window in your VS code window that has your opened project folder, and run:
Windows: pip install pygame pytmx
macOS/Linux: pip3 install pygame pytmx

If You Get Permission Errors, try adding --user:
pip install --user pygame pytmx
or
pip3 install --user pygame pytmx

Part 4: Verify Everything is Correcrtly Installed
Check pygame:
Windows:
python -c "import pygame; print('pygame version:', pygame.ver)"
macOS/Linux:
python3 -c "import pygame; print('pygame version:', pygame.ver)"

You should expect to see an output indicating the version of pygame.

Check pytmx:
Windows: python -c "import pytmx; print('pytmx imported successfully')"
macOS/Linux: python3 -c "import pytmx; print('pytmx imported successfully')"
Expected Output: pytmx imported successfully

Run the Game:

Step 1 - Open the project folder in VS Code
Step 2 - Open main.py
Step 3 - Click the triangle button on the top right of the screen
Alternatively, go into the code folder in the project and execute the python script. This can be done by:
cd code
python main.py    (or python3 main.py, depending on the version)

Playing the Game:
A window titled "Help Susie Get Home" will appear. The start screen will display with game instructions and rules. You can click the "PLAY" button to begin the game. Once the game starts, the player is generated in the middle of the map.
The player can move around following these game controls on the keyboard:

For movement, player can press arrow keys or WASD: ↑ / W - Move up; ↓ / S - Move down; ← / A - Move left; → / D - Move right. Diagonal movement: Press two keys simultaneously (e.g., W+D to move up-right)

For combat, player can do the following: Left Mouse Button (Click and Hold) is to shoot laser. The gun automatically aims toward your mouse cursor. Bullets disappear after 1 second or upon hitting an obstacle/enemy. If the gun isn't properly aimed at the enemy when the left mouse button is clicked, the bullet won't be able to hit the enemy. If the gun was instead aimed at a static sprite like a tree or a rock, the bullet would reach that static sprite and disappear.

Window Controls: X Button (Top Right) closes the game. After a win or loss, on the winning or losing screen, a Play Again Button is available, which the user can click on to restart the game. There is also a quit button on the win or lose game screen, which the player can click on to exit.

The Map/Environment: There are trees and rocks scattered in the forest, which blocks certain paths. The map also has boundaries, or invisible walls at the edges preventing you from leaving the playable area. There are health packs scattered around the map that restore 1 heart when collected, but they only work if you're below max health (5 hearts). They disappear after being picked up.

Game objective and rules: There is a house sprite that appears in one of four random locations. The player must reach the house in order to win. The player starts with 5 hearts, and can lose hearts when enemy sprites collide with the player. The player can combat the enemies to kill them before they reach the player, but trees and rocks could block the shots. Enemies spawn at numerous pre-defined spawn points around the map, and this spawn rate increases as the player spends more time in game.

Enemy types: The player can encounter three different types of enemies. The normal enemies have medium speed and deal 1 damage. The tank enemies are slower but deal 2 heart damages. The fast enemies move faster, but only deal 1 heart damage. Enemies could also be blocked by trees or rocks, but they mostly try to move to where the player is at. The enemy must touch you for 1 full second before dealing damage. After taking damage, you're invincible for 0.5 seconds

Wave System: Enemies come in waves. The current wave number is shown at top-left of screen. After killing 10 enemies, you advance to the next wave. In each subsequent wave, the number of enemies increase by 5, and the enemies spawn faster each wave.
After winning: Click play again to start a new game, quit to exit the game.
After losing: the game ends, and you can play again or quit.

Dependencies:

Required Python Packages

pygame
Version Used in Development: 2.6.1
Minimum Version: 2.0.0 or higher
Purpose: Game engine, graphics, input handling, sound
Installation: pip install pygame
Documentation: [https://www.pygame.org/docs/]
To check your version: pip show pygame

pytmx
Version Used in Development: 3.32
Minimum Version: 3.0.0 or higher recommended
Purpose: Loading and parsing Tiled TMX map files
Installation: pip install pytmx
Documentation: [https://pytmx.readthedocs.io/]
To check your version: pip show pytmx

Python Standard Library
os: File path operations
math: Trigonometric calculations for gun rotation
random: Enemy type selection, home spawn randomization
enum: Screen action enumeration

Version Compatibility
Developed and Tested on: Python 3.12 with pygame 2.6.1
Minimum Python Version: Python 3.7
Operating Systems: Windows 10/11, macOS 10.14+, Linux (Ubuntu 20.04+)
