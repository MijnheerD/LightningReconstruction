import numpy as np


def unit_vector(vector):
    """
    Returns the unit vector of the vector.
    """
    return vector / np.linalg.norm(vector)


def angle_between(v1, v2):
    """
    Calculate the angle between 2 n-dimensional vectors.
    :param v1: First vector.
    :param v2: Second vector, must have some dimension as the first one.
    :return: The angle between the two in radians.
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
