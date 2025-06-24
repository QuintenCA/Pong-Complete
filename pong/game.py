import random
import pygame
from .constants import *
from .entities import Ball, Bat, Impact

class Game:
    """
    Core game class: manages bats, ball, impacts, scoring, and drawing.
    """
    def __init__(self, controls=(None, None), sfx=None):
        # Input functions for each player (or None for AI)
        self.controls  = controls
        # Dictionary of sound-effect lists
        self.sfx       = sfx or {}
        # Create two paddles (left = player 0, right = player 1)
        self.bats      = [Bat(0, controls[0]), Bat(1, controls[1])]
        # Initialize ball moving left
        self.ball      = Ball(-1)
        # List of active Impact effects
        self.impacts   = []
        # Random offset applied to AI target for variety
        self.ai_offset = 0

    def update(self):
        """
        Advance game state: update paddles, ball, impacts, and handle scoring.
        """
        # Move each paddle
        for bat in self.bats:
            bat.update(self)
        # Move the ball, detect collisions
        self.ball.update(self)
        # Update all ripple effects
        for imp in self.impacts:
            imp.update()
        # Remove finished ripples (older than 10 frames)
        self.impacts = [imp for imp in self.impacts if imp.time < 10]

        # Check for scoring: ball out of left or right bounds
        if self.ball.out():
            # Determine which player scored
            scorer = 1 if self.ball.x < HALF_W else 0
            loser  = 1 - scorer

            # Only award point if loser isn't in hit-flash state
            if self.bats[loser].timer < 0:
                # Increment scorer's tally
                self.bats[scorer].score += 1
                # Play goal celebration sound
                self.play_sound("score_goal", 1)
                # Flash loser paddle to indicate score
                self.bats[loser].timer = 20
            # Once flash ends, respawn ball toward the losing side
            elif self.bats[loser].timer == 0:
                direction = -1 if loser == 0 else 1
                self.ball = Ball(direction)

    def draw(self, surf):
        """
        Render the entire game frame: background, center line, impacts, paddles, ball, scores.
        """
        # Fill background with green
        surf.fill(GREEN)
        # Draw dotted center line
        for y in range(0, HEIGHT, 20):
            pygame.draw.line(surf, WHITE, (HALF_W, y), (HALF_W, y + 10), 4)

        # Draw all active ripple effects behind paddles and ball
        for imp in self.impacts:
            imp.draw(surf)

        # Draw paddles (bats)
        for bat in self.bats:
            bat.draw(surf, self)
        # Draw the ball on top
        self.ball.draw(surf)

        # Render players' scores
        font = pygame.font.SysFont("Consolas", 48, bold=True)
        for p, bat in enumerate(self.bats):
            colour = WHITE
            other = 1 - p
            # If opponent just scored (ball out and flash state), color accordingly
            if self.bats[other].timer > 0 and self.ball.out():
                colour = RED if p == 0 else BLUE
            score_surf = font.render(f"{bat.score:02d}", True, colour)
            # Position scores near top center, offset for each player
            surf.blit(score_surf, (255 + 160*p, 20))

    def play_sound(self, name, count=1):
        """
        Play a random variant of the requested sound effect, once or multiple times.

        Only plays if player controls are initialized (suppress sounds in menu).
        """
        # Ensure we have sounds loaded and game is in active play
        if self.controls[0] is not None and name in self.sfx:
            # Pick a random sound from the variants
            sound = random.choice(self.sfx[name])
            if sound:
                sound.play()  # Trigger playback
