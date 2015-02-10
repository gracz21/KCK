__author__ = 'inf109714'

import matplotlib.pyplot as plt
from matplotlib import colors as col
import numpy as np


def load_file():
    data = np.loadtxt(fname='big.dem', skiprows=1)
    return data

def create_custom_cmap():
    cdict = {'red':   [(0.0,  0.0, 0.0),
                       (0.5,  1.0, 1.0),
                       (1.0,  1.0, 1.0)],

             'green': [(0.0,  1.0, 1.0),
                       (0.5, 1.0, 1.0),
                       (1.0,  0.0, 0.0)],

             'blue':  [(0.0,  0.0, 0.0),
                       (0.5,  0.0, 0.0),
                       (1.0,  0.0, 0.0)]}
    my_cmap = col.LinearSegmentedColormap('my_colormap', cdict, 1024)
    return my_cmap

def main():
    data = load_file()
    fig, ax = plt.subplots()
    ax.set_xticks([0, 100, 200, 300, 400])
    ax.set_yticks([400, 300, 200, 100, 0])
    ls = col.LightSource(azdeg=190, altdeg=3, hsv_min_val=0.8, hsv_min_sat=0.9, hsv_max_val=1, hsv_max_sat=0.34)
    rgb = ls.shade(data, create_custom_cmap())
    ax.imshow(rgb)
    fig.savefig('map.pdf')


if __name__ == '__main__':
    main()