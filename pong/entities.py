import pygame, random
from .constants import *
from .utils import normalised


class Impact:
    """
    A visual effect representing the ripple when the ball hits a wall or paddle.
    """

    def __init__(self, pos):
        # Start position of the impact effect
        self.x, self.y = pos
        # Timer to control the growth and fading of the ripple
        self.time = 0

    def update(self):
        # Increment the timer each frame
        self.time += 1

    def draw(self, surf):
        # Radius grows over time, alpha fades out
        radius = int(2 + self.time * 1.5)
        alpha = max(0, 255 - self.time * 25)
        # Create a transparent surface for the ripple
        tmp = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        # Draw a fading circle outline
        pygame.draw.circle(tmp, (255, 255, 255, alpha), (radius, radius), radius, width=3)
        # Blit the ripple at the correct position
        surf.blit(tmp, (self.x - radius, self.y - radius))


class Ball:
    """
    Handles ball movement, collisions with paddles and walls, speed changes, and spawning impacts.
    """

    def __init__(self, dx):
        # Start ball in the center, moving horizontally with initial dx
        self.x, self.y = HALF_W, HALF_H
        self.dx, self.dy = dx, 0
        # Base speed (number of sub-steps per frame)
        self.speed = 5

    def update(self, game):
        # Move the ball in small sub-steps for accurate collision detection
        for _ in range(self.speed):
            prev_x = self.x
            self.x += self.dx
            self.y += self.dy

            # Check for paddle collision when crossing paddle zone
            if abs(self.x - HALF_W) >= 344 and abs(prev_x - HALF_W) < 344:
                # Determine which side (left or right) hit occurred
                side = 0 if self.x < HALF_W else 1
                bat = game.bats[side]
                diff_y = self.y - bat.y  # Vertical offset from bat center
                # Only bounce if within bat height
                if -64 < diff_y < 64:
                    # Reverse horizontal direction
                    self.dx = -self.dx
                    # Adjust vertical speed based on hit location
                    self.dy += diff_y / 128
                    # Clamp dy to prevent excessive angles
                    self.dy = max(-1, min(1, self.dy))
                    # Normalize dx,dy to keep consistent speed
                    self.dx, self.dy = normalised(self.dx, self.dy)

                    # Create a ripple effect just off the paddle
                    game.impacts.append(Impact((self.x - self.dx * 10, self.y)))
                    # Gradually increase speed for challenge
                    self.speed += 1
                    # Randomize AI targeting for the next serve
                    game.ai_offset = random.randint(-10, 10)
                    # Flash the paddle to show a hit occurred
                    bat.timer = 10

                    # Play a 'hit' sound and a speed-based variant
                    game.play_sound("hit", 5)
                    if self.speed <= 10:
                        game.play_sound("hit_slow", 1)
                    elif self.speed <= 12:
                        game.play_sound("hit_medium", 1)
                    elif self.speed <= 16:
                        game.play_sound("hit_fast", 1)
                    else:
                        game.play_sound("hit_veryfast", 1)

            # Check for wall collision (top/bottom bounds)
            if abs(self.y - HALF_H) > 220:
                # Reverse vertical direction and move out of wall
                self.dy = -self.dy
                self.y += self.dy
                # Spawn a ripple at the wall hit location
                game.impacts.append(Impact((self.x, self.y)))
                # Play bounce sounds
                game.play_sound("bounce", 5)
                game.play_sound("bounce_synth", 1)

    def out(self):
        """Return True if the ball has gone off the left or right edge."""
        return self.x < 0 or self.x > WIDTH

    def draw(self, surf):
        # Draw the ball as a simple filled circle
        pygame.draw.circle(surf, WHITE, (int(self.x), int(self.y)), 7)


class Bat:
    """
    Represents a player's paddle; can be human-controlled or AI-driven.
    """

    def __init__(self, player, move_func=None):
        self.player = player
        # Position paddle on left (0) or right (1)
        self.x = 40 if player == 0 else WIDTH - 40
        self.y = HALF_H
        # Movement function: either human input or built-in AI
        self.move_func = move_func or self.ai
        self.score = 0  # Player score
        self.timer = 0  # Flash timer after a hit or score

    def update(self, game):
        # Countdown the hit-flash timer
        self.timer -= 1
        # Calculate vertical movement this frame
        dy = self.move_func(game)
        # Clamp paddle position to stay on-screen
        self.y = max(80, min(400, self.y + dy))

    def draw(self, surf, game):
        # Flash RED if opponent has scored; YELLOW if just hit
        if self.timer > 0:
            color = RED if game.ball.out() else YELLOW
        else:
            color = WHITE
        # Create and draw the paddle rectangle
        rect = pygame.Rect(0, 0, 18, 128)
        rect.center = (self.x, self.y)
        pygame.draw.rect(surf, color, rect, border_radius=4)

    def ai(self, game):
        """
        Simple AI: blends between center and ball Y based on horizontal distance.
        """
        # How far is the ball horizontally from this paddle?
        xdist = abs(game.ball.x - self.x)
        # Two target points: center line and ball Y (+ offset)
        t1 = HALF_H
        t2 = game.ball.y + game.ai_offset
        # Weight toward center when far away, toward ball when near
        w1 = min(1, xdist / HALF_W)
        target = w1 * t1 + (1 - w1) * t2
        # Move at most MAX_AI_SPEED toward the target
        delta = target - self.y
        return max(-MAX_AI_SPEED, min(MAX_AI_SPEED, delta))
