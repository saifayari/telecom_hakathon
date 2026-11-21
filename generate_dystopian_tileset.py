import os
import numpy as np
from PIL import Image

day_tileset = Image.open('assets/sprites/environment/metalslug_tileset_day.png')
night_tileset = Image.open('assets/sprites/environment/metalslug_tileset_night.png')

d_arr = np.array(day_tileset)
n_arr = np.array(night_tileset)

tile_w, tile_h = 32, 32

def put_tile(col, row, d_tile, n_tile):
    x0, y0 = col * tile_w, row * tile_h
    d_arr[y0:y0+tile_h, x0:x0+tile_w] = d_tile
    n_arr[y0:y0+tile_h, x0:x0+tile_w] = n_tile

# Base earth reference
d_base = d_arr[0:32, 0:32].copy()
n_base = n_arr[0:32, 0:32].copy()

# ----------------- TILE (1, 0): TOXIC ACID POOL / CHEMICAL SEEP -----------------
d_acid = d_base.copy()
n_acid = n_base.copy()
for y in range(32):
    for x in range(32):
        # Irregular toxic puddle shape
        dist = np.hypot((x - 16) * 1.1, (y - 15) * 1.3) + 2.0 * np.sin(x * 0.5) * np.cos(y * 0.6)
        if dist < 6.5:
            # Deep pool
            d_acid[y, x] = [135, 175, 45, 255] # Day: vibrant acid sludge
            n_acid[y, x] = [50, 255, 70, 255]  # Night: glowing radioactive green!
        elif dist < 9.5:
            # Slime rim
            d_acid[y, x] = [105, 135, 38, 255]
            n_acid[y, x] = [25, 200, 50, 255]
        elif dist < 12.0:
            # Corroded soil border
            d_acid[y, x] = [65, 80, 32, 255]
            n_acid[y, x] = [15, 90, 30, 255]

# Acid bubbles
for bx, by in [(14, 13), (17, 16), (13, 17)]:
    d_acid[by, bx] = [190, 230, 80, 255]
    n_acid[by, bx] = [180, 255, 150, 255] # glowing bubble center
put_tile(1, 0, d_acid, n_acid)

# ----------------- TILE (2, 0): BROKEN CRUMBLING CONCRETE & EXPOSED REBAR -----------------
d_rebar = d_base.copy()
n_rebar = n_base.copy()
# Cracked concrete slab covering top-left half
for y in range(32):
    for x in range(32):
        if x + y < 38 + np.sin(x) * 2:
            d_rebar[y, x] = [118, 122, 114, 255] # concrete gray
            n_rebar[y, x] = [38, 44, 52, 255]
            if (x * 3 + y * 2) % 11 == 0:
                d_rebar[y, x] = [90, 94, 88, 255]
                n_rebar[y, x] = [26, 30, 36, 255]
# Exposed rusted rebar rods sticking out
# Rod 1: (18, 14) to (27, 23)
for i in range(10):
    rx, ry = 16 + i, 12 + i
    if 0 <= rx < 32 and 0 <= ry < 32:
        d_rebar[ry, rx] = [165, 75, 35, 255] # rusted rebar
        d_rebar[ry+1, rx] = [80, 35, 15, 255] # rebar shadow
        n_rebar[ry, rx] = [75, 40, 20, 255]
        n_rebar[ry+1, rx] = [30, 15, 10, 255]
# Rod 2: (10, 20) to (18, 28)
for i in range(9):
    rx, ry = 10 + i, 20 + i
    if 0 <= rx < 32 and 0 <= ry < 32:
        d_rebar[ry, rx] = [165, 75, 35, 255]
        d_rebar[ry+1, rx] = [80, 35, 15, 255]
        n_rebar[ry, rx] = [75, 40, 20, 255]
        n_rebar[ry+1, rx] = [30, 15, 10, 255]
put_tile(2, 0, d_rebar, n_rebar)

# ----------------- TILE (3, 0): E-WASTE & DISCARDED CIRCUIT BOARD SCRAP -----------------
d_ewaste = d_base.copy()
n_ewaste = n_base.copy()
# Scattered green PCB fragments
pcb_rects = [(6, 8, 8, 6), (18, 16, 9, 7), (8, 21, 6, 5)]
for px, py, pw, ph in pcb_rects:
    d_ewaste[py:py+ph, px:px+pw] = [48, 88, 48, 255] # PCB dark green
    n_ewaste[py:py+ph, px:px+pw] = [20, 42, 24, 255]
    # Copper traces & solder pads
    for cx in range(px + 1, px + pw - 1, 2):
        d_ewaste[py + 1:py + ph - 1, cx] = [185, 120, 45, 255] # copper trace
        n_ewaste[py + 1:py + ph - 1, cx] = [85, 55, 20, 255]
    # Solder joints / capacitors
    d_ewaste[py + 1, px + 1] = [180, 185, 190, 255]
    d_ewaste[py + ph - 2, px + pw - 2] = [180, 185, 190, 255]
    # Night: flickering micro LED
    n_ewaste[py + 1, px + 1] = [0, 255, 200, 255]

