import torch
import os
import time

import pygame as pg
from pygame import surfarray

import numpy as np
from numpy import int32, uint, uint8

"Settings"
screen_x = 1024
screen_y = 768
max_iter = 254
m_center = -0.6+0j
m_width = 1.8
m_height = m_width * (screen_y/screen_x)

color_step = 255//(max_iter+1)
print(color_step)

def set_viewport():
    global top_left, bottom_right, h_step, v_step
    top_left = m_center - complex(m_width, m_height)
    bottom_right = m_center + complex(m_width, m_height)
    h_step = (bottom_right.real - top_left.real) / screen_x
    v_step = (bottom_right.imag - top_left.imag) / screen_y

def recenter(x, y):
    global m_center
    m_center = get_c(x,y)
    print(m_center)

def zoom(mult):
    global m_width, m_height, screen_y, screen_x
    m_width = m_width * mult
    m_height = m_width * (screen_y/screen_x)

def show_array(array_img):
    screen = pg.display.set_mode(array_img.shape[:2], 0, 32)
    surfarray.blit_array(screen, array_img)
    pg.display.flip()

def mouse_zoom(x, y):
    recenter(x, y)
    zoom(0.75)
    render_mandelbrot()

def mouse_reframe(start, end):
    print(start,end)
    if abs(start[0]-end[0]) < 4:
        mouse_zoom(start[0], start[1])
        return

    global m_width, m_height, screen_y, screen_x
    m_width = abs(start[0]-end[0])//2 * h_step
    m_height = m_width * (screen_y/screen_x)
    n_x = start[0] + ((end[0]-start[0])//2)
    n_y = start[1] + ((end[1]-start[1])//2)
    print(n_x, n_y, m_width)
    recenter(n_x, n_y)
    render_mandelbrot()

def wait_click():
    dragging = False
    start_drag = (0,0)
    while True:
        e = pg.event.wait()
        
        # Force application to only advance when main button is released
        if e.type == pg.MOUSEBUTTONUP and e.button == pg.BUTTON_LEFT:
            if dragging:
                end_drag = e.pos
            else:
                end_drag = start_drag
            mouse_reframe(start_drag, end_drag)
            dragging = False
        elif e.type == pg.MOUSEBUTTONDOWN and e.button == pg.BUTTON_LEFT:
            start_drag = e.pos
            dragging = True
        elif e.type == pg.KEYDOWN and e.key == pg.K_MINUS:
            zoom(1.5)
            render_mandelbrot()
        elif e.type == pg.KEYDOWN and e.key == pg.K_EQUALS:
            print(e.key)
            zoom(0.75)
            render_mandelbrot()
        elif (e.type == pg.KEYDOWN and e.key == pg.K_q) or e.type == pg.QUIT:
            pg.quit()
            raise SystemExit()
        elif e.type == pg.KEYDOWN:
            print(e.key)

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
    return i * color_step

def render_mandelbrot():
    set_viewport()
    print(top_left)
    values = np.zeros((screen_x, screen_y, 3), uint8)
    time_s = time.time()
    for x in range(screen_x):
        for y in range(screen_y):
            point_color = calculate_point(x,y)
            values[x][y] = point_color

    time_e = time.time()
    print(time_e - time_s)
    show_array(values)

def main():
    pg.init()
    pg.display.set_caption("mandelbrot")

    render_mandelbrot()

    wait_click()

    pg.quit()

if __name__ == "__main__":
    main()
