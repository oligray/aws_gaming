# Rainbow Islands - Retro Platform Game

A Python/Pygame-CE recreation inspired by the classic Rainbow Islands arcade game.

## Features

- **Classic Platform Gameplay**: Jump between platforms and avoid enemies
- **Rainbow Mechanics**: Shoot rainbows that create temporary bridges
- **Enemy AI**: Patrolling enemies with collision detection
- **Death Animations**: Enemies spin up in the air when defeated
- **Fruit Collection**: Defeated enemies become collectible fruit
- **Retro Graphics**: Simple, colorful pixel-art style graphics
- **Score System**: Earn points by defeating enemies and collecting fruit
- **Two Challenging Levels**: Complete both levels to win the game
- **Level Progression**: Advance through increasingly difficult layouts

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
- **R**: Restart game (when game over or after winning)
- **SPACE**: Advance to next level (when level complete)

### Gameplay
1. Navigate through the level using platforms
2. Avoid red enemies that patrol back and forth
3. Shoot rainbows with X or Left Ctrl to:
   - Defeat enemies (earn 100 points each)
   - Create temporary rainbow bridges to reach higher platforms
4. When enemies are defeated, they spin up in the air and become fruit
5. Collect the fruit for bonus points (20 points each)
6. Defeat all enemies and collect all fruit to complete the level
7. Complete both levels to win the game!
8. Don't fall off the bottom of the screen!

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

- **Orange Character**: The player (you!)
- **Red Platforms**: Static platforms you can jump on
- **Blue Enemies**: Avoid these or defeat them with rainbows
- **Spinning Enemies**: Death animation when enemies are defeated
- **Colorful Fruit**: Collectible items that appear after defeating enemies
- **Rainbow Bridges**: Temporary platforms created by your rainbow shots
- **Colorful Rainbows**: Your projectiles that defeat enemies and create bridges

## Levels

### Level 1: Learning the Ropes
- **Larger platforms** for easier navigation
- **6 enemies** to defeat
- **Simpler layout** to learn the game mechanics

### Level 2: The Challenge
- **Smaller, scattered platforms** requiring more precision
- **15 enemies** across multiple tiers
- **Complex vertical layout** requiring strategic use of rainbow bridges
- **Tighter jumps** and more challenging enemy placement

## Scoring

- **Defeating Enemies**: 100 points each
- **Collecting Fruit**: 20 points each
- **Strategy**: Defeat all enemies and collect all fruit for maximum score!
- **Score carries over** between levels

## Tips

- Time your rainbow shots carefully - they have a cooldown
- Use rainbow bridges to escape from enemies
- Plan your route through the level using both static platforms and rainbow bridges
- Remember that rainbow bridges are temporary - don't get stuck on one!
- Collect all the fruit that appears after defeating enemies for bonus points
- Level 2 requires more strategic use of rainbow bridges due to smaller platforms

## Technical Details

- Built with Python and Pygame-CE
- 60 FPS gameplay
- 800x600 resolution
- Object-oriented design with separate classes for Player, Enemies, Platforms, Rainbows, and Collectibles
- Two distinct levels with different layouts and enemy configurations

## Level Progression

1. **Complete Level 1**: Defeat all 6 enemies and collect all fruit
2. **Press SPACE**: Advance to Level 2 when "LEVEL COMPLETE!" appears
3. **Complete Level 2**: Defeat all 15 enemies and collect all fruit
4. **Press SPACE**: Complete the game when "LEVEL COMPLETE!" appears
5. **Congratulations**: You've beaten Rainbow Islands!

Enjoy this retro platforming adventure!
