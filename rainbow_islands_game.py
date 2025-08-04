import pygame
import sys
import math
import random
from enum import Enum

# Initialize Pygame-CE
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
PINK = (255, 192, 203)
GREY = (120, 120, 120)

# Rainbow colors for the rainbow bridges
RAINBOW_COLORS = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE]

class GameState(Enum):
    PLAYING = 1
    GAME_OVER = 2
    LEVEL_COMPLETE = 3
    WIN = 4

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.jump_power = -8
        self.gravity = 0.5
        self.on_ground = False
        self.facing_right = True
        self.rainbow_cooldown = 0
        
    def update(self, platforms, rainbows):
        # Handle input
        keys = pygame.key.get_pressed()
        self.vel_x = 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -self.speed
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = self.speed
            self.facing_right = True
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False
            
        # Update rainbow cooldown
        if self.rainbow_cooldown > 0:
            self.rainbow_cooldown -= 1
            
        # Apply gravity
        self.vel_y += self.gravity
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Check platform collisions
        self.on_ground = False
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # First check if player is currently on a rainbow
        on_rainbow = False
        for rainbow in rainbows:
            if rainbow.solid and not rainbow.dissolving:
                player_center_x = self.x + self.width // 2
                if rainbow.x <= player_center_x <= rainbow.x + rainbow.bridge_width:
                    # Calculate if player is actually on this rainbow surface
                    x_progress = (player_center_x - rainbow.x) / rainbow.bridge_width
                    arc_height = 20
                    arc_y_offset = arc_height * math.sin(x_progress * math.pi)
                    rainbow_top_y = rainbow.y - arc_y_offset
                    
                    # Check if player is close to the rainbow surface
                    if abs(self.y + self.height - rainbow_top_y) < 10:
                        on_rainbow = True
                        break
        
        # Only apply platform collisions if NOT on a rainbow
        if not on_rainbow:
            for platform in platforms:
                platform_rect = pygame.Rect(platform.x, platform.y, platform.width, platform.height)
                if player_rect.colliderect(platform_rect):
                    # Landing on top of platform
                    if self.vel_y > 0 and self.y < platform.y:
                        self.y = platform.y - self.height
                        self.vel_y = 0
                        self.on_ground = True
                    # Side collisions
                    elif self.vel_x > 0:  # Moving right
                        self.x = platform.x - self.width
                    elif self.vel_x < 0:  # Moving left
                        self.x = platform.x + platform.width
                    
        # Check rainbow collisions (rainbows act as platforms)
        jumped_on_rainbow = None
        
        for rainbow in rainbows:
            if rainbow.solid and not rainbow.dissolving:
                player_center_x = self.x + self.width // 2
                
                # Check if player is horizontally within the rainbow bridge
                if rainbow.x <= player_center_x <= rainbow.x + rainbow.bridge_width:
                    # Calculate the arc height at the player's position
                    x_progress = (player_center_x - rainbow.x) / rainbow.bridge_width
                    arc_height = 20
                    arc_y_offset = arc_height * math.sin(x_progress * math.pi)
                    rainbow_top_y = rainbow.y - arc_y_offset
                    
                    # Create collision rect for the rainbow at this position
                    rainbow_rect = pygame.Rect(player_center_x - 10, rainbow_top_y, 20, rainbow.bridge_height)
                    player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
                    
                    # Check for collision with the rainbow
                    if player_rect.colliderect(rainbow_rect):
                        # Only dissolve on high-velocity landing (jumping onto rainbow)
                        if self.vel_y > 5 and self.y < rainbow_top_y:
                            jumped_on_rainbow = rainbow
                        
                        # Handle collision based on direction
                        if self.vel_y > 0 and self.y < rainbow_top_y:
                            # Landing on top - normal platform behavior
                            self.y = rainbow_top_y - self.height
                            self.vel_y = 0
                            self.on_ground = True
                        elif self.vel_y < 0 and self.y > rainbow_top_y + rainbow.bridge_height:
                            # Hitting from below - dissolve rainbow
                            jumped_on_rainbow = rainbow
                            self.y = rainbow_top_y + rainbow.bridge_height + 2
                            self.vel_y = 2  # Small downward velocity
                        elif self.vel_x > 0:
                            # Hitting from left side
                            self.x = rainbow.x - self.width
                            self.vel_x = 0
                        elif self.vel_x < 0:
                            # Hitting from right side  
                            self.x = rainbow.x + rainbow.bridge_width
                            self.vel_x = 0
                        
                        break  # Only collide with one rainbow at a time
        
        # Keep player on screen
        if self.x < 0:
            self.x = 0
        elif self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width
            
        # Check if player fell off screen
        if self.y > SCREEN_HEIGHT:
            return False
            
        # Return the rainbow that was jumped on, or True if no special event
        return jumped_on_rainbow if jumped_on_rainbow else True
    
    def shoot_rainbow(self):
        offset = 34
        if self.rainbow_cooldown <= 0:
            self.rainbow_cooldown = 30  # Cooldown frames
            direction = 1 if self.facing_right else -1
            # Spawn rainbow right next to character
            if self.facing_right:
                spawn_x = self.x + self.width + offset  # Right edge of character
            else:
                spawn_x = self.x - offset  # Left edge of character
            spawn_y = self.y + self.height - 2
            return Rainbow(spawn_x, spawn_y, direction)
        return None
    
    def draw(self, screen):
        # Draw player as a simple colored rectangle
        color = ORANGE #if self.facing_right else CYAN
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
        # Draw eyes
        eye_size = 4
        if self.facing_right:
            pygame.draw.circle(screen, WHITE, (int(self.x + 20), int(self.y + 10)), eye_size)
            pygame.draw.circle(screen, BLACK, (int(self.x + 22), int(self.y + 10)), 2)
        else:
            pygame.draw.circle(screen, WHITE, (int(self.x + 12), int(self.y + 10)), eye_size)
            pygame.draw.circle(screen, BLACK, (int(self.x + 10), int(self.y + 10)), 2)

