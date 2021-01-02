from PIL import Image
import os
from noise import pnoise1, pnoise2, pnoise3
from math import floor, ceil, sin, sqrt
import random

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

cwd = os.getcwd()
shape = (160, 160)
ani_len = 100
scale = 100

speed = .05

octaves = 6
persistence = .5
lacunarity= 3

seed = random.randint(1, 100)

stretch_v = 0.4

repeatx, repeaty = 16, 16
repeatz = 10

def transform_coord(i, j, z, at_z):
    return i /scale - at_z - z, j/scale - at_z

def perlin_array(z, at_z = 0, shape = shape,
			scale = scale,octaves = octaves,
                        persistence = persistence,
                        lacunarity= lacunarity,
			seed = seed):

    if not seed:

        seed = np.random.randint(0, 100)
        print("seed was {}".format(seed))

    arr = np.zeros(shape)
    
    for i in range(shape[0]):
        for j in range(shape[1]):
            x, y = transform_coord(i, j, z, at_z)
            K = pnoise3(x,
                                        y / stretch_v,
                                        z ,
                                        octaves=octaves,
                                        persistence=persistence,
                                        lacunarity=lacunarity,
                                        repeatx=repeatx,
                                        repeaty=repeaty,
                                        repeatz = repeatz,
                                        base=seed)

            #K = 4*pow(K, 2) + 4*K + 1

            
            
            arr[i][j] = K * i**2
    max_arr = np.max(arr)
    min_arr = np.min(arr)

    norm_me = lambda x: (x-min_arr)/(max_arr - min_arr)
    
    arr = norm_me(arr)
    
##    norm_me = lambda x: 1 - sqrt(x)
##    

    
    return arr

fig2 = plt.figure()

x = np.arange(shape[0])
y = np.arange(shape[1]).reshape(-1, 1)

frames = []

at_z = random.randint(-shape[0], 0)
for t in np.arange(0, ani_len):
    z = at_z + speed*t
    base = perlin_array(z, at_z)
    
    frames.append((plt.pcolor(x, y, base, shading='auto',cmap='hot', vmin = 0, vmax = 1),))

im_ani = animation.ArtistAnimation(fig2, frames, interval=45, repeat = True,
                                   blit=False)

plt.show()
