import os
import numpy as np
from PIL import Image

os.makedirs('assets/sprites/environment', exist_ok=True)

# ----------------- LOAD SOURCE ASSETS -----------------
utumno = Image.open('project_utumno.png')
treepack = Image.open('treepacknewest.png')
dead_src = Image.open('pixeltroid_tree_rep2.png')

# ----------------- PALETTE HELPERS -----------------
def remap_dirt_tile(tile, is_night=False):
    arr = np.array(tile).astype(float)
    rgb = arr[:, :, :3]
    lum = (0.299 * rgb[:,:,0] + 0.587 * rgb[:,:,1] + 0.114 * rgb[:,:,2]) / 255.0
    out = np.zeros((32, 32, 4), dtype=np.uint8)
    out[:, :, 3] = 255
    if not is_night:
        c_dark = np.array([55, 62, 44])
        c_mid = np.array([98, 108, 82])
        c_light = np.array([138, 150, 118])
    else:
        c_dark = np.array([20, 24, 20])
        c_mid = np.array([38, 45, 36])
        c_light = np.array([62, 72, 58])
    c = np.where(lum[:,:,None] < 0.5,
                 c_dark + (c_mid - c_dark) * (lum[:,:,None] / 0.5),
                 c_mid + (c_light - c_mid) * ((lum[:,:,None] - 0.5) / 0.5))
    out[:, :, :3] = np.clip(c, 0, 255)
    return out

# Sample natural dirt tiles from Utumno row 6 (y: 192 to 224)
dirt_raw_1 = utumno.crop((32, 192, 64, 224))
dirt_raw_2 = utumno.crop((64, 192, 96, 224))
dirt_raw_3 = utumno.crop((96, 192, 128, 224))
dirt_raw_4 = utumno.crop((128, 192, 160, 224))
dirt_raw_5 = utumno.crop((160, 192, 192, 224))
dirt_raw_6 = utumno.crop((192, 192, 224, 224))
dirt_raw_7 = utumno.crop((224, 192, 256, 224))

# ----------------- BUILD 8x4 TILESET -----------------
tile_w, tile_h = 32, 32
cols, rows = 8, 4
day_tileset = np.zeros((rows * tile_h, cols * tile_w, 4), dtype=np.uint8)
night_tileset = np.zeros((rows * tile_h, cols * tile_w, 4), dtype=np.uint8)

def put_tile(col, row, d_tile, n_tile):
    x0, y0 = col * tile_w, row * tile_h
    day_tileset[y0:y0+tile_h, x0:x0+tile_w] = d_tile
    night_tileset[y0:y0+tile_h, x0:x0+tile_w] = n_tile

# ROW 0: Ground Earth Tiles
# (0, 0): Base Wasteland Dirt
d_base = remap_dirt_tile(dirt_raw_1, False)
n_base = remap_dirt_tile(dirt_raw_1, True)
put_tile(0, 0, d_base, n_base)

# (1, 0): Fissure / Cracked Mud
d_crack = remap_dirt_tile(dirt_raw_2, False)
n_crack = remap_dirt_tile(dirt_raw_2, True)
put_tile(1, 0, d_crack, n_crack)

# (2, 0): Gravel & Small Rocks
d_grav = remap_dirt_tile(dirt_raw_3, False)
n_grav = remap_dirt_tile(dirt_raw_3, True)
put_tile(2, 0, d_grav, n_grav)

# (3, 0): Olive Weed Tufts
d_weed = remap_dirt_tile(dirt_raw_4, False)
n_weed = remap_dirt_tile(dirt_raw_4, True)
# Overlay grass tufts
tufts = [(7, 10), (8, 9), (9, 10), (7, 11), (9, 11),
         (21, 20), (22, 19), (23, 20), (21, 21), (23, 21),
         (14, 25), (15, 24), (16, 25)]
for tx, ty in tufts:
    d_weed[ty, tx] = [82, 106, 54, 255]
    n_weed[ty, tx] = [34, 52, 40, 255]
put_tile(3, 0, d_weed, n_weed)

