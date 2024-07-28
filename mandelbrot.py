import torch
import os

import pygame as pg
from pygame import surfarray

import numpy as np
from numpy import int32, uint

"Settings"
screen_x = 512
screen_y = 256

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

def calculate_point(x, y):
    r = x%256
    g = y%256
    b = (x*y)%256
    return (r,g,b)

def main():
    pg.init()
    pg.display.set_caption("mandelbrot")

    values = np.zeros((screen_x, screen_y, 3), int32)
    for x in range(screen_x):
        for y in range(screen_y):
            (r,g,b) = calculate_point(x,y)
            values[x][y] = (r,g,b)
    show_array(values)

    wait_click()

    pg.quit()

if __name__ == "__main__":
    main()