class Platform:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    def draw(self, screen):
        # Draw brick pattern
        brick_width = 32
        brick_height = 16
        
        # Fill background with base red brick color
        pygame.draw.rect(screen, (139, 35, 35), (self.x, self.y, self.width, self.height))  # Dark red base
        
        # Draw individual bricks
        for row in range(0, self.height, brick_height):
            for col in range(0, self.width, brick_width):
                # Offset every other row for brick pattern
                offset = (brick_width // 2) if (row // brick_height) % 2 == 1 else 0
                brick_x = self.x + col + offset
                brick_y = self.y + row
                
                # Only draw brick if it fits within the platform
                if brick_x < self.x + self.width and brick_y < self.y + self.height:
                    # Calculate actual brick dimensions (may be clipped)
                    actual_width = min(brick_width, self.x + self.width - brick_x)
                    actual_height = min(brick_height, self.y + self.height - brick_y)
                    
                    if actual_width > 0 and actual_height > 0:
                        # Draw brick with gradient effect
                        # Red brick color
                        pygame.draw.rect(screen, (178, 34, 34), (brick_x, brick_y, actual_width, actual_height))
                        
                        # Highlight on top and left (3D effect)
                        pygame.draw.line(screen, (220, 80, 80), (brick_x, brick_y), (brick_x + actual_width - 1, brick_y), 2)
                        pygame.draw.line(screen, (220, 80, 80), (brick_x, brick_y), (brick_x, brick_y + actual_height - 1), 2)
                        
                        # Shadow on bottom and right (3D effect)
                        pygame.draw.line(screen, (100, 20, 20), (brick_x, brick_y + actual_height - 1), (brick_x + actual_width - 1, brick_y + actual_height - 1), 2)
                        pygame.draw.line(screen, (100, 20, 20), (brick_x + actual_width - 1, brick_y), (brick_x + actual_width - 1, brick_y + actual_height - 1), 2)
                        
                        # Dark outline for each brick
                        pygame.draw.rect(screen, (80, 15, 15), (brick_x, brick_y, actual_width, actual_height), 1)
        
        # Draw overall platform border
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height), 2)