# (4, 0): Embedded Metal Scrap Plate with Rivets
d_plate = d_base.copy()
n_plate = n_base.copy()
d_plate[6:26, 6:26] = [92, 96, 90, 255]
n_plate[6:26, 6:26] = [30, 36, 42, 255]
d_plate[9:14, 8:16] = [138, 72, 38, 255]
n_plate[9:14, 8:16] = [68, 38, 22, 255]
d_plate[18:23, 17:24] = [138, 72, 38, 255]
n_plate[18:23, 17:24] = [68, 38, 22, 255]
d_plate[6, 6:26] = [128, 132, 124, 255]
d_plate[6:26, 6] = [128, 132, 124, 255]
d_plate[25, 6:26] = [40, 42, 38, 255]
d_plate[6:26, 25] = [40, 42, 38, 255]
n_plate[6, 6:26] = [52, 62, 72, 255]
n_plate[6:26, 6] = [52, 62, 72, 255]
n_plate[25, 6:26] = [10, 12, 16, 255]
n_plate[6:26, 25] = [10, 12, 16, 255]
for rx, ry in [(8, 8), (23, 8), (8, 23), (23, 23), (15, 15), (16, 15)]:
    d_plate[ry, rx] = [128, 132, 124, 255]
    d_plate[ry+1, rx] = [40, 42, 38, 255]
    n_plate[ry, rx] = [0, 180, 200, 255] if (rx == 15 or rx == 16) else [52, 62, 72, 255]
    n_plate[ry+1, rx] = [10, 12, 16, 255]
put_tile(4, 0, d_plate, n_plate)

# (5, 0): Crawler Tread Earth
d_tread = remap_dirt_tile(dirt_raw_5, False)
n_tread = remap_dirt_tile(dirt_raw_5, True)
for ty in range(2, 30, 4):
    d_tread[ty:ty+2, 4:12] = [55, 62, 44, 255]
    d_tread[ty:ty+2, 20:28] = [55, 62, 44, 255]
    n_tread[ty:ty+2, 4:12] = [20, 24, 20, 255]
    n_tread[ty:ty+2, 20:28] = [20, 24, 20, 255]
put_tile(5, 0, d_tread, n_tread)

# (6, 0): Rusted Scrap Shards Earth
d_shards = remap_dirt_tile(dirt_raw_6, False)
n_shards = remap_dirt_tile(dirt_raw_6, True)
for sx, sy, sw, sh in [(8, 12, 5, 3), (20, 8, 4, 3), (16, 22, 6, 2)]:
    d_shards[sy:sy+sh, sx:sx+sw] = [138, 72, 38, 255]
    n_shards[sy:sy+sh, sx:sx+sw] = [68, 38, 22, 255]
    d_shards[sy, sx:sx+sw] = [128, 132, 124, 255]
    n_shards[sy, sx:sx+sw] = [52, 62, 72, 255]
put_tile(6, 0, d_shards, n_shards)

# (7, 0): Scorched Crater Earth
d_crater = remap_dirt_tile(dirt_raw_7, False)
n_crater = remap_dirt_tile(dirt_raw_7, True)
for cy in range(32):
    for cx in range(32):
        dist = np.hypot(cx - 16, cy - 16)
        if dist < 6:
            d_crater[cy, cx] = [40, 42, 38, 255]
            n_crater[cy, cx] = [14, 18, 14, 255]
        elif dist < 11:
            d_crater[cy, cx] = [52, 58, 42, 255]
            n_crater[cy, cx] = [20, 24, 20, 255]
put_tile(7, 0, d_crater, n_crater)

# ROW 1: Foundation Platform Outer Edges
D_STEEL = np.array([92, 96, 90, 255], dtype=np.uint8)
D_STEEL_D = np.array([64, 68, 62, 255], dtype=np.uint8)
D_STEEL_DD = np.array([40, 42, 38, 255], dtype=np.uint8)
D_STEEL_L = np.array([128, 132, 124, 255], dtype=np.uint8)
D_HAZ_Y = np.array([195, 155, 35, 255], dtype=np.uint8)
D_HAZ_B = np.array([32, 34, 30, 255], dtype=np.uint8)

N_STEEL = np.array([30, 36, 42, 255], dtype=np.uint8)
N_STEEL_D = np.array([18, 22, 26, 255], dtype=np.uint8)
N_STEEL_DD = np.array([10, 12, 16, 255], dtype=np.uint8)
N_STEEL_L = np.array([52, 62, 72, 255], dtype=np.uint8)
N_HAZ_Y = np.array([135, 95, 20, 255], dtype=np.uint8)
N_HAZ_B = np.array([14, 16, 18, 255], dtype=np.uint8)
N_CYAN = np.array([0, 240, 255, 255], dtype=np.uint8)
N_CYAN_DIM = np.array([0, 130, 150, 255], dtype=np.uint8)
N_AMBER = np.array([255, 140, 0, 255], dtype=np.uint8)

