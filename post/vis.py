import numpy as np
from numpy.typing import ArrayLike
import matplotlib.pyplot as plt
from helpers.gcode import read_file

def vis_toolpaths(coords: ArrayLike):
    fig = plt.figure(figsize=(0, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(-60, 60)
    ax.set_ylim(-60, 60)
    ax.set_zlim(-60, 60)

    ax.set_box_aspect([
        120, 120, 120
    ])

    ax.set_xlabel('X')
    ax.set_xlabel('Y')
    ax.set_xlabel('Z')

    ax.plot(
            coords[:, 0], 
            coords[:, 1], 
            coords[:, 2], 
            color='blue', 
            linewidth=0.8, 
            alpha=0.8,
            label='Toolpath'
        )

    plt.title("S4_Slicer Toolpath Visualization")
    plt.show()
