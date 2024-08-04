import torch

target_device = "mps"

def render_mandelbrot(screen_x, screen_y, max_iter, top_left, h_step, v_step):
    global target_device
    x = torch.linspace(top_left.real, top_left.real + screen_x * h_step, screen_x, dtype=torch.float32).to(target_device)
    y = torch.linspace(top_left.imag, top_left.imag + screen_y * v_step, screen_y, dtype=torch.float32).to(target_device)

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
    
    return k