# Inner Floor (4, 1)
dp_inner = np.full((32, 32, 4), D_STEEL, dtype=np.uint8)
np_inner = np.full((32, 32, 4), N_STEEL, dtype=np.uint8)
dp_inner[15:17, :] = D_STEEL_DD
dp_inner[:, 15:17] = D_STEEL_DD
np_inner[15:17, :] = N_STEEL_DD
np_inner[:, 15:17] = N_STEEL_DD
dp_inner[0, :] = D_STEEL_L
dp_inner[:, 0] = D_STEEL_L
dp_inner[17, :] = D_STEEL_L
dp_inner[:, 17] = D_STEEL_L
np_inner[0, :] = N_STEEL_L
np_inner[:, 0] = N_STEEL_L
np_inner[17, :] = N_STEEL_L
np_inner[:, 17] = N_STEEL_L
for rx, ry in [(2, 2), (13, 2), (2, 13), (13, 13), (19, 2), (29, 2), (19, 13), (29, 13),
               (2, 19), (13, 19), (2, 29), (13, 29), (19, 19), (29, 19), (19, 29), (29, 29)]:
    dp_inner[ry, rx] = D_STEEL_L
    dp_inner[ry+1, rx] = D_STEEL_DD
    np_inner[ry, rx] = N_STEEL_L
    np_inner[ry+1, rx] = N_STEEL_DD
put_tile(4, 1, dp_inner, np_inner)

