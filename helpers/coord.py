import numpy as np
from typing import Optional

# Coordinate transforms
def to_polar(xyz: np.ArrayLike, prev_xyz: Optional[np.array], resolution: Optional[int]) -> np.array:
    """
    xyz: [x, y, z],
    Assumes no B, so B may be set to zero by default and allow planar
    """
    r = np.sqrt(xyz[0]**2, xyz[1]**2)
    theta = np.atan2(xyz[1], xyz[0])
    z = xyz[3]

    return np.array([r, theta, z])

def segment(a: np.ArrayLike, b: np.ArrayLike, resolution: int=10):
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


def to_xyz(crt: np.ArrayLike, b_len: int) -> np.array:
    """
    ctzb = [x, z, c, b]
    """
    c = np.deg2rad(crt[2])
    b = np.deg2rad(crt[3])
    x = crt[0]
    z = crt[1]
    return np.array[
        (x-(b_len*np.cos(b)))*np.cos(c), 
        (x-b_len*np.cos(b))*np.sin(c), 
        z+np.sin(b)
    ]

def get_dist(a: np.ArrayLike, b: np.ArrayLike) -> int:
    return np.sqrt(
        (b[0]- a[0])**2,
        (b[1]- a[1])**2,
        (b[2]- a[2])**2
    )