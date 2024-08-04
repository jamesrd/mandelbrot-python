## About

Mandelbrot visualization in Python.

PyTorch is used for the set calculation. It can take advantage of GPU backends
to speed up computations.

PyGame is used to show the visualization and provide interactivity.

### To get set up:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### To run it:

```sh
python3 main.py
```

### Interacting

Controls:
* Click anywhere to zoom in on that point
* Click and drag over an area to zoom more quickly to that area
* Press `-` (minus) to zoom out
* Press `=` (equals) to zoom in
* Press `q` to quit