# Corner TL (0, 1)
dp_tl = d_base.copy()
np_tl = n_base.copy()
dp_tl[8:, 8:] = dp_inner[8:, 8:]
np_tl[8:, 8:] = np_inner[8:, 8:]
dp_tl[8:12, 8:] = D_STEEL_DD
dp_tl[8:, 8:12] = D_STEEL_DD
np_tl[8:12, 8:] = N_STEEL_DD
np_tl[8:, 8:12] = N_STEEL_DD
for i in range(8, 32):
    dp_tl[8:10, i] = D_HAZ_Y if ((i // 4) % 2 == 0) else D_HAZ_B
    dp_tl[i, 8:10] = D_HAZ_Y if ((i // 4) % 2 == 0) else D_HAZ_B
    np_tl[8:10, i] = N_HAZ_Y if ((i // 4) % 2 == 0) else N_HAZ_B
    np_tl[i, 8:10] = N_HAZ_Y if ((i // 4) % 2 == 0) else N_HAZ_B
dp_tl[8:12, 8:12] = D_HAZ_Y
np_tl[8:12, 8:12] = N_AMBER
put_tile(0, 1, dp_tl, np_tl)

# Top Edge (1, 1)
dp_t = d_base.copy()
np_t = n_base.copy()
dp_t[8:, :] = dp_inner[8:, :]
np_t[8:, :] = np_inner[8:, :]
for i in range(32):
    dp_t[8:10, i] = D_HAZ_Y if ((i // 4) % 2 == 0) else D_HAZ_B
    np_t[8:10, i] = N_HAZ_Y if ((i // 4) % 2 == 0) else N_HAZ_B
dp_t[10:12, :] = D_STEEL_DD
np_t[10:12, :] = N_STEEL_DD
put_tile(1, 1, dp_t, np_t)

# Top-Right Corner (2, 1)
dp_tr = d_base.copy()
np_tr = n_base.copy()
dp_tr[8:, :24] = dp_inner[8:, :24]
np_tr[8:, :24] = np_inner[8:, :24]
dp_tr[8:12, :24] = D_STEEL_DD
dp_tr[8:, 20:24] = D_STEEL_DD
np_tr[8:12, :24] = N_STEEL_DD
np_tr[8:, 20:24] = N_STEEL_DD
for i in range(24):
    dp_tr[8:10, i] = D_HAZ_Y if ((i // 4) % 2 == 0) else D_HAZ_B
    dp_tr[i+8, 22:24] = D_HAZ_Y if ((i // 4) % 2 == 0) else D_HAZ_B
    np_tr[8:10, i] = N_HAZ_Y if ((i // 4) % 2 == 0) else N_HAZ_B
    np_tr[i+8, 22:24] = N_HAZ_Y if ((i // 4) % 2 == 0) else N_HAZ_B
dp_tr[8:12, 20:24] = D_HAZ_Y
np_tr[8:12, 20:24] = N_AMBER
put_tile(2, 1, dp_tr, np_tr)

# Left Edge (3, 1)
dp_l = d_base.copy()
np_l = n_base.copy()
dp_l[:, 8:] = dp_inner[:, 8:]
np_l[:, 8:] = np_inner[:, 8:]
for i in range(32):
    dp_l[i, 8:10] = D_HAZ_Y if ((i // 4) % 2 == 0) else D_HAZ_B
    np_l[i, 8:10] = N_HAZ_Y if ((i // 4) % 2 == 0) else N_HAZ_B
dp_l[:, 10:12] = D_STEEL_DD
np_l[:, 10:12] = N_STEEL_DD
put_tile(3, 1, dp_l, np_l)

# Right Edge (5, 1)
dp_r = d_base.copy()
np_r = n_base.copy()
dp_r[:, :24] = dp_inner[:, :24]
np_r[:, :24] = np_inner[:, :24]
for i in range(32):
    dp_r[i, 22:24] = D_HAZ_Y if ((i // 4) % 2 == 0) else D_HAZ_B
    np_r[i, 22:24] = N_HAZ_Y if ((i // 4) % 2 == 0) else N_HAZ_B
dp_r[:, 20:22] = D_STEEL_DD
np_r[:, 20:22] = N_STEEL_DD
put_tile(5, 1, dp_r, np_r)

# Bottom-Left Corner (6, 1)
dp_bl = d_base.copy()
np_bl = n_base.copy()
dp_bl[:24, 8:] = dp_inner[:24, 8:]
np_bl[:24, 8:] = np_inner[:24, 8:]
dp_bl[20:24, 8:] = D_STEEL_DD
dp_bl[:24, 8:12] = D_STEEL_DD
np_bl[20:24, 8:] = N_STEEL_DD
np_bl[:24, 8:12] = N_STEEL_DD
for i in range(8, 32):
    dp_bl[22:24, i] = D_HAZ_Y if ((i // 4) % 2 == 0) else D_HAZ_B
    dp_bl[i-8, 8:10] = D_HAZ_Y if ((i // 4) % 2 == 0) else D_HAZ_B
    np_bl[22:24, i] = N_HAZ_Y if ((i // 4) % 2 == 0) else N_HAZ_B
    np_bl[i-8, 8:10] = N_HAZ_Y if ((i // 4) % 2 == 0) else N_HAZ_B
dp_bl[20:24, 8:12] = D_HAZ_Y
np_bl[20:24, 8:12] = N_AMBER
put_tile(6, 1, dp_bl, np_bl)

# Bottom Edge (7, 1)
dp_b = d_base.copy()
np_b = n_base.copy()
dp_b[:24, :] = dp_inner[:24, :]
np_b[:24, :] = np_inner[:24, :]
for i in range(32):
    dp_b[22:24, i] = D_HAZ_Y if ((i // 4) % 2 == 0) else D_HAZ_B
    np_b[22:24, i] = N_HAZ_Y if ((i // 4) % 2 == 0) else N_HAZ_B
dp_b[20:22, :] = D_STEEL_DD
np_b[20:22, :] = N_STEEL_DD
put_tile(7, 1, dp_b, np_b)

# Bottom-Right Corner (0, 2)
dp_br = d_base.copy()
np_br = n_base.copy()
dp_br[:24, :24] = dp_inner[:24, :24]
np_br[:24, :24] = np_inner[:24, :24]
dp_br[20:24, :24] = D_STEEL_DD
dp_br[:24, 20:24] = D_STEEL_DD
np_br[20:24, :24] = N_STEEL_DD
np_br[:24, 20:24] = N_STEEL_DD
for i in range(24):
    dp_br[22:24, i] = D_HAZ_Y if ((i // 4) % 2 == 0) else D_HAZ_B
    dp_br[i, 22:24] = D_HAZ_Y if ((i // 4) % 2 == 0) else D_HAZ_B
    np_br[22:24, i] = N_HAZ_Y if ((i // 4) % 2 == 0) else N_HAZ_B
    np_br[i, 22:24] = N_HAZ_Y if ((i // 4) % 2 == 0) else N_HAZ_B
dp_br[20:24, 20:24] = D_HAZ_Y
np_br[20:24, 20:24] = N_AMBER
put_tile(0, 2, dp_br, np_br)

# ROW 2: Power Conduits & Center Socket
# Horizontal Conduit (1, 2)
dp_ch = dp_inner.copy()
np_ch = np_inner.copy()
dp_ch[13:19, :] = D_STEEL_DD
dp_ch[14:18, :] = D_STEEL_L
dp_ch[15:17, :] = [138, 72, 38, 255]
np_ch[13:19, :] = N_STEEL_DD
np_ch[14:18, :] = N_CYAN_DIM
np_ch[15:17, :] = N_CYAN
put_tile(1, 2, dp_ch, np_ch)

# Vertical Conduit (2, 2)
dp_cv = dp_inner.copy()
np_cv = np_inner.copy()
dp_cv[:, 13:19] = D_STEEL_DD
dp_cv[:, 14:18] = D_STEEL_L
dp_cv[:, 15:17] = [138, 72, 38, 255]
np_cv[:, 13:19] = N_STEEL_DD
np_cv[:, 14:18] = N_CYAN_DIM
np_cv[:, 15:17] = N_CYAN
put_tile(2, 2, dp_cv, np_cv)

# Conduit Cross Junction (3, 2)
dp_cx = dp_inner.copy()
np_cx = np_inner.copy()
dp_cx[13:19, :] = D_STEEL_DD
dp_cx[:, 13:19] = D_STEEL_DD
dp_cx[14:18, :] = D_STEEL_L
dp_cx[:, 14:18] = D_STEEL_L
dp_cx[15:17, :] = [138, 72, 38, 255]
dp_cx[:, 15:17] = [138, 72, 38, 255]
np_cx[13:19, :] = N_STEEL_DD
np_cx[:, 13:19] = N_STEEL_DD
np_cx[14:18, :] = N_CYAN_DIM
np_cx[:, 14:18] = N_CYAN_DIM
np_cx[15:17, :] = N_CYAN
np_cx[:, 15:17] = N_CYAN
put_tile(3, 2, dp_cx, np_cx)

# Center Tower Socket / Mounting Ring (4, 2)
dp_sock = dp_inner.copy()
np_sock = np_inner.copy()
for cy in range(32):
    for cx in range(32):
        dist = np.hypot(cx - 15.5, cy - 15.5)
        if dist < 6.0:
            dp_sock[cy, cx] = [18, 18, 18, 255]
            np_sock[cy, cx] = [8, 10, 12, 255]
        elif dist < 8.5:
            dp_sock[cy, cx] = D_STEEL_L
            np_sock[cy, cx] = N_CYAN
        elif dist < 11.5:
            dp_sock[cy, cx] = D_STEEL_DD
            np_sock[cy, cx] = N_STEEL_DD
            if int(dist * 2) % 2 == 0 and (cx * cy) % 3 == 0:
                dp_sock[cy, cx] = D_STEEL_L
                np_sock[cy, cx] = N_CYAN_DIM
        elif dist < 14.0:
            dp_sock[cy, cx] = D_STEEL_D
            np_sock[cy, cx] = N_STEEL_D
put_tile(4, 2, dp_sock, np_sock)

# Ventilation Grate (5, 2)
dp_vent = dp_inner.copy()
np_vent = np_inner.copy()
dp_vent[4:28, 4:28] = D_STEEL_DD
np_vent[4:28, 4:28] = N_STEEL_DD
for vy in range(6, 26, 3):
    dp_vent[vy:vy+2, 6:26] = [20, 20, 20, 255]
    np_vent[vy:vy+2, 6:26] = [10, 12, 14, 255]
put_tile(5, 2, dp_vent, np_vent)

# Cable Conduit Terminus (6, 2)
dp_term = dp_inner.copy()
np_term = np_inner.copy()
dp_term[10:22, 4:20] = D_STEEL_DD
dp_term[12:20, 6:18] = [138, 72, 38, 255]
np_term[10:22, 4:20] = N_STEEL_DD
np_term[12:20, 6:18] = N_CYAN_DIM
np_term[14:18, 8:16] = N_CYAN
put_tile(6, 2, dp_term, np_term)

# Warning Beacon Mount Pad (7, 2)
dp_bc = dp_inner.copy()
np_bc = np_inner.copy()
dp_bc[8:24, 8:24] = D_STEEL_DD
dp_bc[11:21, 11:21] = D_HAZ_Y
dp_bc[13:19, 13:19] = [220, 180, 50, 255]
np_bc[8:24, 8:24] = N_STEEL_DD
np_bc[11:21, 11:21] = N_AMBER
np_bc[13:19, 13:19] = [255, 200, 60, 255]
put_tile(7, 2, dp_bc, np_bc)

# ROW 3: Extra Earth Variations & Scrap Barricades
# (0, 3): Scrap Wire Fence Post
dp_f_t = d_base.copy()
np_f_t = n_base.copy()
dp_f_t[4:28, 13:19] = [72, 50, 32, 255]
dp_f_t[4:28, 14:18] = [98, 70, 45, 255]
np_f_t[4:28, 13:19] = [24, 28, 32, 255]
np_f_t[4:28, 14:18] = [40, 48, 56, 255]
for wy in [10, 18, 24]:
    dp_f_t[wy, :] = D_STEEL_L
    dp_f_t[wy+1, :] = D_STEEL_DD
    np_f_t[wy, :] = N_STEEL_L
    np_f_t[wy+1, :] = N_STEEL_DD
    for bx in range(4, 32, 8):
        dp_f_t[wy-1:wy+2, bx] = [138, 72, 38, 255]
        np_f_t[wy-1:wy+2, bx] = [68, 38, 22, 255]
put_tile(0, 3, dp_f_t, np_f_t)

# (1, 3): Scrap Wire Fence Horizontal
dp_f_h = d_base.copy()
np_f_h = n_base.copy()
for wy in [10, 18, 24]:
    dp_f_h[wy, :] = D_STEEL_L
    dp_f_h[wy+1, :] = D_STEEL_DD
    np_f_h[wy, :] = N_STEEL_L
    np_f_h[wy+1, :] = N_STEEL_DD
    for bx in range(2, 32, 6):
        dp_f_h[wy-1:wy+2, bx] = [138, 72, 38, 255]
        np_f_h[wy-1:wy+2, bx] = [68, 38, 22, 255]
put_tile(1, 3, dp_f_h, np_f_h)

# (2, 3): Corrugated Scrap Sheet Barricade
dp_corr = d_base.copy()
np_corr = n_base.copy()
dp_corr[6:26, 2:30] = D_STEEL
np_corr[6:26, 2:30] = N_STEEL
for cx in range(4, 28, 3):
    dp_corr[6:26, cx] = D_STEEL_L
    dp_corr[6:26, cx+1] = D_STEEL_DD
    np_corr[6:26, cx] = N_STEEL_L
    np_corr[6:26, cx+1] = N_STEEL_DD
dp_corr[10:18, 12:22] = [138, 72, 38, 255]
np_corr[10:18, 12:22] = [68, 38, 22, 255]
put_tile(2, 3, dp_corr, np_corr)

# (4, 3), (5, 3), (6, 3): Organic Earth Variations
put_tile(4, 3, remap_dirt_tile(dirt_raw_2, False), remap_dirt_tile(dirt_raw_2, True))
put_tile(5, 3, remap_dirt_tile(dirt_raw_3, False), remap_dirt_tile(dirt_raw_3, True))
put_tile(6, 3, remap_dirt_tile(dirt_raw_5, False), remap_dirt_tile(dirt_raw_5, True))

# Save Tilesets
Image.fromarray(day_tileset).save('assets/sprites/environment/metalslug_tileset_day.png')
Image.fromarray(night_tileset).save('assets/sprites/environment/metalslug_tileset_night.png')
print('Saved master tilesets.')

# ----------------- BUILD TREES & PROPS -----------------
def remap_foliage_tree(im, is_night=False, target_size=None):
    if target_size:
        im = im.resize(target_size, Image.Resampling.NEAREST)
    arr = np.array(im).astype(float)
    alpha = arr[:, :, 3]
    rgb = arr[:, :, :3]
    lum = (0.299 * rgb[:,:,0] + 0.587 * rgb[:,:,1] + 0.114 * rgb[:,:,2]) / 255.0
    is_fol = (rgb[:,:,1] > rgb[:,:,0] * 0.88) & (rgb[:,:,1] > rgb[:,:,2] * 0.88) & (rgb[:,:,1] > 25)
    
    out = np.zeros_like(arr)
    out[:, :, 3] = alpha
    
    if not is_night:
        # Day: Metal Slug olive foliage & weathered wood
        f_dark, f_mid, f_bright = np.array([25, 32, 20]), np.array([75, 92, 48]), np.array([135, 155, 78])
        t_dark, t_mid, t_bright = np.array([24, 18, 14]), np.array([72, 50, 32]), np.array([125, 92, 58])
    else:
        # Night: Nocturnal moonlit slate-cyan & cold charcoal
        f_dark, f_mid, f_bright = np.array([12, 18, 18]), np.array([28, 45, 42]), np.array([55, 88, 80])
        t_dark, t_mid, t_bright = np.array([10, 12, 15]), np.array([28, 33, 38]), np.array([50, 58, 65])
        
    fol_c = np.where(lum[:,:,None] < 0.5, 
                     f_dark + (f_mid - f_dark) * (lum[:,:,None] / 0.5),
                     f_mid + (f_bright - f_mid) * ((lum[:,:,None] - 0.5) / 0.5))
    trk_c = np.where(lum[:,:,None] < 0.5,
                     t_dark + (t_mid - t_dark) * (lum[:,:,None] / 0.5),
                     t_mid + (t_bright - t_mid) * ((lum[:,:,None] - 0.5) / 0.5))
    out[:, :, :3] = np.clip(np.where(is_fol[:,:,None], fol_c, trk_c), 0, 255)
    return Image.fromarray(out.astype(np.uint8))

def remap_dead_tree(im, is_night=False, target_size=None):
    if target_size:
        im = im.resize(target_size, Image.Resampling.NEAREST)
    arr = np.array(im).astype(float)
    alpha = arr[:, :, 3]
    rgb = arr[:, :, :3]
    lum = (0.299 * rgb[:,:,0] + 0.587 * rgb[:,:,1] + 0.114 * rgb[:,:,2]) / 255.0
    out = np.zeros_like(arr)
    out[:, :, 3] = alpha
    if not is_night:
        t_dark, t_mid, t_bright = np.array([22, 16, 12]), np.array([68, 48, 30]), np.array([115, 85, 52])
    else:
        t_dark, t_mid, t_bright = np.array([12, 14, 16]), np.array([32, 38, 44]), np.array([62, 75, 84])
    c = np.where(lum[:,:,None] < 0.5,
                 t_dark + (t_mid - t_dark) * (lum[:,:,None] / 0.5),
                 t_mid + (t_bright - t_mid) * ((lum[:,:,None] - 0.5) / 0.5))
    out[:, :, :3] = np.clip(c, 0, 255)
    return Image.fromarray(out.astype(np.uint8))

# 1. Large Oak (cropped from treepack 23, 18 to 290, 300)
oak_lg = treepack.crop((23, 18, 290, 300))
remap_foliage_tree(oak_lg, False, (140, 150)).save('assets/sprites/environment/tree_oak_large_day.png')
remap_foliage_tree(oak_lg, True, (140, 150)).save('assets/sprites/environment/tree_oak_large_night.png')

# 2. Medium Oak (cropped from treepack 330, 0 to 490, 180)
oak_md = treepack.crop((330, 0, 490, 180))
remap_foliage_tree(oak_md, False, (100, 112)).save('assets/sprites/environment/tree_oak_med_day.png')
remap_foliage_tree(oak_md, True, (100, 112)).save('assets/sprites/environment/tree_oak_med_night.png')

# 3. Pine Tree (cropped from treepack 7, 340 to 80, 500)
pine = treepack.crop((7, 340, 80, 500))
remap_foliage_tree(pine, False, (64, 140)).save('assets/sprites/environment/tree_pine_day.png')
remap_foliage_tree(pine, True, (64, 140)).save('assets/sprites/environment/tree_pine_night.png')

# 4. Dead Tree (from pixeltroid)
remap_dead_tree(dead_src, False, (96, 116)).save('assets/sprites/environment/tree_dead_day.png')
remap_dead_tree(dead_src, True, (96, 116)).save('assets/sprites/environment/tree_dead_night.png')

# 5. Tree Stump (from treepack stump region 530, 0 to 600, 70)
stump = treepack.crop((530, 0, 600, 70))
remap_foliage_tree(stump, False, (48, 48)).save('assets/sprites/environment/stump_day.png')
remap_foliage_tree(stump, True, (48, 48)).save('assets/sprites/environment/stump_night.png')

print('All Metal Slug style assets generated successfully!')
