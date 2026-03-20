'''
Detects collisions and replaces with fast moves
'''

import numpy as np

def dist(A, P):
    return np.sqrt(np.sum((P-A)**2, axis=1))

def fix_collisions(df):
    for i in range(len(df)):
        P = df[i]