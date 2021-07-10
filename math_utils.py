import numpy as np

def pol2cart(phi, r=1):
    return r * np.array([np.cos(phi), np.sin(phi)])


def perp(p):
    return np.array([-p[1], p[0]])

def mp(x, y):
    return np.array([x, y])