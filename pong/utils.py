import math


# -----------------------------------------------------------------------------
# Utility functions for simple vector math and helpers
# -----------------------------------------------------------------------------

def normalised(x, y):
    """
    Convert a 2D vector (x, y) into a unit-length vector.

    This preserves the direction of (x, y) but scales it to length 1.
    If the input vector has zero length, returns (0, 0) to avoid division by zero.

    Args:
        x (float): Horizontal component of the vector.
        y (float): Vertical component of the vector.

    Returns:
        (float, float): A tuple representing the normalized (unit) vector.
    """
    # Compute the vector magnitude using the hypotenuse function
    length = math.hypot(x, y)

    # If the vector is zero-length, return a zero vector to avoid division by zero
    if length == 0:
        return 0, 0

    # Scale each component by the length to obtain a unit vector
    return x / length, y / length
