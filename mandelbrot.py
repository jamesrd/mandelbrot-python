import torch
import os
import time

import pygame as pg
from pygame import surfarray

import numpy as np
from numpy import int32, uint

"Settings"
screen_x = 1024
screen_y = 768
max_iter = 150
top_left = -1.5-1.25j
bottom_right = 0.75+1.25j

"calculations"
h_step = (bottom_right.real - top_left.real) / screen_x
v_step = (bottom_right.imag - top_left.imag) / screen_y

"colors"
color_black = (0,0,0)
color_red = (255,0,0)
color_green = (0,255,0)
color_blue = (0,0,255)
c_step1 = max_iter//8
c_step2 = c_step1 * 3


def show_array(array_img):
    screen = pg.display.set_mode(array_img.shape[:2], 0, 32)
    surfarray.blit_array(screen, array_img)
    pg.display.flip()

def wait_click():
    while True:
        e = pg.event.wait()
        
        # Force application to only advance when main button is released
        if e.type == pg.MOUSEBUTTONUP and e.button == pg.BUTTON_LEFT:
            break
        elif e.type == pg.QUIT:
            pg.quit()
            raise SystemExit()

def get_c(x, y):
    return top_left + complex(x * h_step, y * v_step)

def check_point(c):
    i = 1
    z = 0+0j+c
    while i <= max_iter:
        i = i + 1
        z = (z*z)+c
        if abs(z.real) > 2 or abs(z.imag) > 2:
            return i

    return i

def calculate_point(x, y):
    c = get_c(x,y)
    i = check_point(c)
    return color_point(i)

def color_point(i):
    if i < c_step1:
        return tuple(z * (i/c_step1) for z in color_red)
    if i < c_step2:
        return tuple(z * (i/c_step2) for z in color_green)
    elif i < max_iter:
        return color_blue
    return color_black

def main():
    pg.init()
    pg.display.set_caption("mandelbrot")

    values = np.zeros((screen_x, screen_y, 3), int32)
    time_s = time.time()
    for x in range(screen_x):
        for y in range(screen_y):
            (r,g,b) = calculate_point(x,y)
            values[x][y] = (r,g,b)

    time_e = time.time()
    print(time_e - time_s)
    show_array(values)

    wait_click()

    pg.quit()

if __name__ == "__main__":
    main()
