import torch

target_device = "mps"

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

def render_mandelbrot_old(screen_x, screen_y, max_iter, top_left, h_step, v_step):
    values = np.zeros((screen_x, screen_y, 3), uint8)
    for x in range(screen_x):
        for y in range(screen_y):
            point_color = calculate_point(x,y, top_left, h_step, v_step, max_iter)
            values[x][y] = point_color

    return values

def render_mandelbrot(screen_x, screen_y, max_iter, top_left, h_step, v_step):
    x = torch.linspace(top_left.real, top_left.real + screen_x * h_step, screen_x, dtype=torch.float).to(target_device)
    y = torch.linspace(top_left.imag, top_left.imag + screen_y * v_step, screen_y, dtype=torch.float).to(target_device)

    cx, cy = torch.meshgrid([x,y])

    zx = torch.zeros(screen_x * screen_y, dtype=torch.float32).to(target_device).resize_as_(cx)
    zy = torch.zeros(screen_x * screen_y, dtype=torch.float32).to(target_device).resize_as_(cy)

    k = torch.zeros(screen_x * screen_y, dtype=torch.uint8).reshape(screen_x,screen_y).to(target_device)

    for i in range(max_iter):
        zx2 = zx**2
        zy2 = zy**2
        #inf is a tensor containing all the points for which zx2+zy2>4
        inf = (zx2+zy2)>4 #if zx2+zy2>4 then sqrt(zx2+zy2)>2, i.e. point's distance from (0,0) is >2, i.e. it will escape to inifinity; 
        k[inf] = i #for all the points escaping to infinity, store the number of iteration when that was this discovered
        zxn = zx2 - zy2 + cx #
        zyn = 2*zx*zy + cy
        zx = zxn
        zy = zyn
    
    return k.numpy(force=True)
