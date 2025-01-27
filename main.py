import pygame as pg
from pygame import surfarray
import time
import torch

import mandelbrot as m

"Settings"
target_device = "mps" # change to cpu if you're not on Apple Silicon
screen_x = 1024
screen_y = 768
max_iter = 255
m_center = (-0.6,0)
m_width = 3.6
m_height = m_width * (screen_y/screen_x)

"Methods for translating screen coordinates to Mandelbrot set coordinates"

def set_viewport():
    global screen_x, screen_y, m_width, m_height
    top_left = (m_center[0] - (m_width / 2), m_center[1] - (m_height / 2))
    bottom_right = (m_center[0] + (m_width / 2), m_center[1] + (m_height / 2))
    return top_left, bottom_right

def recenter(x, y):
    global m_center, screen_x, screen_y
    top_left = (m_center[0] - (m_width / 2), m_center[1] - (m_height / 2))
    h_step = m_width / screen_x
    v_step = m_height / screen_y
    m_center = (top_left[0] + x * h_step, top_left[1] + y * v_step)

def zoom(mult):
    global m_width, m_height
    m_width = m_width * mult
    m_height = m_height * mult

def mouse_zoom(x, y):
    recenter(x, y)
    zoom(0.75)
    render_mandelbrot()

def mouse_reframe(start, end):
    # if area dragged isn't too large just zoom
    if abs(start[0]-end[0]) < 4:
        mouse_zoom(start[0], start[1])
        return

    global m_width, m_height, screen_y, screen_x
    n_x = start[0] + ((end[0]-start[0])//2)
    n_y = start[1] + ((end[1]-start[1])//2)
    recenter(n_x, n_y)
    h_step = m_width / screen_x
    m_width = abs(start[0]-end[0]) * h_step
    m_height = m_width * (screen_y/screen_x)
    render_mandelbrot()

"Display methods"

def build_palette(pmode):
    global surf_palette
    loop = range(256)
    if pmode == 'bw':
        # black & white:
        surf_palette = [(255, 255, 255) for x in loop]
        surf_palette[0] = (0,0,0)
    elif pmode == 'red':
        # red gradient
        surf_palette = [(x,0,0) for x in loop]
    elif pmode == 'green':
        # green gradient
        surf_palette = [(0,x,0) for x in loop]
    elif pmode == 'blue':
        # blue gradient
        surf_palette = [(0,0,x) for x in loop]
    elif pmode == 'greenblue':
        surf_palette = [(0,x,x) for x in loop]
    else:
        # gray scale:
        surf_palette = [(x,x,x) for x in loop]

def show_array(array_img):
    surf =surfarray.make_surface(array_img)
    surf.set_palette(surf_palette)
    screen.blit(surf, (0,0))
    pg.display.flip()

def init_display():
    global screen_x, screen_y, m_width, m_height
    global screen
    screen = pg.display.set_mode((screen_x,screen_y), 0, 32)
    (screen_x, screen_y) = pg.display.get_window_size()
    m_height = m_width * (screen_y/screen_x)
    build_palette('greenblue')
    pg.display.set_caption("mandelbrot")

"UI interaction method"

def wait_click():
    dragging = False
    start_drag = (0,0)
    while True:
        e = pg.event.wait()
        
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
            zoom(0.75)
            render_mandelbrot()
        elif (e.type == pg.KEYDOWN and e.key == pg.K_q) or e.type == pg.QUIT:
            pg.quit()
            raise SystemExit()

def render_mandelbrot():
    global screen_x, screen_y
    top_left, bottom_right = set_viewport()
    time_s = time.time()
    x_range = (top_left[0], bottom_right[0])
    y_range = (top_left[1], bottom_right[1])
    values = m.render_mandelbrot(screen_x, screen_y, max_iter, x_range, y_range)
    va = values.cpu().numpy()
    time_e = time.time()
    print("calc time: {}s".format(time_e-time_s))
    show_array(va)

def main():
    m.target_device = target_device

    pg.init()
    init_display()

    render_mandelbrot()

    wait_click()

    pg.quit()

if __name__ == "__main__":
    main()
