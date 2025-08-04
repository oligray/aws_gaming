#!/usr/bin/env python3
"""
Simple script to create an example player sprite image.
You can replace this with your own custom artwork.
"""

import pygame
import sys

# Initialize Pygame
pygame.init()

# Create a 32x32 surface for the player sprite
sprite_size = (32, 32)
sprite_surface = pygame.Surface(sprite_size, pygame.SRCALPHA)

# Colors
ORANGE = (255, 165, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_ORANGE = (200, 120, 0)
LIGHT_ORANGE = (255, 200, 100)

# Draw a simple character sprite
# Body (rounded rectangle)
pygame.draw.rect(sprite_surface, ORANGE, (4, 8, 24, 24), border_radius=4)

# Head (circle)
pygame.draw.circle(sprite_surface, LIGHT_ORANGE, (16, 8), 8)

# Eyes
pygame.draw.circle(sprite_surface, WHITE, (13, 6), 2)
pygame.draw.circle(sprite_surface, WHITE, (19, 6), 2)
pygame.draw.circle(sprite_surface, BLACK, (14, 6), 1)
pygame.draw.circle(sprite_surface, BLACK, (20, 6), 1)

# Mouth (small smile)
pygame.draw.arc(sprite_surface, BLACK, (14, 8, 4, 3), 0, 3.14, 1)

# Arms
pygame.draw.circle(sprite_surface, ORANGE, (8, 16), 3)
pygame.draw.circle(sprite_surface, ORANGE, (24, 16), 3)

# Legs
pygame.draw.rect(sprite_surface, DARK_ORANGE, (12, 28, 3, 4))
pygame.draw.rect(sprite_surface, DARK_ORANGE, (17, 28, 3, 4))

# Add some shading/highlights
pygame.draw.circle(sprite_surface, LIGHT_ORANGE, (13, 5), 1)  # Eye highlight
pygame.draw.circle(sprite_surface, LIGHT_ORANGE, (19, 5), 1)  # Eye highlight

# Save the sprite
pygame.image.save(sprite_surface, 'player.png')
print("Player sprite created as 'player.png'")
print("You can now run the game and it will use this image!")
print("Feel free to replace player.png with your own custom artwork.")

pygame.quit()
