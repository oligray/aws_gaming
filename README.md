# Rainbow Islands - Retro Platform Game

A Python/Pygame-CE recreation inspired by the classic Rainbow Islands arcade game.

## Features

- **Classic Platform Gameplay**: Jump between platforms and avoid enemies
- **Rainbow Mechanics**: Shoot rainbows that create temporary bridges
- **Enemy AI**: Patrolling enemies with collision detection
- **Retro Graphics**: Simple, colorful pixel-art style graphics
- **Score System**: Earn points by defeating enemies
- **Level Progression**: Complete levels by defeating all enemies

## Installation

1. Make sure you have Python 3.6+ installed
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Play

### Controls
- **Arrow Keys** or **WASD**: Move left/right and jump
- **X** or **Left Ctrl**: Shoot rainbow
- **R**: Restart game (when game over)

### Gameplay
1. Navigate through the level using platforms
2. Avoid red enemies that patrol back and forth
3. Shoot rainbows with X or Left Ctrl to:
   - Defeat enemies (earn 100 points each)
   - Create temporary rainbow bridges to reach higher platforms
4. Defeat all enemies to complete the level
5. Don't fall off the bottom of the screen!

### Rainbow Mechanics
- Rainbows arc through the air when shot
- After completing their arc, they become solid bridges
- Rainbow bridges last for about 5 seconds
- Use them strategically to reach higher platforms and escape enemies

## Running the Game

```bash
python rainbow_islands_game.py
```

## Game Elements

- **Blue Character**: The player (you!)
- **Green Platforms**: Static platforms you can jump on
- **Red Enemies**: Avoid these or defeat them with rainbows
- **Rainbow Bridges**: Temporary platforms created by your rainbow shots
- **Colorful Rainbows**: Your projectiles that defeat enemies and create bridges

## Tips

- Time your rainbow shots carefully - they have a cooldown
- Use rainbow bridges to escape from enemies
- Plan your route through the level using both static platforms and rainbow bridges
- Remember that rainbow bridges are temporary - don't get stuck on one!

## Technical Details

- Built with Python and Pygame-CE
- 60 FPS gameplay
- 800x600 resolution
- Object-oriented design with separate classes for Player, Enemies, Platforms, and Rainbows

Enjoy this retro platforming adventure!
