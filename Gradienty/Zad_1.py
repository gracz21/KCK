#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division             # Division in Python 2.7
import matplotlib
matplotlib.use('Agg')                       # So that we can render files without GUI
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import math

from matplotlib import colors

def plot_color_gradients(gradients, names):
    # For pretty latex fonts (commented out, because it does not work on some machines)
    rc('text', usetex=True)
    rc('font', family='serif', serif=['Times'], size=10)
    rc('legend', fontsize=10)

    column_width_pt = 400         # Show in latex using \the\linewidth
    pt_per_inch = 72
    size = column_width_pt / pt_per_inch

    fig, axes = plt.subplots(nrows=len(gradients), sharex=True, figsize=(size, 0.75 * size))
    fig.subplots_adjust(top=1.00, bottom=0.05, left=0.25, right=0.95)


    for ax, gradient, name in zip(axes, gradients, names):
        # Create image with two lines and draw gradient on it
        img = np.zeros((2, 1024, 3))
        for i, v in enumerate(np.linspace(0, 1, 1024)):
            img[:, i] = gradient(v)

        im = ax.imshow(img, aspect='auto')
        im.set_extent([0, 1, 0, 1])
        ax.yaxis.set_visible(False)

        pos = list(ax.get_position().bounds)
        x_text = pos[0] - 0.25
        y_text = pos[1] + pos[3]/2.
        fig.text(x_text, y_text, name, va='center', ha='left', fontsize=10)

    fig.savefig('my-gradients.pdf')

def hsv2rgb(h, s, v):
    if v == 0:
        return (0,0,0)
    h /= 60
    i = math.floor(h)
    f = h - i
    p = v * (1 - s)
    q = v * (1 - (s*f))
    t = v * (1 - (s * (1 - f)))
    if i == 0:
        return(v,t,p)
    if i == 1:
        return(q,v,p)
    if i == 2:
        return(p,v,t)
    if i == 3:
        return(p,q,v)
    if i == 4:
        return(t,p,v)
    if i == 5:
        return(v,p,q)

def gradient_rgb_bw(v):
    return (v)


def gradient_rgb_gbr(v):
    return (np.maximum(0, (v-0.5)*2), np.maximum(0, (1-v-0.5)*2), 1-np.absolute((v-0.5)*2))


def gradient_rgb_gbr_full(v):
    if v < 0.25:
        return (0, 1, v*4)
    elif v < 0.5:
        return (0, 1 - (v - 0.25)*4, 1)
    elif v < 0.75:
        return ((v - 0.5)*4, 0, 1)
    else:
        return (1, 0, 1 - (v - 0.75)*4)


def gradient_rgb_wb_custom(v):
    if v < 1/7:
        return (1, 1 - v*7, 1)
    elif v < 2/7:
        return (1 - (v - 1/7)*7, 0, 1)
    elif v < 3/7:
        return (0, (v - 2/7)*7, 1)
    elif v < 4/7:
        return (0, 1, 1 - (v-3/7)*7)
    elif v < 5/7:
        return ((v - 4/7)*7, 1, 0)
    elif v < 6/7:
        return (1, 1 - (v - 5/7)*7, 0)
    else:
        return (1 - (v - 6/7)*7, 0, 0)


def gradient_hsv_bw(v):
    return hsv2rgb(0, 0, v)


def gradient_hsv_gbr(v):
    return hsv2rgb((120 + v*240), 1.0, 1.0)

def gradient_hsv_unknown(v):
    return hsv2rgb((120 - v*120), 0.5, 1.0)


def gradient_hsv_custom(v):
    if v > 0.5:
        return hsv2rgb(v*360, 1.0 - (v - 0.5)*2, 1.0)
    else:
        return hsv2rgb(v*360, 1.0, 1.0)


if __name__ == '__main__':
    def toname(g):
        return g.__name__.replace('gradient_', '').replace('_', '-').upper()

    gradients = (gradient_rgb_bw, gradient_rgb_gbr, gradient_rgb_gbr_full, gradient_rgb_wb_custom,
                 gradient_hsv_bw, gradient_hsv_gbr, gradient_hsv_unknown, gradient_hsv_custom)

    plot_color_gradients(gradients, [toname(g) for g in gradients])
