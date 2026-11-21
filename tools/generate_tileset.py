#!/usr/bin/env python3
"""
Pixel Art Tileset & Map Assets Generator for FACTORY RESET.
Generates:
1. arena_tileset_day.png (256x256, 8x8 tiles of 32x32)
2. arena_tileset_night.png (256x256, 8x8 tiles of 32x32)
3. Individual slice PNGs in assets/sprites/environment/tileset_day/ & tileset_night/
4. Multi-tile landmark props:
   - turret_mount_pad_day.png / _night.png (64x64)
   - aegis_landing_pad_day.png / _night.png (64x64)
   - scrap_depot_zone_day.png / _night.png (64x64)
   - central_tower_bay_day.png / _night.png (128x128 - empty center mounting bay)
"""

import os
import math
from PIL import Image, ImageDraw

TILE_SIZE = 32
GRID_COLS = 8
GRID_ROWS = 8
SHEET_W = GRID_COLS * TILE_SIZE  # 256
SHEET_H = GRID_ROWS * TILE_SIZE  # 256

# ==============================================================================
# PALETTES
# ==============================================================================
# Day: Industrial sunlit metal, warm rust, safety yellow, dark rubber cables
PAL_DAY = {
    "bg_void": (45, 52, 60, 255),
    "steel_light": (135, 145, 160, 255),
    "steel_mid": (90, 100, 115, 255),
    "steel_dark": (60, 68, 80, 255),
    "steel_shadow": (38, 44, 54, 255),
    "steel_black": (24, 28, 35, 255),
    
    "rivet_light": (180, 190, 205, 255),
    "rivet_dark": (30, 35, 45, 255),
    
    "rust_light": (185, 110, 60, 255),
    "rust_mid": (145, 75, 40, 255),
    "rust_dark": (95, 45, 25, 255),
    
    "hazard_yellow": (235, 185, 25, 255),
    "hazard_dark": (35, 38, 45, 255),
    
    "cable_jacket": (28, 32, 40, 255),
    "cable_core": (175, 95, 40, 255),
    "cable_blue": (40, 75, 110, 255),
    
    "light_off": (75, 80, 90, 255),
    "light_glow": (245, 165, 35, 255),
    "beacon": (230, 80, 40, 255),
    
    "vent_void": (20, 24, 30, 255),
    "acid_stain": (115, 150, 40, 220),
    "weld_scorch": (25, 25, 30, 240),
}

# Night: Cyberpunk dark obsidian steel, electric neon cyan, glowing amber, warning crimson
PAL_NIGHT = {
    "bg_void": (8, 10, 15, 255),
    "steel_light": (50, 65, 88, 255),
    "steel_mid": (28, 38, 55, 255),
    "steel_dark": (18, 24, 38, 255),
    "steel_shadow": (12, 16, 26, 255),
    "steel_black": (6, 8, 14, 255),
    
    "rivet_light": (90, 130, 180, 255),
    "rivet_dark": (8, 12, 20, 255),
    
    "rust_light": (90, 50, 70, 255),
    "rust_mid": (60, 30, 50, 255),
    "rust_dark": (35, 18, 30, 255),
    
    "hazard_yellow": (255, 120, 0, 255),  # glowing cyber amber neon!
    "hazard_dark": (15, 18, 28, 255),
    
    "cable_jacket": (10, 18, 30, 255),
    "cable_core": (0, 245, 255, 255),     # glowing cyan superconductor!
    "cable_blue": (0, 160, 255, 255),
    
    "light_off": (30, 45, 65, 255),
    "light_glow": (0, 245, 255, 255),    # intense cyan neon!
    "beacon": (255, 30, 70, 255),        # glowing crimson beacon!
    
    "vent_void": (5, 8, 14, 255),
    "acid_stain": (70, 180, 30, 240),    # glowing bioluminescent acid!
    "weld_scorch": (10, 15, 25, 255),
}

# ==============================================================================
# TILE DRAWING FUNCTIONS (Draws into a 32x32 RGBA Image)
# ==============================================================================

def make_tile(is_night=False):
    img = Image.new("RGBA", (TILE_SIZE, TILE_SIZE), (0, 0, 0, 0))
    pal = PAL_NIGHT if is_night else PAL_DAY
    return img, ImageDraw.Draw(img), pal

def draw_base_metal(draw, pal):
    """Fills 32x32 with a beveled metal plate, grain and 4 corner rivets."""
    # Base background
    draw.rectangle([0, 0, 31, 31], fill=pal["steel_mid"])
    # Highlight top and left
    draw.line([(0, 0), (31, 0)], fill=pal["steel_light"])
    draw.line([(0, 0), (0, 31)], fill=pal["steel_light"])
    # Shadow bottom and right
    draw.line([(0, 31), (31, 31)], fill=pal["steel_shadow"])
    draw.line([(31, 0), (31, 31)], fill=pal["steel_shadow"])
    # Inner border line
    draw.rectangle([1, 1, 30, 30], outline=pal["steel_dark"])
    
    # 4 corner rivets
    rivets = [(3, 3), (28, 3), (3, 28), (28, 28)]
    for rx, ry in rivets:
        draw.point((rx, ry), fill=pal["rivet_dark"])
        draw.point((rx, ry-1), fill=pal["rivet_light"])
        draw.point((rx-1, ry), fill=pal["rivet_light"])