class WinnersCup:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 24
        self.height = 32
        self.collected = False
        self.bob_offset = 0  # For floating animation
        
    def update(self):
        # Gentle bobbing animation
        self.bob_offset = math.sin(pygame.time.get_ticks() * 0.005) * 3
        
    def draw(self, screen):
        if not self.collected:
            # Draw trophy cup with bobbing animation
            cup_y = self.y + self.bob_offset
            
            # Cup base (dark gold)
            pygame.draw.rect(screen, (184, 134, 11), (self.x + 6, cup_y + 24, 12, 8))
            
            # Cup stem (gold)
            pygame.draw.rect(screen, (255, 215, 0), (self.x + 9, cup_y + 18, 6, 6))
            
            # Cup bowl (bright gold)
            pygame.draw.ellipse(screen, (255, 215, 0), (self.x + 2, cup_y + 8, 20, 12))
            
            # Cup handles (gold)
            pygame.draw.arc(screen, (255, 215, 0), (self.x - 2, cup_y + 10, 8, 8), 0, math.pi, 3)
            pygame.draw.arc(screen, (255, 215, 0), (self.x + 18, cup_y + 10, 8, 8), 0, math.pi, 3)
            
            # Cup top rim (bright gold)
            pygame.draw.ellipse(screen, (255, 223, 0), (self.x + 4, cup_y + 6, 16, 6))
            
            # Sparkle effects
            sparkle_time = pygame.time.get_ticks() * 0.01
            for i in range(3):
                sparkle_x = self.x + 8 + math.sin(sparkle_time + i * 2) * 15
                sparkle_y = cup_y + 10 + math.cos(sparkle_time + i * 1.5) * 10
                pygame.draw.circle(screen, (255, 255, 255), (int(sparkle_x), int(sparkle_y)), 2)

class DeadEnemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.start_y = y
        self.width = 24
        self.height = 24
        self.vel_y = -8  # Initial upward velocity
        self.gravity = 0.4
        self.rotation = 0
        self.rotation_speed = 15  # Degrees per frame
        self.max_height = 40  # Maximum height to rise
        self.landed = False
        
    def update(self):
        if not self.landed:
            # Apply physics
            self.vel_y += self.gravity
            self.y += self.vel_y
            self.rotation += self.rotation_speed
            
            # Check if enemy has landed back on or below original position
            if self.y >= self.start_y:
                self.y = self.start_y
                self.landed = True
                return True  # Signal that animation is complete
        return False
        
    def draw(self, screen):
        if not self.landed:
            # Create a surface for the rotating enemy
            enemy_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.rect(enemy_surf, BLUE, (0, 0, self.width, self.height))
            # Draw simple face
            pygame.draw.circle(enemy_surf, WHITE, (8, 8), 3)
            pygame.draw.circle(enemy_surf, WHITE, (16, 8), 3)
            pygame.draw.circle(enemy_surf, BLACK, (8, 8), 1)
            pygame.draw.circle(enemy_surf, BLACK, (16, 8), 1)
            
            # Rotate the surface
            rotated_surf = pygame.transform.rotate(enemy_surf, self.rotation)
            
            # Get the rect and center it on the enemy position
            rotated_rect = rotated_surf.get_rect(center=(self.x + self.width//2, self.y + self.height//2))
            screen.blit(rotated_surf, rotated_rect)

class Fruit:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 16
        self.height = 16
        self.collected = False
        self.bob_offset = 0
        self.bob_speed = 0.1
        self.color = random.choice([RED, ORANGE, YELLOW, GREEN, PURPLE])  # Random fruit color
        
    def update(self):
        # Gentle bobbing animation
        self.bob_offset = math.sin(pygame.time.get_ticks() * self.bob_speed) * 2
        
    def draw(self, screen):
        if not self.collected:
            fruit_y = self.y + self.bob_offset
            
            # Draw fruit as a circle with highlight
            pygame.draw.circle(screen, self.color, (int(self.x + self.width//2), int(fruit_y + self.height//2)), 8)
            # Add a small white highlight
            pygame.draw.circle(screen, WHITE, (int(self.x + self.width//2 - 2), int(fruit_y + self.height//2 - 2)), 2)

class Enemy:
    def __init__(self, x, y, patrol_start, patrol_end):
        self.x = x
        self.y = y
        self.width = 24
        self.height = 24
        self.speed = 1
        self.direction = 1
        self.patrol_start = patrol_start
        self.patrol_end = patrol_end
        
        # Animation properties
        self.animation_frame = 0
        self.animation_speed = 8  # Frames between animation updates (slower = less frequent updates)
        self.frame_counter = 0
        self.total_frames = 4  # Number of animation frames
        
    def update(self, platforms, rainbows=None):
        # Move enemy
        self.x += self.speed * self.direction
        
        # Update animation
        self.frame_counter += 1
        if self.frame_counter >= self.animation_speed:
            self.frame_counter = 0
            self.animation_frame = (self.animation_frame + 1) % self.total_frames
        
        # Reverse direction at patrol boundaries
        if self.x <= self.patrol_start or self.x >= self.patrol_end - self.width:
            self.direction *= -1
            
        # Check for collisions with solid rainbow bridges (enemies should turn around, not be pushed)
        if rainbows:
            enemy_rect = pygame.Rect(self.x, self.y, self.width, self.height)
            for rainbow in rainbows:
                # Only turn around when touching solid, non-dissolving rainbows
                # Dissolving rainbows should kill the enemy, not affect movement
                if rainbow.solid and not rainbow.dissolving:
                    # Create collision detection for rainbow bridges
                    rainbow_rect = pygame.Rect(rainbow.x, rainbow.y - 20, rainbow.bridge_width, rainbow.bridge_height + 20)
                    
                    if enemy_rect.colliderect(rainbow_rect):
                        # Simply turn around when touching a solid rainbow bridge
                        self.direction *= -1
                        break  # Only handle collision with one rainbow at a time
            
    def draw(self, screen):
        # Create animated sprite by drawing different patterns based on animation frame
        base_color = BLUE
        
        # Main body
        pygame.draw.rect(screen, base_color, (self.x, self.y, self.width, self.height))
        
        # Eyes that look in the direction of movement
        pygame.draw.circle(screen, WHITE, (int(self.x + 6), int(self.y + 8)), 3)
        pygame.draw.circle(screen, WHITE, (int(self.x + 18), int(self.y + 8)), 3)
        
        # Pupils follow movement direction
        if self.direction > 0:  # Moving right
            pygame.draw.circle(screen, BLACK, (int(self.x + 7), int(self.y + 8)), 1)  # Right pupil
            pygame.draw.circle(screen, BLACK, (int(self.x + 19), int(self.y + 8)), 1)  # Right pupil
        else:  # Moving left
            pygame.draw.circle(screen, BLACK, (int(self.x + 5), int(self.y + 8)), 1)  # Left pupil
            pygame.draw.circle(screen, BLACK, (int(self.x + 17), int(self.y + 8)), 1)  # Left pupil
        
        # Animated mouth expressions based on current frame
        if self.animation_frame == 0:
            # Frame 0: Small curved mouth
            pygame.draw.arc(screen, BLACK, (self.x + 8, self.y + 14, 8, 6), 0, math.pi, 2)
            
        elif self.animation_frame == 1:
            # Frame 1: Slightly open mouth
            pygame.draw.ellipse(screen, BLACK, (self.x + 10, self.y + 15, 4, 3))
            
        elif self.animation_frame == 2:
            # Frame 2: Open mouth
            pygame.draw.ellipse(screen, BLACK, (self.x + 9, self.y + 14, 6, 4))
            
        else:  # Frame 3
            # Frame 3: Closed mouth (line)
            pygame.draw.line(screen, BLACK, (self.x + 10, self.y + 16), (self.x + 14, self.y + 16), 2)

class Rainbow:
    def __init__(self, x, y, direction):
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.direction = direction
        self.width = 8
        self.height = 8
        self.speed = 0.8  # Reduced from 8 to limit horizontal travel to 20 pixels
        self.lifetime = 120  # frames
        self.solid = False
        self.solid_timer = 0
        self.arc_progress = 0
        self.max_arc = 25  # With speed=0.8 and increment=2: 0.8 * 25 = 20 pixels
        self.bridge_width = 100
        self.bridge_height = 12  # Height of the rainbow bridge
        self.dissolving = False
        self.dissolve_timer = 0
        self.dissolve_fall_speed = 2  # Pixels per frame to fall during dissolution
        
    def dissolve(self):
        """Start the dissolution process"""
        if self.solid and not self.dissolving:
            self.dissolving = True
            self.dissolve_timer = 0
            return True
        return False
        
    def update(self):
        # Handle dissolution
        if self.dissolving:
            self.dissolve_timer += 1
            # Move rainbow down during dissolution
            self.y += self.dissolve_fall_speed
            if self.dissolve_timer > 120:  # Dissolve over 120 frames (2 seconds at 60 FPS)
                return False
            return True
            
        # Move rainbow in an arc
        self.arc_progress += 2
        if self.arc_progress > self.max_arc:
            if not self.solid:
                # Just became solid - set up bridge dimensions and position
                self.solid = True
                self.width = self.bridge_width
                self.height = self.bridge_height
                # Center the bridge on the final position
                self.x = self.x - (self.bridge_width // 2)
            self.solid_timer += 1
            if self.solid_timer > 300:  # Rainbow bridge lasts 5 seconds
                return False
        else:
            # Calculate arc position
            progress = self.arc_progress / self.max_arc
            self.x = self.start_x + (self.direction * self.speed * self.arc_progress)
            self.y = self.start_y - (50 * math.sin(progress * math.pi))
            
        self.lifetime -= 1
        return self.lifetime > 0 or self.solid
        
    def draw(self, screen):
        if self.solid:
            # Draw as a solid rainbow bridge in an arc shape
            alpha = 255
            if self.dissolving:
                # Fade out during dissolution over 2 seconds (120 frames)
                alpha = max(0, 255 - (self.dissolve_timer * 255 // 120))
            
            # Draw rainbow as an arc (hill shape)
            arc_height = 25  # Height of the arc at the center
            segments = 20  # Number of segments to create smooth arc
            segment_width = self.bridge_width // segments
            
            for segment in range(segments):
                # Calculate arc position for this segment
                x_progress = segment / (segments - 1)  # 0 to 1
                arc_y_offset = arc_height * math.sin(x_progress * math.pi)  # Sine wave for hill shape
                
                segment_x = self.x + (segment * segment_width)
                segment_y = self.y - arc_y_offset  # Subtract to go upward
                
                # Draw each color stripe of the rainbow for this segment
                for i, color in enumerate(RAINBOW_COLORS):
                    stripe_y = segment_y + (i * 2)
                    
                    # Create a surface for alpha blending if dissolving
                    if self.dissolving and alpha < 255:
                        surf = pygame.Surface((segment_width + 1, 2))  # +1 to avoid gaps
                        surf.set_alpha(alpha)
                        surf.fill(color)
                        screen.blit(surf, (segment_x, stripe_y))
                    else:
                        pygame.draw.rect(screen, color, (segment_x, stripe_y, segment_width + 1, 2))
        else:
            # Draw as moving rainbow projectile
            color_index = (pygame.time.get_ticks() // 100) % len(RAINBOW_COLORS)
            pygame.draw.circle(screen, RAINBOW_COLORS[color_index], (int(self.x), int(self.y)), 4)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Rainbow Islands - Retro Platform Game")
        self.clock = pygame.time.Clock()
        self.state = GameState.PLAYING
        
        # Initialize game objects
        self.player = Player(100, 500)
        self.platforms = self.create_level()
        self.enemies = self.create_enemies()
        # self.trophy = self.create_trophy()
        self.rainbows = []
        self.dead_enemies = []  # For death animations
        self.fruits = []  # For collectible fruits
        self.score = 0
        self.level = 1
        
    def create_level(self):
        platforms = []
        
        # Ground level platforms (shorter, scattered)
        platforms.extend([
            Platform(0, 580, 180, 20),      # Left edge
            Platform(320, 580, 160, 20),    # Center
            Platform(620, 580, 180, 20),    # Right edge (extends to screen edge)
        ])
        
        # Mid platforms (medium length, some from edges) - increased gap from 450 to 380
        platforms.extend([
            Platform(0, 380, 220, 20),      # From left edge
            Platform(400, 330, 140, 20),    # Center short
            Platform(580, 280, 220, 20),    # From right edge (extends to screen edge)
            Platform(80, 250, 160, 20),     # Left side
        ])
        
        # Top platform (moved down, removed the two beneath it)
        platforms.extend([
            Platform(0, 120, 800, 20),      # Full screen width platform (moved down from Y=40)
        ])
        
        return platforms
        
    def create_enemies(self):
        enemies = [
            # Ground level enemies (removed enemy from spawn platform and center platform)
            Enemy(650, 556, 620, 800),      # On right ground platform only
            
            # Mid-level enemies (removed enemy from shortest center platform)
            Enemy(100, 356, 0, 220),        # On left-edge platform (Y=380-20-4=356)
            Enemy(650, 256, 580, 800),      # On right-edge platform (Y=280-20-4=256)
            Enemy(120, 226, 80, 240),       # On left-side platform (Y=250-20-4=226)
            
            # Top level enemies (kept all - these are on longer platforms)
            Enemy(200, 96, 0, 350),         # On very long left platform (Y=120-20-4=96)
            Enemy(600, 96, 450, 800),       # On very long right platform (Y=100-20-4=76)
        ]
        return enemies
        
    def create_trophy(self):
        trophy = WinnersCup(650, 20)
        #trophy.draw()
        return trophy

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x or event.key == pygame.K_LCTRL:
                    # Shoot rainbow
                    rainbow = self.player.shoot_rainbow()
                    if rainbow:
                        self.rainbows.append(rainbow)
                elif event.key == pygame.K_r and self.state == GameState.GAME_OVER:
                    # Restart game
                    self.__init__()
                    
        return True
        
    def update(self):
        if self.state == GameState.PLAYING:
            # Update player
            jumped_rainbow = self.player.update(self.platforms, self.rainbows)
            if jumped_rainbow is False:  # Player died
                self.state = GameState.GAME_OVER
            elif jumped_rainbow is not True:  # Player jumped on a rainbow (returned Rainbow object)
                # Dissolve the rainbow (monster killing will happen during fall)
                jumped_rainbow.dissolve()
                
            # Check rainbow projectile-enemy collisions FIRST (before rainbows can become solid)
            rainbows_to_remove = []
            for rainbow in self.rainbows:
                if not rainbow.solid:  # Only projectile rainbows can kill enemies
                    # Create a collision rect for the rainbow projectile (matches the 4-pixel radius circle)
                    rainbow_rect = pygame.Rect(rainbow.x - 4, rainbow.y - 4, 8, 8)
                    hit_enemy = False
                    for enemy in self.enemies[:]:  # Use slice to avoid modification during iteration
                        enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
                        if rainbow_rect.colliderect(enemy_rect):
                            # Create death animation
                            dead_enemy = DeadEnemy(enemy.x, enemy.y)
                            self.dead_enemies.append(dead_enemy)
                            # Remove enemy from active enemies
                            self.enemies.remove(enemy)
                            self.score += 100
                            print(f"Rainbow projectile killed enemy! Score: {self.score}")  # Debug message
                            rainbows_to_remove.append(rainbow)
                            hit_enemy = True
                            break  # Rainbow can only hit one enemy
                                
            # Remove rainbows that hit enemies
            for rainbow in rainbows_to_remove:
                if rainbow in self.rainbows:
                    self.rainbows.remove(rainbow)
                
            # Update rainbows AFTER projectile collision check (so dissolving rainbows start falling)
            self.rainbows = [rainbow for rainbow in self.rainbows if rainbow.update()]
            
            # Check falling rainbow-enemy collisions BEFORE enemy movement (so enemies get killed instead of pushed)
            enemies_to_remove = []  # Track enemies to remove to avoid modification during iteration
            for rainbow in self.rainbows:
                if rainbow.dissolving:
                    # Create collision rect for the falling rainbow
                    rainbow_rect = pygame.Rect(rainbow.x, rainbow.y, rainbow.bridge_width, rainbow.bridge_height)
                    for enemy in self.enemies:
                        if enemy not in enemies_to_remove:  # Don't check enemies already marked for removal
                            enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
                            if rainbow_rect.colliderect(enemy_rect):
                                # Create death animation
                                dead_enemy = DeadEnemy(enemy.x, enemy.y)
                                self.dead_enemies.append(dead_enemy)
                                # Mark enemy for removal
                                enemies_to_remove.append(enemy)
                                self.score += 100
                                print(f"Falling rainbow killed enemy! Score: {self.score}")  # Debug message
                                
            # Remove all enemies that were killed by falling rainbows
            for enemy in enemies_to_remove:
                if enemy in self.enemies:
                    self.enemies.remove(enemy)
                
            # Update enemies AFTER falling rainbow collision check
            for enemy in self.enemies:
                enemy.update(self.platforms, self.rainbows)
                
            # Check for falling rainbow collisions (chain reaction)
            newly_triggered = []  # Track rainbows that were just triggered this frame
            for i, rainbow1 in enumerate(self.rainbows):
                if rainbow1.dissolving and rainbow1.dissolve_timer > 1:  # Only after first frame of dissolution
                    rainbow1_rect = pygame.Rect(rainbow1.x, rainbow1.y, rainbow1.bridge_width, rainbow1.bridge_height)
                    for j, rainbow2 in enumerate(self.rainbows):
                        if (i != j and rainbow2.solid and not rainbow2.dissolving and 
                            rainbow2 not in newly_triggered):  # Different rainbow that's solid, not falling, and not already triggered this frame
                            
                            # More precise collision detection - check if rainbows actually overlap
                            rainbow2_rect = pygame.Rect(rainbow2.x, rainbow2.y, rainbow2.bridge_width, rainbow2.bridge_height)
                            
                            # Check for actual overlap (not just touching edges)
                            if (rainbow1_rect.colliderect(rainbow2_rect) and 
                                abs(rainbow1.y - rainbow2.y) < rainbow1.bridge_height):  # Vertical overlap check
                                
                                # Trigger chain reaction - make the second rainbow start falling
                                if rainbow2.dissolve():  # Only trigger if dissolve() returns True (wasn't already dissolving)
                                    newly_triggered.append(rainbow2)
                                    print(f"Chain reaction! Falling rainbow triggered another rainbow to fall!")  # Debug message
            
            # Check falling rainbow-enemy collisions (when rainbows are dissolving)
            enemies_to_remove = []  # Track enemies to remove to avoid modification during iteration
            for rainbow in self.rainbows:
                if rainbow.dissolving:
                    # Create collision rect for the falling rainbow
                    rainbow_rect = pygame.Rect(rainbow.x, rainbow.y, rainbow.bridge_width, rainbow.bridge_height)
                    for enemy in self.enemies:
                        if enemy not in enemies_to_remove:  # Don't check enemies already marked for removal
                            enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
                            if rainbow_rect.colliderect(enemy_rect):
                                # Create death animation
                                dead_enemy = DeadEnemy(enemy.x, enemy.y)
                                self.dead_enemies.append(dead_enemy)
                                # Mark enemy for removal
                                enemies_to_remove.append(enemy)
                                self.score += 100
                                print(f"Falling rainbow killed enemy! Score: {self.score}")  # Debug message
                                
            # Remove all enemies that were killed by falling rainbows
            for enemy in enemies_to_remove:
                if enemy in self.enemies:
                    self.enemies.remove(enemy)
                                
            # Check player-enemy collisions
            player_rect = pygame.Rect(self.player.x, self.player.y, self.player.width, self.player.height)
            for enemy in self.enemies:
                enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
                if player_rect.colliderect(enemy_rect):
                    self.state = GameState.GAME_OVER
                    
            # Update dead enemies and create fruits when they land
            dead_enemies_to_remove = []
            for dead_enemy in self.dead_enemies:
                if dead_enemy.update():  # Returns True when animation is complete
                    # Create fruit at the dead enemy's position
                    fruit = Fruit(dead_enemy.x + 4, dead_enemy.y + 4)  # Center fruit on enemy position
                    self.fruits.append(fruit)
                    dead_enemies_to_remove.append(dead_enemy)
                    
            # Remove completed death animations
            for dead_enemy in dead_enemies_to_remove:
                self.dead_enemies.remove(dead_enemy)
                
            # Update fruits
            for fruit in self.fruits:
                fruit.update()
                
            # Check player-fruit collisions
            for fruit in self.fruits[:]:  # Use slice to avoid modification during iteration
                if not fruit.collected:
                    fruit_rect = pygame.Rect(fruit.x, fruit.y, fruit.width, fruit.height)
                    if player_rect.colliderect(fruit_rect):
                        fruit.collected = True
                        self.fruits.remove(fruit)
                        self.score += 20
                        print(f"Collected fruit! Score: {self.score}")  # Debug message
                                
            # Check if level is complete - all enemies defeated AND all fruit collected
            if len(self.enemies) == 0 and len(self.dead_enemies) == 0 and len(self.fruits) == 0:
                self.state = GameState.LEVEL_COMPLETE
                
    def draw(self):
        self.screen.fill((134, 206, 250))  # Light blue background #86CEFA
        
        # Draw platforms
        for platform in self.platforms:
            platform.draw(self.screen)
            
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen)
            
        # Draw dead enemies (death animations)
        for dead_enemy in self.dead_enemies:
            dead_enemy.draw(self.screen)
            
        # Draw fruits
        for fruit in self.fruits:
            fruit.draw(self.screen)
            
        # Draw rainbows
        for rainbow in self.rainbows:
            rainbow.draw(self.screen)
            
        # Draw player
        self.player.draw(self.screen)
        
        # Draw UI
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))
        
        level_text = font.render(f"Level: {self.level}", True, BLACK)
        self.screen.blit(level_text, (10, 50))
        
        # Draw instructions
        font_small = pygame.font.Font(None, 24)
        instructions = [
            "Arrow Keys / WASD: Move and Jump",
            "X / Left Ctrl: Shoot Rainbow",
            "Defeat enemies to create fruit (20 points each)!",
            "Create rainbow bridges to reach higher platforms!"
        ]
        for i, instruction in enumerate(instructions):
            text = font_small.render(instruction, True, GREY)
            self.screen.blit(text, (400, SCREEN_HEIGHT - 200 + i * 25))
        
        if self.state == GameState.GAME_OVER:
            # Draw game over screen
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            font_large = pygame.font.Font(None, 72)
            game_over_text = font_large.render("GAME OVER", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(game_over_text, text_rect)
            
            restart_text = font.render("Press R to Restart", True, WHITE)
            text_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            self.screen.blit(restart_text, text_rect)
            
        elif self.state == GameState.LEVEL_COMPLETE:
            # Draw level complete screen
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            font_large = pygame.font.Font(None, 72)
            complete_text = font_large.render("LEVEL COMPLETE!", True, GREEN)
            text_rect = complete_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(complete_text, text_rect)
            
            score_text = font.render(f"Final Score: {self.score}", True, WHITE)
            text_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            self.screen.blit(score_text, text_rect)
        
        pygame.display.flip()
        
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
