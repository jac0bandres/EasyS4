import numpy as np
from numpy.typing import ArrayLike
from typing import Optional

# Coordinate transforms
def to_polar_xyplane(x, y) -> ArrayLike:
    r = np.sqrt(x**2, x[1]**2)
    theta = np.atan2(y, x)
    return r, theta

def segment(a: ArrayLike, b: ArrayLike, resolution: int=10):
    """
    Arc length segmentation to account for rotating bed
    """
    dist = get_dist(a, b)
    coords = []
    if dist > resolution:
        num_steps = int(dist / resolution)
        # linearly interpolate xyz
        x_steps = np.linspace(b[0], a[0], num_steps)
        y_steps = np.linspace(b[1], a[1], num_steps)
        z_steps = np.linspace(b[2], a[2], num_steps)

        for i in range (1, len(x_steps)):
            coords.append(x_steps[i], y_steps[i], z_steps[i])
    else:
        coords.append(a) 

    return np.array(coords)

def to_xyz(x, z, b, c, b_len: int):
    if c is None or b is None:
        raise TypeError('np.deg2rad will fail on NoneType, DF may not be processed')

    c = np.deg2rad(c)
    b = np.deg2rad(b)
    return np.array[
        (x-(b_len*np.cos(b)))*np.cos(c), 
        (x-(b_len*np.cos(b)))*np.sin(c), 
        z+np.sin(b)
    ]

def get_dist(a: ArrayLike, b: ArrayLike) -> int:
    return np.sqrt(
        (b[0]- a[0])**2,
        (b[1]- a[1])**2,
        (b[2]- a[2])**2
    )