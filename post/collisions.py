'''
Detects and z-hops over collision
'''
import numpy as np

def detect_collisions(df, slice_height = 2):
    vectors = df.xyz[1:] - df.xyz[:-1]
    z_max = 0

    for i in range (len(df.xyz) - 1):
        curr_row = df.xyz.iloc[i]
        next_row = df.xyz.iloc[i+1]
        if curr_row['Z'] < z_max:
            ray = next_row - curr_row
            bounding_slice = vectors[(vectors['Z'] >= i - slice_height) & (vectors['Z'] <= i + slice_height)]

            for sl in bounding_slice:
                res = np.linalg.norm(np.cross(ray, bounding_slice))
                if res == 0:
                    print("Collision")
        else:
            z_max = curr_row['Z']