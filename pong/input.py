import pygame
from .constants import PLAYER_SPEED

# -----------------------------------------------------------------------------
# Human input handlers for player paddles
# Each function returns a vertical velocity based on key presses.
# -----------------------------------------------------------------------------

def p1_controls(game):
    """
    Player 1 control mapping:
      - Z key or Down Arrow: move paddle down
      - A key or Up Arrow:   move paddle up
    Returns:
      int: vertical speed (positive = down, negative = up)
    """
    keys = pygame.key.get_pressed()

    # Check for downward movement input
    if keys[pygame.K_z] or keys[pygame.K_DOWN]:
        return PLAYER_SPEED

    # Check for upward movement input
    if keys[pygame.K_a] or keys[pygame.K_UP]:
        return -PLAYER_SPEED

    # No movement
    return 0


def p2_controls(game):
    """
    Player 2 control mapping:
      - M key: move paddle down
      - K key: move paddle up
    Returns:
      int: vertical speed (positive = down, negative = up)
    """
    keys = pygame.key.get_pressed()

    # Check for downward movement input
    if keys[pygame.K_m]:
        return PLAYER_SPEED

    # Check for upward movement input
    if keys[pygame.K_k]:
        return -PLAYER_SPEED

    # No movement
    return 0
