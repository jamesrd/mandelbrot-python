import torch
import os

import pygame as pg
from pygame import surfarray

import numpy as np
from numpy import int32, uint

def surfdemo_show(array_img):
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


def main():
    pg.init()
    pg.display.set_caption("mandelbrot")

    # striped
    # the element type is required for np.zeros in numpy else
    # an array of float is returned.
    striped = np.zeros((512, 256, 3), int32)
    striped[:] = (255, 0, 0)
    striped[:, ::3] = (0, 255, 255)
    surfdemo_show(striped)

    wait_click()

    pg.quit()

if __name__ == "__main__":
    main()
