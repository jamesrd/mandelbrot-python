import torch

target_device = "mps"

def render_mandelbrot(width, height, max_iter, x_range, y_range):
    global target_device
    x = torch.linspace(x_range[0], x_range[1], width, dtype=torch.float32).to(target_device)
    y = torch.linspace(y_range[0], y_range[1], height, dtype=torch.float32).to(target_device)

    cx, cy = torch.meshgrid([x,y])

    zx = torch.zeros(width * height, dtype=torch.float32).to(target_device).resize_as_(cx)
    zy = torch.zeros(width * height, dtype=torch.float32).to(target_device).resize_as_(cy)

    k = torch.zeros(width * height, dtype=torch.uint8).reshape(width,height).to(target_device)

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