# Tile 0: Steel Plate
def draw_tile_0(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw_base_metal(draw, pal)
    # Subtle metal grain
    for y in range(4, 28, 4):
        draw.line([(4, y), (27, y)], fill=pal["steel_dark"])
    return img

# Tile 1: Quad Panels (4 smaller 16x16 steel plates)
def draw_tile_1(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw_base_metal(draw, pal)
    # Cross seams
    draw.line([(15, 1), (15, 30)], fill=pal["steel_shadow"])
    draw.line([(16, 1), (16, 30)], fill=pal["steel_light"])
    draw.line([(1, 15), (30, 15)], fill=pal["steel_shadow"])
    draw.line([(1, 16), (30, 16)], fill=pal["steel_light"])
    # Extra rivets at mid intersections
    for (rx, ry) in [(13, 3), (18, 3), (13, 28), (18, 28), (3, 13), (3, 18), (28, 13), (28, 18)]:
        draw.point((rx, ry), fill=pal["rivet_dark"])
    return img

# Tile 2: Heavy Vent Grate
def draw_tile_2(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw_base_metal(draw, pal)
    # Recessed frame
    draw.rectangle([4, 4, 27, 27], fill=pal["vent_void"])
    # Grate mesh slats
    for x in range(6, 26, 3):
        draw.line([(x, 5), (x, 26)], fill=pal["steel_dark"])
        draw.line([(x+1, 5), (x+1, 26)], fill=pal["steel_light"])
    # Cross brace
    draw.line([(4, 15), (27, 15)], fill=pal["steel_shadow"])
    draw.line([(4, 16), (27, 16)], fill=pal["steel_light"])
    if is_night:
        # Subtle eerie blue glow from the deep vent
        draw.point((15, 10), fill=pal["cable_blue"])
        draw.point((16, 21), fill=pal["cable_blue"])
    return img

# Tile 3: Diamond Tread Plate
def draw_tile_3(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw_base_metal(draw, pal)
    # Diamond pattern dots
    for y in range(4, 28, 4):
        offset = 2 if (y // 4) % 2 == 1 else 0
        for x in range(4 + offset, 28, 4):
            draw.point((x, y-1), fill=pal["steel_light"])
            draw.point((x, y), fill=pal["steel_light"])
            draw.point((x+1, y), fill=pal["steel_shadow"])
            draw.point((x, y+1), fill=pal["steel_shadow"])
    return img

# Tile 4: Hexagonal Plate
def draw_tile_4(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw_base_metal(draw, pal)
    # Hex outline in center
    hex_pts = [(16, 6), (24, 11), (24, 21), (16, 26), (8, 21), (8, 11)]
    draw.polygon(hex_pts, outline=pal["steel_dark"], fill=pal["steel_mid"])
    draw.polygon([(16, 8), (22, 12), (22, 20), (16, 24), (10, 20), (10, 12)], outline=pal["steel_light"])
    if is_night:
        # Center hex node glows cyan
        draw.point((16, 16), fill=pal["light_glow"])
        draw.point((15, 16), fill=pal["cable_core"])
        draw.point((17, 16), fill=pal["cable_core"])
    return img

# Tile 5: Corrugated Metal
def draw_tile_5(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw_base_metal(draw, pal)
    for y in range(4, 28, 3):
        draw.line([(2, y), (29, y)], fill=pal["steel_light"])
        draw.line([(2, y+1), (29, y+1)], fill=pal["steel_mid"])
        draw.line([(2, y+2), (29, y+2)], fill=pal["steel_shadow"])
    return img

# Tile 6: Rusted / Pitted Plate
def draw_tile_6(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw_base_metal(draw, pal)
    # Rust patches
    rust_boxes = [
        (6, 6, 14, 15),
        (18, 14, 26, 24),
        (12, 18, 17, 26),
    ]
    for (x1, y1, x2, y2) in rust_boxes:
        draw.rectangle([x1, y1, x2, y2], fill=pal["rust_dark"])
        draw.rectangle([x1+1, y1+1, x2-1, y2-1], fill=pal["rust_mid"])
        draw.point((x1+2, y1+2), fill=pal["rust_light"])
    return img

# Tile 7: Scratched / Impact Battle Plate
def draw_tile_7(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw_base_metal(draw, pal)
    # Scratches (claw marks from crawler)
    draw.line([(6, 8), (20, 22)], fill=pal["steel_black"])
    draw.line([(7, 8), (21, 22)], fill=pal["steel_light"])
    draw.line([(10, 6), (24, 20)], fill=pal["steel_black"])
    draw.line([(11, 6), (25, 20)], fill=pal["steel_light"])
    draw.line([(14, 4), (28, 18)], fill=pal["steel_black"])
    draw.line([(15, 4), (29, 18)], fill=pal["steel_light"])
    # Blast mark
    draw.ellipse([8, 18, 16, 26], fill=pal["weld_scorch"])
    return img

# ------------------------------------------------------------------------------
# Row 1: Cables & Energy Conduits
# ------------------------------------------------------------------------------

# Tile 8 (0,1): Conduit Horizontal
def draw_tile_8(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw_base_metal(draw, pal)
    # Channel trench
    draw.rectangle([0, 11, 31, 20], fill=pal["steel_black"])
    draw.line([(0, 10), (31, 10)], fill=pal["steel_shadow"])
    draw.line([(0, 21), (31, 21)], fill=pal["steel_light"])
    # Conduits
    draw.line([(0, 13), (31, 13)], fill=pal["cable_jacket"])
    draw.line([(0, 14), (31, 14)], fill=pal["cable_core"])
    draw.line([(0, 15), (31, 15)], fill=pal["cable_jacket"])
    draw.line([(0, 17), (31, 17)], fill=pal["cable_blue"])
    draw.line([(0, 18), (31, 18)], fill=pal["cable_jacket"])
    if is_night:
        # High intensity core highlight
        draw.line([(0, 14), (31, 14)], fill=(220, 255, 255, 255))
        draw.line([(0, 17), (31, 17)], fill=pal["cable_core"])
    return img

# Tile 9 (1,1): Conduit Vertical
def draw_tile_9(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw_base_metal(draw, pal)
    # Channel trench
    draw.rectangle([11, 0, 20, 31], fill=pal["steel_black"])
    draw.line([(10, 0), (10, 31)], fill=pal["steel_shadow"])
    draw.line([(21, 0), (21, 31)], fill=pal["steel_light"])
    # Conduits
    draw.line([(13, 0), (13, 31)], fill=pal["cable_jacket"])
    draw.line([(14, 0), (14, 31)], fill=pal["cable_core"])
    draw.line([(15, 0), (15, 31)], fill=pal["cable_jacket"])
    draw.line([(17, 0), (17, 31)], fill=pal["cable_blue"])
    draw.line([(18, 0), (18, 31)], fill=pal["cable_jacket"])
    if is_night:
        draw.line([(14, 0), (14, 31)], fill=(220, 255, 255, 255))
        draw.line([(17, 0), (17, 31)], fill=pal["cable_core"])
    return img

# Tile 10 (2,1): Conduit T-Junction (Down)
def draw_tile_10(is_night=False):
    img = draw_tile_8(is_night)
    draw = ImageDraw.Draw(img)
    pal = PAL_NIGHT if is_night else PAL_DAY
    # Cut trench downward from center
    draw.rectangle([11, 15, 20, 31], fill=pal["steel_black"])
    draw.line([(10, 20), (10, 31)], fill=pal["steel_shadow"])
    draw.line([(21, 20), (21, 31)], fill=pal["steel_light"])
    draw.line([(14, 15), (14, 31)], fill=pal["cable_core"])
    draw.line([(17, 15), (17, 31)], fill=pal["cable_blue"])
    if is_night:
        draw.line([(14, 15), (14, 31)], fill=(220, 255, 255, 255))
        draw.point((14, 14), fill=(255, 255, 255, 255))
    return img

# Tile 11 (3,1): Conduit 4-Way Cross
def draw_tile_11(is_night=False):
    img = draw_tile_8(is_night)
    draw = ImageDraw.Draw(img)
    pal = PAL_NIGHT if is_night else PAL_DAY
    # Cut vertical trench through
    draw.rectangle([11, 0, 20, 31], fill=pal["steel_black"])
    draw.line([(0, 14), (31, 14)], fill=pal["cable_core"])
    draw.line([(14, 0), (14, 31)], fill=pal["cable_core"])
    if is_night:
        draw.line([(0, 14), (31, 14)], fill=(220, 255, 255, 255))
        draw.line([(14, 0), (14, 31)], fill=(220, 255, 255, 255))
        draw.rectangle([13, 13, 15, 15], fill=(255, 255, 255, 255))
    return img

# Tile 12 (4,1): Conduit Corner (Top to Left)
def draw_tile_12(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw_base_metal(draw, pal)
    draw.rectangle([11, 0, 20, 20], fill=pal["steel_black"])
    draw.rectangle([0, 11, 20, 20], fill=pal["steel_black"])
    draw.line([(14, 0), (14, 14)], fill=pal["cable_core"])
    draw.line([(0, 14), (14, 14)], fill=pal["cable_core"])
    if is_night:
        draw.line([(14, 0), (14, 14)], fill=(220, 255, 255, 255))
        draw.line([(0, 14), (14, 14)], fill=(220, 255, 255, 255))
    return img

# Tile 13 (5,1): Conduit Corner (Top to Right)
def draw_tile_13(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw_base_metal(draw, pal)
    draw.rectangle([11, 0, 20, 20], fill=pal["steel_black"])
    draw.rectangle([11, 11, 31, 20], fill=pal["steel_black"])
    draw.line([(14, 0), (14, 14)], fill=pal["cable_core"])
    draw.line([(14, 14), (31, 14)], fill=pal["cable_core"])
    if is_night:
        draw.line([(14, 0), (14, 14)], fill=(220, 255, 255, 255))
        draw.line([(14, 14), (31, 14)], fill=(220, 255, 255, 255))
    return img

# Tile 14 (6,1): Junction Node Box
def draw_tile_14(is_night=False):
    img = draw_tile_8(is_night)
    draw = ImageDraw.Draw(img)
    pal = PAL_NIGHT if is_night else PAL_DAY
    # Raised steel junction box in center
    draw.rectangle([9, 9, 22, 22], fill=pal["steel_dark"], outline=pal["steel_light"])
    draw.rectangle([11, 11, 20, 20], fill=pal["steel_shadow"])
    # Status LED
    draw.rectangle([13, 13, 18, 18], fill=pal["light_glow"])
    if is_night:
        draw.rectangle([14, 14, 17, 17], fill=(255, 255, 255, 255))
    return img

# Tile 15 (7,1): Conduit Terminus / High-Voltage Cap
def draw_tile_15(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw_base_metal(draw, pal)
    # Conduit entering from left and terminating into heavy capacitor block
    draw.rectangle([0, 11, 16, 20], fill=pal["steel_black"])
    draw.line([(0, 14), (16, 14)], fill=pal["cable_core"])
    # Cap block
    draw.rectangle([16, 8, 26, 23], fill=pal["steel_dark"], outline=pal["steel_light"])
    # Warning lightning bolt / spark indicator
    draw.line([(21, 11), (19, 15)], fill=pal["hazard_yellow"])
    draw.line([(19, 15), (23, 15)], fill=pal["hazard_yellow"])
    draw.line([(23, 15), (20, 20)], fill=pal["hazard_yellow"])
    return img

# ------------------------------------------------------------------------------
# Row 2: Hazard Caution Borders
# ------------------------------------------------------------------------------

def draw_hazard_stripes(draw, pal, box, orientation="horizontal"):
    x1, y1, x2, y2 = box
    draw.rectangle([x1, y1, x2, y2], fill=pal["hazard_dark"])
    step = 6
    if orientation == "horizontal":
        for x in range(x1 - 10, x2 + 10, step):
            draw.line([(x, y2), (x + (y2 - y1), y1)], fill=pal["hazard_yellow"], width=2)
    else:
        for y in range(y1 - 10, y2 + 10, step):
            draw.line([(x1, y), (x2, y + (x2 - x1))], fill=pal["hazard_yellow"], width=2)

# Tile 16 (0,2): Hazard Top
def draw_tile_16(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw_base_metal(draw, pal)
    draw_hazard_stripes(draw, pal, (0, 0, 31, 8), "horizontal")
    draw.line([(0, 8), (31, 8)], fill=pal["steel_shadow"])
    return img

# Tile 17 (1,2): Hazard Bottom
def draw_tile_17(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw_base_metal(draw, pal)
    draw_hazard_stripes(draw, pal, (0, 23, 31, 31), "horizontal")
    draw.line([(0, 22), (31, 22)], fill=pal["steel_light"])
    return img

# Tile 18 (2,2): Hazard Left
def draw_tile_18(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw_base_metal(draw, pal)
    draw_hazard_stripes(draw, pal, (0, 0, 8, 31), "vertical")
    draw.line([(8, 0), (8, 31)], fill=pal["steel_shadow"])
    return img

# Tile 19 (3,2): Hazard Right
def draw_tile_19(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw_base_metal(draw, pal)
    draw_hazard_stripes(draw, pal, (23, 0, 31, 31), "vertical")
    draw.line([(22, 0), (22, 31)], fill=pal["steel_light"])
    return img

# Tile 20 (4,2): Hazard Corner TL
def draw_tile_20(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw_base_metal(draw, pal)
    draw_hazard_stripes(draw, pal, (0, 0, 31, 8), "horizontal")
    draw_hazard_stripes(draw, pal, (0, 0, 8, 31), "vertical")
    return img

# Tile 21 (5,2): Hazard Corner TR
def draw_tile_21(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw_base_metal(draw, pal)
    draw_hazard_stripes(draw, pal, (0, 0, 31, 8), "horizontal")
    draw_hazard_stripes(draw, pal, (23, 0, 31, 31), "vertical")
    return img

# Tile 22 (6,2): Hazard Corner BL
def draw_tile_22(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw_base_metal(draw, pal)
    draw_hazard_stripes(draw, pal, (0, 23, 31, 31), "horizontal")
    draw_hazard_stripes(draw, pal, (0, 0, 8, 31), "vertical")
    return img

# Tile 23 (7,2): Hazard Corner BR
def draw_tile_23(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw_base_metal(draw, pal)
    draw_hazard_stripes(draw, pal, (0, 23, 31, 31), "horizontal")
    draw_hazard_stripes(draw, pal, (23, 0, 31, 31), "vertical")
    return img

# ------------------------------------------------------------------------------
# Row 3: Platform Outer Railings & Rooftop Edges
# ------------------------------------------------------------------------------

# Tile 24 (0,3): Top Railing
def draw_tile_24(is_night=False):
    img, draw, pal = make_tile(is_night)
    # Outside is abyss / sky
    draw.rectangle([0, 0, 31, 11], fill=pal["bg_void"])
    # Metal deck platform starts at y=12
    draw.rectangle([0, 12, 31, 31], fill=pal["steel_mid"])
    draw.line([(0, 12), (31, 12)], fill=pal["steel_light"])
    # Stanchions (vertical posts)
    for px in [3, 15, 27]:
        draw.rectangle([px, 3, px+2, 13], fill=pal["steel_dark"], outline=pal["steel_light"])
    # Top handrail pipe
    draw.line([(0, 3), (31, 3)], fill=pal["steel_light"], width=2)
    # Mid safety rail
    draw.line([(0, 7), (31, 7)], fill=pal["steel_dark"])
    return img

# Tile 25 (1,3): Bottom Edge Lip (dropping into chasm)
def draw_tile_25(is_night=False):
    img, draw, pal = make_tile(is_night)
    # Top half is metal deck
    draw.rectangle([0, 0, 31, 19], fill=pal["steel_mid"])
    # Heavy curb edge
    draw.rectangle([0, 20, 31, 24], fill=pal["steel_dark"])
    draw.line([(0, 20), (31, 20)], fill=pal["steel_light"])
    # Drop-off face
    draw.rectangle([0, 25, 31, 28], fill=pal["steel_black"])
    # Abyss
    draw.rectangle([0, 29, 31, 31], fill=pal["bg_void"])
    # Edge safety reflectors
    for rx in [5, 15, 25]:
        draw.point((rx, 22), fill=pal["light_glow"])
    return img

# Tile 26 (2,3): Left Railing
def draw_tile_26(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw.rectangle([0, 0, 11, 31], fill=pal["bg_void"])
    draw.rectangle([12, 0, 31, 31], fill=pal["steel_mid"])
    draw.line([(12, 0), (12, 31)], fill=pal["steel_light"])
    # Vertical rail
    draw.line([(3, 0), (3, 31)], fill=pal["steel_light"], width=2)
    draw.line([(7, 0), (7, 31)], fill=pal["steel_dark"])
    # Stanchion brackets
    for py in [4, 16, 28]:
        draw.rectangle([3, py, 13, py+2], fill=pal["steel_dark"])
    return img

# Tile 27 (3,3): Right Railing
def draw_tile_27(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw.rectangle([20, 0, 31, 31], fill=pal["bg_void"])
    draw.rectangle([0, 0, 19, 31], fill=pal["steel_mid"])
    draw.line([(19, 0), (19, 31)], fill=pal["steel_shadow"])
    # Vertical rail
    draw.line([(28, 0), (28, 31)], fill=pal["steel_light"], width=2)
    draw.line([(24, 0), (24, 31)], fill=pal["steel_dark"])
    for py in [4, 16, 28]:
        draw.rectangle([18, py, 28, py+2], fill=pal["steel_dark"])
    return img

# Tile 28 (4,3): Corner Post TL with Warning Beacon
def draw_tile_28(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw.rectangle([0, 0, 31, 31], fill=pal["bg_void"])
    draw.rectangle([12, 12, 31, 31], fill=pal["steel_mid"])
    # Post base
    draw.rectangle([4, 4, 16, 16], fill=pal["steel_dark"], outline=pal["steel_light"])
    # Beacon light
    draw.ellipse([7, 7, 13, 13], fill=pal["beacon"])
    if is_night:
        draw.point((10, 10), fill=(255, 255, 255, 255))
        # Neon beacon glow ring
        draw.ellipse([5, 5, 15, 15], outline=pal["beacon"])
    return img

# Tile 29 (5,3): Corner Post TR
def draw_tile_29(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw.rectangle([0, 0, 31, 31], fill=pal["bg_void"])
    draw.rectangle([0, 12, 19, 31], fill=pal["steel_mid"])
    draw.rectangle([15, 4, 27, 16], fill=pal["steel_dark"], outline=pal["steel_light"])
    draw.ellipse([18, 7, 24, 13], fill=pal["beacon"])
    if is_night:
        draw.point((21, 10), fill=(255, 255, 255, 255))
        draw.ellipse([16, 5, 26, 15], outline=pal["beacon"])
    return img

# Tile 30 (6,3): Corner Post BL
def draw_tile_30(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw.rectangle([0, 0, 31, 31], fill=pal["bg_void"])
    draw.rectangle([12, 0, 31, 19], fill=pal["steel_mid"])
    draw.rectangle([4, 15, 16, 27], fill=pal["steel_dark"], outline=pal["steel_light"])
    draw.ellipse([7, 18, 13, 24], fill=pal["beacon"])
    if is_night:
        draw.point((10, 21), fill=(255, 255, 255, 255))
        draw.ellipse([5, 16, 15, 26], outline=pal["beacon"])
    return img

# Tile 31 (7,3): Corner Post BR
def draw_tile_31(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw.rectangle([0, 0, 31, 31], fill=pal["bg_void"])
    draw.rectangle([0, 0, 19, 19], fill=pal["steel_mid"])
    draw.rectangle([15, 15, 27, 27], fill=pal["steel_dark"], outline=pal["steel_light"])
    draw.ellipse([18, 18, 24, 24], fill=pal["beacon"])
    if is_night:
        draw.point((21, 21), fill=(255, 255, 255, 255))
        draw.ellipse([16, 16, 26, 26], outline=pal["beacon"])
    return img

# ------------------------------------------------------------------------------
# Row 4: Ingress Breaches & Hardpoints
# ------------------------------------------------------------------------------

# Tile 32 (0,4): North Breach (Left bent rail)
def draw_tile_32(is_night=False):
    img = draw_tile_24(is_night)
    draw = ImageDraw.Draw(img)
    pal = PAL_NIGHT if is_night else PAL_DAY
    # Bent snapped metal rail
    draw.line([(15, 3), (25, 11)], fill=pal["steel_light"], width=2)
    draw.line([(15, 7), (28, 12)], fill=pal["steel_dark"])
    # Slime claw scratch
    draw.line([(18, 12), (28, 22)], fill=pal["acid_stain"], width=2)
    return img

# Tile 33 (1,4): North Breach (Center open gap)
def draw_tile_33(is_night=False):
    img, draw, pal = make_tile(is_night)
    # Open void where railing was torn down
    draw.rectangle([0, 0, 31, 13], fill=pal["bg_void"])
    draw.rectangle([0, 14, 31, 31], fill=pal["steel_mid"])
    # Jagged torn metal edge
    for x in range(0, 32, 4):
        draw.polygon([(x, 14), (x+2, 11), (x+4, 14)], fill=pal["steel_light"])
    # Nanobots claw scratches and acid drips
    draw.line([(6, 15), (6, 26)], fill=pal["acid_stain"])
    draw.line([(16, 15), (14, 28)], fill=pal["acid_stain"], width=2)
    draw.line([(24, 15), (26, 24)], fill=pal["acid_stain"])
    return img

# Tile 34 (2,4): North Breach (Right bent rail)
def draw_tile_34(is_night=False):
    img = draw_tile_24(is_night)
    draw = ImageDraw.Draw(img)
    pal = PAL_NIGHT if is_night else PAL_DAY
    draw.line([(5, 11), (15, 3)], fill=pal["steel_light"], width=2)
    draw.line([(3, 12), (15, 7)], fill=pal["steel_dark"])
    draw.line([(4, 22), (14, 12)], fill=pal["acid_stain"], width=2)
    return img

# Tile 35 (3,4): South Cable Lift Breach (Left door)
def draw_tile_35(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw.rectangle([0, 0, 31, 20], fill=pal["steel_mid"])
    # Elevator frame & dark shaft pit
    draw.rectangle([6, 20, 31, 31], fill=pal["steel_black"])
    draw.rectangle([0, 16, 6, 31], fill=pal["steel_dark"], outline=pal["steel_light"])
    # Heavy cables dangling into pit
    draw.line([(12, 10), (12, 31)], fill=pal["cable_jacket"], width=2)
    draw.line([(20, 5), (20, 31)], fill=pal["cable_core"])
    return img

# Tile 36 (4,4): South Cable Lift Breach (Right door)
def draw_tile_36(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw.rectangle([0, 0, 31, 20], fill=pal["steel_mid"])
    draw.rectangle([0, 20, 25, 31], fill=pal["steel_black"])
    draw.rectangle([25, 16, 31, 31], fill=pal["steel_dark"], outline=pal["steel_light"])
    draw.line([(10, 5), (10, 31)], fill=pal["cable_core"])
    draw.line([(18, 10), (18, 31)], fill=pal["cable_jacket"], width=2)
    return img

# Tile 37 (5,4): Turret Mounting Hardpoint Tile
def draw_tile_37(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw_base_metal(draw, pal)
    # Heavy circular locking ring
    draw.ellipse([4, 4, 27, 27], outline=pal["steel_dark"], fill=pal["steel_black"])
    draw.ellipse([7, 7, 24, 24], outline=pal["steel_light"], fill=pal["steel_mid"])
    # Center locking port
    draw.ellipse([12, 12, 19, 19], fill=pal["steel_black"])
    # 4 Bolt anchors (cardinal)
    for bx, by in [(15, 5), (15, 25), (5, 15), (25, 15)]:
        draw.point((bx, by), fill=pal["light_glow"])
        draw.point((bx+1, by), fill=pal["light_glow"])
    if is_night:
        # High-tech glowing neon cyan targeting circle!
        draw.ellipse([6, 6, 25, 25], outline=pal["cable_core"])
        draw.line([(15, 0), (15, 31)], fill=pal["cable_blue"])
        draw.line([(0, 15), (31, 15)], fill=pal["cable_blue"])
        draw.point((15, 15), fill=(255, 255, 255, 255))
    return img

# Tile 38 (6,4): Scrap Deposit Zone Marker
def draw_tile_38(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw_base_metal(draw, pal)
    # Yellow floor stencil markings
    # Box frame with corner brackets
    col = pal["hazard_yellow"]
    draw.line([(4, 4), (12, 4)], fill=col, width=2)
    draw.line([(4, 4), (4, 12)], fill=col, width=2)
    draw.line([(27, 4), (19, 4)], fill=col, width=2)
    draw.line([(27, 4), (27, 12)], fill=col, width=2)
    draw.line([(4, 27), (12, 27)], fill=col, width=2)
    draw.line([(4, 27), (4, 19)], fill=col, width=2)
    draw.line([(27, 27), (19, 27)], fill=col, width=2)
    draw.line([(27, 27), (27, 19)], fill=col, width=2)
    # Stencil "S" in center
    draw.line([(13, 11), (18, 11)], fill=col)
    draw.line([(13, 11), (13, 15)], fill=col)
    draw.line([(13, 15), (18, 15)], fill=col)
    draw.line([(18, 15), (18, 20)], fill=col)
    draw.line([(13, 20), (18, 20)], fill=col)
    return img

# Tile 39 (7,4): AEGIS Drone Landing Pad Marker
def draw_tile_39(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw_base_metal(draw, pal)
    col = pal["cable_core"] if is_night else pal["hazard_yellow"]
    # Outer circle
    draw.ellipse([4, 4, 27, 27], outline=col, width=2)
    # Center "H" mark (Helipad / Drone landing)
    draw.line([(11, 10), (11, 21)], fill=col, width=2)
    draw.line([(20, 10), (20, 21)], fill=col, width=2)
    draw.line([(11, 15), (20, 15)], fill=col, width=2)
    if is_night:
        # Runway indicator dots
        for px, py in [(15, 2), (15, 29), (2, 15), (29, 15)]:
            draw.point((px, py), fill=(255, 255, 255, 255))
    return img

# ------------------------------------------------------------------------------
# Row 5: Central Tower Foundation (Empty Center - as explicitly requested!)
# ------------------------------------------------------------------------------

# Tile 40 (0,5): Tower Base Top-Left Corner
def draw_tile_40(is_night=False):
    img, draw, pal = make_tile(is_night)
    # Outside is standard floor
    draw.rectangle([0, 0, 31, 31], fill=pal["steel_mid"])
    # Recessed trench starting inside
    draw.rectangle([12, 12, 31, 31], fill=pal["steel_black"])
    # Heavy beveled rim
    draw.line([(12, 12), (31, 12)], fill=pal["steel_shadow"], width=2)
    draw.line([(12, 12), (12, 31)], fill=pal["steel_shadow"], width=2)
    # Corner heavy hydraulic anchor bolt
    draw.rectangle([6, 6, 14, 14], fill=pal["steel_dark"], outline=pal["steel_light"])
    draw.ellipse([8, 8, 12, 12], fill=pal["light_glow"])
    if is_night:
        # Cyan conduit line running towards the empty center
        draw.line([(14, 14), (31, 31)], fill=pal["cable_core"])
    return img

# Tile 41 (1,5): Tower Base Top Border
def draw_tile_41(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw.rectangle([0, 0, 31, 11], fill=pal["steel_mid"])
    draw.line([(0, 11), (31, 11)], fill=pal["steel_light"])
    # Recessed bay floor
    draw.rectangle([0, 12, 31, 31], fill=pal["steel_black"])
    draw.line([(0, 12), (31, 12)], fill=pal["steel_shadow"], width=2)
    # Umbilical cable socket
    draw.rectangle([11, 4, 20, 11], fill=pal["steel_dark"], outline=pal["steel_light"])
    draw.line([(15, 12), (15, 31)], fill=pal["cable_core"] if is_night else pal["cable_jacket"])
    return img

# Tile 42 (2,5): Tower Base Top-Right Corner
def draw_tile_42(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw.rectangle([0, 0, 31, 31], fill=pal["steel_mid"])
    draw.rectangle([0, 12, 19, 31], fill=pal["steel_black"])
    draw.line([(0, 12), (19, 12)], fill=pal["steel_shadow"], width=2)
    draw.line([(19, 12), (19, 31)], fill=pal["steel_shadow"], width=2)
    draw.rectangle([17, 6, 25, 14], fill=pal["steel_dark"], outline=pal["steel_light"])
    draw.ellipse([19, 8, 23, 12], fill=pal["light_glow"])
    if is_night:
        draw.line([(17, 14), (0, 31)], fill=pal["cable_core"])
    return img

# Tile 43 (3,5): Tower Base Left Border
def draw_tile_43(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw.rectangle([0, 0, 11, 31], fill=pal["steel_mid"])
    draw.line([(11, 0), (11, 31)], fill=pal["steel_light"])
    draw.rectangle([12, 0, 31, 31], fill=pal["steel_black"])
    draw.line([(12, 0), (12, 31)], fill=pal["steel_shadow"], width=2)
    # Cable conduit
    draw.line([(12, 15), (31, 15)], fill=pal["cable_core"] if is_night else pal["cable_jacket"])
    return img

# Tile 44 (4,5): Tower Base Interior Pit (Empty Ground - waiting for tower!)
def draw_tile_44(is_night=False):
    img, draw, pal = make_tile(is_night)
    # Deep recessed titanium foundation plate
    draw.rectangle([0, 0, 31, 31], fill=pal["steel_black"])
    # Floor reinforcement grid
    draw.line([(0, 0), (31, 0)], fill=pal["steel_shadow"])
    draw.line([(0, 31), (31, 31)], fill=pal["steel_shadow"])
    draw.line([(0, 0), (0, 31)], fill=pal["steel_shadow"])
    draw.line([(31, 0), (31, 31)], fill=pal["steel_shadow"])
    # Center mounting anchor cross
    draw.line([(15, 8), (15, 23)], fill=pal["steel_dark"])
    draw.line([(8, 15), (23, 15)], fill=pal["steel_dark"])
    # 4 Center guide bolts
    for gx, gy in [(10, 10), (21, 10), (10, 21), (21, 21)]:
        draw.point((gx, gy), fill=pal["steel_light"])
    if is_night:
        # Guide laser alignment dots shining into the empty pit
        draw.point((15, 15), fill=pal["cable_core"])
        draw.line([(14, 15), (16, 15)], fill=(255, 255, 255, 255))
        draw.line([(15, 14), (15, 16)], fill=(255, 255, 255, 255))
    return img

# Tile 45 (5,5): Tower Base Right Border
def draw_tile_45(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw.rectangle([20, 0, 31, 31], fill=pal["steel_mid"])
    draw.line([(20, 0), (20, 31)], fill=pal["steel_shadow"])
    draw.rectangle([0, 0, 19, 31], fill=pal["steel_black"])
    draw.line([(19, 0), (19, 31)], fill=pal["steel_shadow"], width=2)
    draw.line([(0, 15), (19, 15)], fill=pal["cable_core"] if is_night else pal["cable_jacket"])
    return img

# Tile 46 (6,5): Tower Base Bottom-Left Corner
def draw_tile_46(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw.rectangle([0, 0, 31, 31], fill=pal["steel_mid"])
    draw.rectangle([12, 0, 31, 19], fill=pal["steel_black"])
    draw.line([(12, 0), (12, 19)], fill=pal["steel_shadow"], width=2)
    draw.line([(12, 19), (31, 19)], fill=pal["steel_shadow"], width=2)
    draw.rectangle([6, 17, 14, 25], fill=pal["steel_dark"], outline=pal["steel_light"])
    draw.ellipse([8, 19, 12, 23], fill=pal["light_glow"])
    if is_night:
        draw.line([(14, 17), (31, 0)], fill=pal["cable_core"])
    return img

# Tile 47 (7,5): Tower Base Bottom-Right Corner
def draw_tile_47(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw.rectangle([0, 0, 31, 31], fill=pal["steel_mid"])
    draw.rectangle([0, 0, 19, 19], fill=pal["steel_black"])
    draw.line([(0, 19), (19, 19)], fill=pal["steel_shadow"], width=2)
    draw.line([(19, 0), (19, 19)], fill=pal["steel_shadow"], width=2)
    draw.rectangle([17, 17, 25, 25], fill=pal["steel_dark"], outline=pal["steel_light"])
    draw.ellipse([19, 19, 23, 23], fill=pal["light_glow"])
    if is_night:
        draw.line([(17, 17), (0, 0)], fill=pal["cable_core"])
    return img

# ------------------------------------------------------------------------------
# Row 6: Architectural & Environmental Details
# ------------------------------------------------------------------------------

# Tile 48 (0,6): Void Smog Edge
def draw_tile_48(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw.rectangle([0, 0, 31, 31], fill=pal["bg_void"])
    # Smog swirls
    for y in range(2, 30, 6):
        col = (20, 25, 35, 180) if is_night else (70, 80, 75, 180)
        draw.line([(2, y), (29, y+2)], fill=col, width=2)
    return img

# Tile 49 (1,6): Acid Puddle on Steel
def draw_tile_49(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw_base_metal(draw, pal)
    # Corrosive acid stain
    draw.ellipse([6, 7, 25, 23], fill=pal["acid_stain"])
    draw.ellipse([10, 10, 21, 20], fill=pal["acid_stain"])
    # Bubbles
    draw.point((12, 13), fill=(220, 255, 100, 255))
    draw.point((18, 16), fill=(220, 255, 100, 255))
    return img

# Tile 50 (2,6): Welding Scorches
def draw_tile_50(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw_base_metal(draw, pal)
    # Solder seam line with heat tinting
    draw.line([(4, 15), (27, 15)], fill=pal["weld_scorch"], width=3)
    draw.line([(4, 15), (27, 15)], fill=(120, 80, 180, 200)) # blue-purple heat anneal
    draw.line([(4, 16), (27, 16)], fill=(220, 140, 50, 220)) # copper oxide
    return img

# Tile 51 (3,6): Recessed Floor Floodlight
def draw_tile_51(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw_base_metal(draw, pal)
    # Heavy rectangular glass fixture
    draw.rectangle([8, 8, 23, 23], fill=pal["steel_black"], outline=pal["steel_light"])
    if not is_night:
        draw.rectangle([10, 10, 21, 21], fill=(160, 180, 195, 255))
        draw.line([(10, 10), (21, 21)], fill=(220, 240, 255, 255))
    else:
        # High power upward floodlight!
        draw.rectangle([10, 10, 21, 21], fill=(220, 255, 255, 255))
        draw.rectangle([8, 8, 23, 23], outline=pal["cable_core"])
        # Light halo rays
        draw.line([(4, 15), (27, 15)], fill=(0, 245, 255, 100))
        draw.line([(15, 4), (15, 27)], fill=(0, 245, 255, 100))
    return img

# Tile 52 (4,6): Cable Trench Grate
def draw_tile_52(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw_base_metal(draw, pal)
    # Deep trench with cables visible through grate
    draw.rectangle([4, 0, 27, 31], fill=pal["steel_black"])
    draw.line([(12, 0), (12, 31)], fill=pal["cable_core"])
    draw.line([(19, 0), (19, 31)], fill=pal["cable_blue"])
    # Grate slats over cables
    for y in range(2, 31, 4):
        draw.line([(4, y), (27, y)], fill=pal["steel_dark"])
        draw.line([(4, y+1), (27, y+1)], fill=pal["steel_light"])
    return img

# Tile 53 (5,6): Diagonal Warning Caution Strip
def draw_tile_53(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw_base_metal(draw, pal)
    # Full tile diagonal hazard
    draw_hazard_stripes(draw, pal, (0, 0, 31, 31), "horizontal")
    return img

# Tile 54 (6,6): Deck Access Hatch (Circular)
def draw_tile_54(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw_base_metal(draw, pal)
    draw.ellipse([4, 4, 27, 27], fill=pal["steel_dark"], outline=pal["steel_light"])
    draw.ellipse([7, 7, 24, 24], fill=pal["steel_mid"], outline=pal["steel_shadow"])
    # Wheel spokes
    draw.line([(15, 7), (15, 24)], fill=pal["steel_light"], width=2)
    draw.line([(7, 15), (24, 15)], fill=pal["steel_light"], width=2)
    draw.ellipse([13, 13, 17, 17], fill=pal["steel_black"])
    return img

# Tile 55 (7,6): Guy-Wire Anchor Pad
def draw_tile_55(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw_base_metal(draw, pal)
    # Triangular steel gusset anchor
    draw.polygon([(16, 4), (27, 26), (5, 26)], fill=pal["steel_dark"], outline=pal["steel_light"])
    draw.ellipse([13, 12, 19, 18], fill=pal["steel_black"])
    # Heavy braided steel cable angled up
    draw.line([(16, 15), (31, 0)], fill=pal["steel_light"], width=2)
    return img

# ------------------------------------------------------------------------------
# Row 7: Spare / Reserved Tiles
# ------------------------------------------------------------------------------
def draw_tile_empty(is_night=False):
    img, draw, pal = make_tile(is_night)
    draw_base_metal(draw, pal)
    return img

# List of all tile drawers in order 0..63
TILE_BUILDERS = [
    # Row 0: Floors
    draw_tile_0, draw_tile_1, draw_tile_2, draw_tile_3, draw_tile_4, draw_tile_5, draw_tile_6, draw_tile_7,
    # Row 1: Cables & Conduits
    draw_tile_8, draw_tile_9, draw_tile_10, draw_tile_11, draw_tile_12, draw_tile_13, draw_tile_14, draw_tile_15,
    # Row 2: Hazards
    draw_tile_16, draw_tile_17, draw_tile_18, draw_tile_19, draw_tile_20, draw_tile_21, draw_tile_22, draw_tile_23,
    # Row 3: Railings & Edges
    draw_tile_24, draw_tile_25, draw_tile_26, draw_tile_27, draw_tile_28, draw_tile_29, draw_tile_30, draw_tile_31,
    # Row 4: Breaches & Hardpoints
    draw_tile_32, draw_tile_33, draw_tile_34, draw_tile_35, draw_tile_36, draw_tile_37, draw_tile_38, draw_tile_39,
    # Row 5: Central Tower Empty Base
    draw_tile_40, draw_tile_41, draw_tile_42, draw_tile_43, draw_tile_44, draw_tile_45, draw_tile_46, draw_tile_47,
    # Row 6: Details
    draw_tile_48, draw_tile_49, draw_tile_50, draw_tile_51, draw_tile_52, draw_tile_53, draw_tile_54, draw_tile_55,
    # Row 7: Extra variations
    draw_tile_0, draw_tile_1, draw_tile_2, draw_tile_8, draw_tile_9, draw_tile_37, draw_tile_44, draw_tile_empty,
]

TILE_NAMES = [
    # Row 0
    "floor_steel_plate", "floor_quad_panels", "floor_vent_grate", "floor_diamond_tread",
    "floor_hex_plate", "floor_corrugated", "floor_rusted", "floor_scratched",
    # Row 1
    "conduit_h", "conduit_v", "conduit_t_down", "conduit_cross",
    "conduit_corner_tl", "conduit_corner_tr", "conduit_junction_node", "conduit_terminus",
    # Row 2
    "hazard_top", "hazard_bottom", "hazard_left", "hazard_right",
    "hazard_corner_tl", "hazard_corner_tr", "hazard_corner_bl", "hazard_corner_br",
    # Row 3
    "railing_top", "railing_bottom", "railing_left", "railing_right",
    "corner_beacon_tl", "corner_beacon_tr", "corner_beacon_bl", "corner_beacon_br",
    # Row 4
    "breach_north_left", "breach_north_center", "breach_north_right",
    "lift_south_left", "lift_south_right", "turret_mount_hardpoint",
    "scrap_deposit_marker", "aegis_pad_marker",
    # Row 5
    "tower_base_tl", "tower_base_top", "tower_base_tr", "tower_base_left",
    "tower_base_empty_pit", "tower_base_right", "tower_base_bl", "tower_base_br",
    # Row 6
    "void_smog_edge", "floor_acid_puddle", "floor_welding_burn", "floor_floodlight",
    "trench_grate_cables", "hazard_full_diagonal", "deck_hatch_round", "guy_wire_anchor",
    # Row 7
    "floor_steel_var2", "floor_quad_var2", "floor_vent_var2", "conduit_h_alt",
    "conduit_v_alt", "turret_mount_alt", "tower_pit_alt", "floor_plain_blank",
]

def generate_tilesets():
    base_dir = "assets/sprites/environment"
    day_slice_dir = os.path.join(base_dir, "tileset_day")
    night_slice_dir = os.path.join(base_dir, "tileset_night")
    os.makedirs(day_slice_dir, exist_ok=True)
    os.makedirs(night_slice_dir, exist_ok=True)

    for is_night in [False, True]:
        sheet = Image.new("RGBA", (SHEET_W, SHEET_H), (0, 0, 0, 0))
        tag = "night" if is_night else "day"
        slice_dir = night_slice_dir if is_night else day_slice_dir
        
        for idx, builder in enumerate(TILE_BUILDERS):
            tile_img = builder(is_night=is_night)
            col = idx % GRID_COLS
            row = idx // GRID_COLS
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            sheet.paste(tile_img, (x, y))
            
            # Save individual sliced tile
            name = TILE_NAMES[idx]
            tile_img.save(os.path.join(slice_dir, f"{name}_{tag}.png"))
        
        sheet_path = os.path.join(base_dir, f"arena_tileset_{tag}.png")
        sheet.save(sheet_path)
        print(f"Generated {sheet_path} ({SHEET_W}x{SHEET_H}) with {len(TILE_BUILDERS)} tiles.")

# ==============================================================================
# MULTI-TILE LANDMARK PROPS (64x64 and 128x128)
# ==============================================================================

def generate_turret_mount_pad():
    """64x64 Turret hardpoint pad with octagonal armor rim and locking clamps."""
    for is_night in [False, True]:
        img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        pal = PAL_NIGHT if is_night else PAL_DAY
        
        # Base platform plate
        draw.rectangle([0, 0, 63, 63], fill=pal["steel_mid"])
        draw.rectangle([2, 2, 61, 61], outline=pal["steel_light"])
        draw.rectangle([4, 4, 59, 59], outline=pal["steel_shadow"])
        
        # Octagonal outer ring
        oct_pts = [
            (18, 4), (45, 4), (59, 18), (59, 45),
            (45, 59), (18, 59), (4, 45), (4, 18)
        ]
        draw.polygon(oct_pts, fill=pal["steel_dark"], outline=pal["steel_light"])
        
        # Inner circular turntable
        draw.ellipse([10, 10, 53, 53], fill=pal["steel_black"], outline=pal["steel_light"])
        draw.ellipse([16, 16, 47, 47], fill=pal["steel_mid"], outline=pal["steel_dark"])
        draw.ellipse([24, 24, 39, 39], fill=pal["steel_black"])
        
        # 4 Heavy hydraulic locking clamps
        clamps = [
            (28, 4, 35, 14),   # Top
            (28, 49, 35, 59),  # Bottom
            (4, 28, 14, 35),   # Left
            (49, 28, 59, 35),  # Right
        ]
        for c in clamps:
            draw.rectangle(c, fill=pal["steel_light"], outline=pal["steel_black"])
            # Status diode on clamp
            draw.point((c[0]+3, c[1]+3), fill=pal["light_glow"])
            
        if is_night:
            # Illuminated cyan targeting reticle and circular power conduits
            draw.ellipse([14, 14, 49, 49], outline=pal["cable_core"], width=2)
            draw.line([(31, 8), (31, 55)], fill=pal["cable_core"])
            draw.line([(8, 31), (55, 31)], fill=pal["cable_core"])
            draw.ellipse([27, 27, 36, 36], outline=(255, 255, 255, 255))
        
        tag = "night" if is_night else "day"
        out_path = f"assets/sprites/environment/turret_mount_pad_{tag}.png"
        img.save(out_path)
        print(f"Generated {out_path} (64x64)")

def generate_aegis_landing_pad():
    """64x64 AEGIS Drone landing platform with flight beacon markings."""
    for is_night in [False, True]:
        img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        pal = PAL_NIGHT if is_night else PAL_DAY
        
        # Steel pad deck with bevel
        draw.rectangle([0, 0, 63, 63], fill=pal["steel_mid"])
        draw.rectangle([1, 1, 62, 62], outline=pal["steel_light"])
        draw.rectangle([3, 3, 60, 60], outline=pal["steel_shadow"])
        
        # Yellow / Neon circular perimeter
        col = pal["cable_core"] if is_night else pal["hazard_yellow"]
        draw.ellipse([6, 6, 57, 57], outline=col, width=3)
        draw.ellipse([14, 14, 49, 49], outline=pal["steel_dark"])
        
        # Center "A-01" / Drone symbol
        # "A"
        draw.line([(24, 42), (31, 20)], fill=col, width=3)
        draw.line([(39, 42), (32, 20)], fill=col, width=3)
        draw.line([(27, 34), (36, 34)], fill=col, width=2)
        
        # 4 Corner runway lights
        corners = [(6, 6), (57, 6), (6, 57), (57, 57)]
        for cx, cy in corners:
            draw.ellipse([cx-3, cy-3, cx+3, cy+3], fill=pal["steel_black"])
            draw.point((cx, cy), fill=(255, 255, 255, 255) if is_night else pal["hazard_yellow"])
            if is_night:
                draw.ellipse([cx-4, cy-4, cx+4, cy+4], outline=pal["cable_blue"])
                
        tag = "night" if is_night else "day"
        out_path = f"assets/sprites/environment/aegis_landing_pad_{tag}.png"
        img.save(out_path)
        print(f"Generated {out_path} (64x64)")

def generate_scrap_depot_zone():
    """64x64 Scrap crate deposit bay with hazard border stencils."""
    for is_night in [False, True]:
        img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        pal = PAL_NIGHT if is_night else PAL_DAY
        
        draw.rectangle([0, 0, 63, 63], fill=pal["steel_mid"])
        # Crosshatched grating inside
        draw.rectangle([6, 6, 57, 57], fill=pal["steel_black"])
        for x in range(8, 56, 4):
            draw.line([(x, 7), (x, 56)], fill=pal["steel_dark"])
        for y in range(8, 56, 4):
            draw.line([(7, y), (56, y)], fill=pal["steel_dark"])
            
        # Hazard striped outer border
        draw_hazard_stripes(draw, pal, (0, 0, 63, 6), "horizontal")
        draw_hazard_stripes(draw, pal, (0, 57, 63, 63), "horizontal")
        draw_hazard_stripes(draw, pal, (0, 6, 6, 57), "vertical")
        draw_hazard_stripes(draw, pal, (57, 6, 63, 57), "vertical")
        
        # Stencil "RECYCLE / SCRAP" cross symbol
        col = pal["hazard_yellow"]
        draw.rectangle([28, 16, 35, 47], fill=col)
        draw.rectangle([16, 28, 47, 35], fill=col)
        draw.rectangle([25, 25, 38, 38], fill=pal["steel_black"])
        
        tag = "night" if is_night else "day"
        out_path = f"assets/sprites/environment/scrap_depot_zone_{tag}.png"
        img.save(out_path)
        print(f"Generated {out_path} (64x64)")

def generate_central_tower_bay():
    """
    128x128 Central Tower Mounting Bay (The empty footprint!).
    User requested: Keep the center tower area empty for now.
    This asset represents the reinforced foundation bay with power umbilicals,
    alignment lasers, and anchor slots where the Comm Core and TOWER_OS terminal
    will be erected later.
    """
    for is_night in [False, True]:
        img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        pal = PAL_NIGHT if is_night else PAL_DAY
        
        # Outer steel decking
        draw.rectangle([0, 0, 127, 127], fill=pal["steel_mid"])
        
        # Outer beveled hexagonal perimeter
        hex_outer = [
            (38, 4), (89, 4), (123, 38), (123, 89),
            (89, 123), (38, 123), (4, 89), (4, 38)
        ]
        draw.polygon(hex_outer, fill=pal["steel_dark"], outline=pal["steel_light"])
        
        # Recessed foundation trench
        hex_trench = [
            (42, 10), (85, 10), (117, 42), (117, 85),
            (85, 117), (42, 117), (10, 85), (10, 42)
        ]
        draw.polygon(hex_trench, fill=pal["steel_black"], outline=pal["steel_shadow"])
        
        # Raised empty center mounting ring (waiting for the tower)
        draw.ellipse([28, 28, 99, 99], fill=pal["steel_dark"], outline=pal["steel_light"])
        draw.ellipse([34, 34, 93, 93], fill=pal["steel_black"], outline=pal["steel_shadow"])
        
        # Empty center pit
        draw.ellipse([44, 44, 83, 83], fill=pal["steel_mid"], outline=pal["steel_black"])
        draw.ellipse([48, 48, 79, 79], fill=pal["steel_black"])
        
        # Stencil "TOWER COMM CORE - RESERVED" marking / crosshair
        draw.line([(63, 16), (63, 111)], fill=pal["steel_dark"], width=2)
        draw.line([(16, 63), (111, 63)], fill=pal["steel_dark"], width=2)
        
        # 8 Anchor Bolt Sockets around the ring
        angles = [0, 45, 90, 135, 180, 225, 270, 315]
        for ang in angles:
            rad = math.radians(ang)
            bx = int(63 + 42 * math.cos(rad))
            by = int(63 + 42 * math.sin(rad))
            draw.ellipse([bx-4, by-4, bx+4, by+4], fill=pal["steel_black"], outline=pal["steel_light"])
            draw.point((bx, by), fill=pal["light_glow"])
            
        # 4 Heavy Power Umbilicals connecting to the sides
        # North umbilical
        draw.rectangle([58, 0, 68, 20], fill=pal["steel_black"])
        draw.line([(63, 0), (63, 20)], fill=pal["cable_core"])
        # South umbilical
        draw.rectangle([58, 107, 68, 127], fill=pal["steel_black"])
        draw.line([(63, 107), (63, 127)], fill=pal["cable_core"])
        # West umbilical
        draw.rectangle([0, 58, 20, 68], fill=pal["steel_black"])
        draw.line([(0, 63), (20, 63)], fill=pal["cable_core"])
        # East umbilical
        draw.rectangle([107, 58, 127, 68], fill=pal["steel_black"])
        draw.line([(107, 63), (127, 63)], fill=pal["cable_core"])
        
        if is_night:
            # Pulsing cyan alignment grid and laser targeting in the empty bay
            draw.ellipse([34, 34, 93, 93], outline=pal["cable_core"], width=2)
            draw.ellipse([48, 48, 79, 79], outline=pal["cable_core"])
            draw.line([(63, 28), (63, 99)], fill=pal["cable_core"])
            draw.line([(28, 63), (99, 63)], fill=pal["cable_core"])
            draw.point((63, 63), fill=(255, 255, 255, 255))
            
            # Glowing standby laser dots
            for ang in angles:
                rad = math.radians(ang)
                lx = int(63 + 26 * math.cos(rad))
                ly = int(63 + 26 * math.sin(rad))
                draw.point((lx, ly), fill=pal["cable_core"])
                
        tag = "night" if is_night else "day"
        out_path = f"assets/sprites/environment/central_tower_bay_{tag}.png"
        img.save(out_path)
        print(f"Generated {out_path} (128x128)")

if __name__ == "__main__":
    print("=== Generating FACTORY RESET Pixel Art Map Assets ===")
    generate_tilesets()
    generate_turret_mount_pad()
    generate_aegis_landing_pad()
    generate_scrap_depot_zone()
    generate_central_tower_bay()
    print("=== All Assets Successfully Generated! ===")
