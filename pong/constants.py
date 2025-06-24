# -----------------------------------------------------------------------------
# pong/constants.py
#
# Configuration constants for screen size, speeds, colors, and game timing.
# -----------------------------------------------------------------------------

# --- Screen dimensions --------------------------------------------------------
# Pixel width and height of the game window
WIDTH = 800
HEIGHT = 480
# Precomputed half-values for centering objects
HALF_W = WIDTH // 2
HALF_H = HEIGHT // 2

# --- Movement speeds ----------------------------------------------------------
# Speed at which a human-controlled paddle moves (pixels per frame)
PLAYER_SPEED = 6
# Maximum speed for the AI-controlled paddle (pixels per frame)
MAX_AI_SPEED = 6

# --- Color definitions --------------------------------------------------------
# RGB color tuples for easy reference in rendering
WHITE = (255, 255, 255)  # Default text and ball color
GREEN = (30, 128, 30)  # Background court color
YELLOW = (240, 240, 50)  # Highlight color (e.g., prompts)
RED = (240, 50, 50)  # Alert/flash color (e.g., losing paddle)
BLUE = (50, 50, 240)  # Secondary highlight (e.g., opponent scored)
BLACK = (0, 0, 0)  # Background for menus and overlays

# --- Timing -------------------------------------------------------------------
# Frames per second cap to control game speed and CPU usage
FPS = 60