# Tangled wires snaking through mud
wire_pts = [(2, 12), (5, 13), (9, 15), (14, 18), (17, 24), (22, 27), (28, 28)]
for wx, wy in wire_pts:
    d_ewaste[wy, wx] = [190, 40, 30, 255] # red wire
    d_ewaste[wy+1, wx] = [30, 30, 30, 255] # black ground wire
    n_ewaste[wy, wx] = [100, 20, 15, 255]
    n_ewaste[wy+1, wx] = [15, 15, 15, 255]
put_tile(3, 0, d_ewaste, n_ewaste)

# ----------------- TILE (4, 0): SCORCHED BLAST CRATER & ASH -----------------
d_crater = d_base.copy()
n_crater = n_base.copy()
for y in range(32):
    for x in range(32):
        dist = np.hypot(x - 16, y - 16)
        if dist < 6:
            d_crater[y, x] = [28, 26, 24, 255] # charred black pit
            n_crater[y, x] = [12, 10, 10, 255]
        elif dist < 10:
            d_crater[y, x] = [58, 54, 48, 255] # soot ring
            n_crater[y, x] = [22, 20, 18, 255]
        elif dist < 14 and (x ^ y) % 3 == 0:
            d_crater[y, x] = [82, 76, 68, 255] # ash splatter
            n_crater[y, x] = [35, 32, 28, 255]

# Glowing embers inside crater at night
for ex, ey in [(15, 14), (17, 16), (14, 17)]:
    d_crater[ey, ex] = [160, 60, 20, 255]
    n_crater[ey, ex] = [255, 90, 10, 255] # glowing orange ember
put_tile(4, 0, d_crater, n_crater)

# ----------------- TILE (5, 0): OIL SLICK / PETROCHEMICAL PUDDLE -----------------
d_oil = d_base.copy()
n_oil = n_base.copy()
for y in range(32):
    for x in range(32):
        dist = np.hypot((x - 17) * 1.4, (y - 15) * 1.0)
        if dist < 7:
            # Dark petroleum sheen
            d_oil[y, x] = [32, 34, 38, 255]
            n_oil[y, x] = [14, 16, 22, 255]
        elif dist < 11:
            # Iridescent purple/blue petrol film
            d_oil[y, x] = [62, 54, 72, 255]
            n_oil[y, x] = [25, 30, 42, 255]
put_tile(5, 0, d_oil, n_oil)

# ----------------- TILE (0, 3): COILED RAZOR WIRE ON POST -----------------
d_razor = d_base.copy()
n_razor = n_base.copy()
# Rusted steel post in center
d_razor[3:29, 14:18] = [75, 45, 30, 255]
d_razor[3:29, 15:17] = [110, 65, 40, 255]
n_razor[3:29, 14:18] = [30, 22, 18, 255]
n_razor[3:29, 15:17] = [50, 36, 28, 255]
# Coiled razor circles
for cy in [9, 16, 23]:
    for a in np.linspace(0, 2*np.pi, 24):
        cx = int(16 + 11 * np.cos(a))
        py = int(cy + 5 * np.sin(a))
        if 0 <= cx < 32 and 0 <= py < 32:
            d_razor[py, cx] = [150, 155, 150, 255] # razor wire silver
            n_razor[py, cx] = [65, 75, 82, 255]
            # Barbs
            if int(a * 4) % 3 == 0:
                d_razor[py, cx] = [170, 75, 35, 255] # rusted barb
                n_razor[py, cx] = [80, 40, 20, 255]
put_tile(0, 3, d_razor, n_razor)

# ----------------- TILE (3, 3): LEAKING TOXIC CHEMICAL DRUM -----------------
d_barrel = d_base.copy()
n_barrel = n_base.copy()
# Toxic sludge leak under barrel
for by in range(16, 30):
    for bx in range(4, 28):
        if np.hypot(bx - 16, by - 22) < 7:
            d_barrel[by, bx] = [120, 155, 40, 255]
            n_barrel[by, bx] = [40, 240, 60, 255] # toxic glow
# Corroded yellow barrel body
d_barrel[6:22, 9:23] = [185, 145, 30, 255] # hazardous yellow
n_barrel[6:22, 9:23] = [80, 65, 15, 255]
# Rust streaks & ribs
d_barrel[10:12, 9:23] = [140, 70, 30, 255]
d_barrel[17:19, 9:23] = [140, 70, 30, 255]
n_barrel[10:12, 9:23] = [55, 28, 14, 255]
n_barrel[17:19, 9:23] = [55, 28, 14, 255]
# Biohazard black stencil in center
d_barrel[12:16, 14:18] = [30, 30, 30, 255]
n_barrel[12:16, 14:18] = [15, 15, 15, 255]
put_tile(3, 3, d_barrel, n_barrel)

# Save updated tilesets
Image.fromarray(d_arr).save('assets/sprites/environment/metalslug_tileset_day.png')
Image.fromarray(n_arr).save('assets/sprites/environment/metalslug_tileset_night.png')
print('Dystopian tiles successfully infused into master tilesets!')
