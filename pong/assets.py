import pygame
from pathlib import Path

# -----------------------------------------------------------------------------
# pong/assets.py
#
# Loads all sound effects into a structured dictionary for easy playback.
# -----------------------------------------------------------------------------

def load_sfx():
    """
    Initialize the mixer and load all sound effects into a dict:
      - "hit" and "bounce" have multiple variants (hit0.ogg through hit4.ogg)
      - Other effects attempt name0.ogg, then fall back to name.ogg

    Returns:
        dict: mapping effect names to lists of pygame.Sound objects
    Raises:
        FileNotFoundError: if neither name0.ogg nor name.ogg is found for a given effect
    """
    # Ensure the mixer is ready before loading sounds
    pygame.mixer.init()
    sfx = {}

    # Determine the directory containing the 'sounds' folder
    project_root = Path(__file__).resolve().parent.parent
    sounds_dir   = project_root / "sounds"

    # --- Multi-variant effects ---
    # Load a list of sounds for "hit" and "bounce" (5 variants each)
    sfx["hit"]    = [pygame.mixer.Sound(str(sounds_dir / f"hit{i}.ogg"))    for i in range(5)]
    sfx["bounce"] = [pygame.mixer.Sound(str(sounds_dir / f"bounce{i}.ogg")) for i in range(5)]

    # --- Single-variant effects ---
    for name in (
        "hit_slow", "hit_medium", "hit_fast", "hit_veryfast",
        "bounce_synth", "score_goal", "up", "down"
    ):
        # Prefer files with a "0" suffix, else fallback to base name
        p0 = sounds_dir / f"{name}0.ogg"
        p1 = sounds_dir / f"{name}.ogg"

        if p0.exists():
            path = p0
        elif p1.exists():
            path = p1
        else:
            # Missing asset is a critical error; fail fast
            raise FileNotFoundError(
                f"Could not find sound file for '{name}' (tried '{p0.name}' and '{p1.name}')"
            )

        # Store as a single-element list for consistency with multi-variant effects
        sfx[name] = [pygame.mixer.Sound(str(path))]

    return sfx
