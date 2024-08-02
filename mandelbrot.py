import torch

import numpy as np
from numpy import int32, uint, uint8

def get_c(x, y, top_left, h_step, v_step):
    return top_left + complex(x * h_step, y * v_step)

def check_point(c, max_iter):
    i = 1
    z = 0+0j+c
    while i <= max_iter:
        i = i + 1
        z = (z*z)+c
        if abs(z.real) > 2 or abs(z.imag) > 2:
            return i

    return i

def calculate_point(x, y, top_left, h_step, v_step, max_iter):
    c = get_c(x,y, top_left, h_step, v_step)
    i = check_point(c, max_iter)
    return i

def render_mandelbrot(screen_x, screen_y, max_iter, top_left, h_step, v_step):
    values = np.zeros((screen_x, screen_y, 3), uint)
    for x in range(screen_x):
        for y in range(screen_y):
            point_color = calculate_point(x,y, top_left, h_step, v_step, max_iter)
            values[x][y] = point_color

    return values
