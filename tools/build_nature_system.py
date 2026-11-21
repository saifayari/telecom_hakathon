#!/usr/bin/env python3
"""
Nature Tileset & Map Assets Generator for FACTORY RESET.
Sources high quality CC0 pixel art from LPC (Liberated Pixel Cup),
assembles Day and Night sheets (32x32 tiles), generates tree props,
and creates the empty central tower bay for the outdoor setting.
"""

import os
import colorsys
from PIL import Image, ImageDraw, ImageFilter

TILE_SIZE = 32
GRID_COLS = 8
GRID_ROWS = 8
SHEET_W = GRID_COLS * TILE_SIZE  # 256
SHEET_H = GRID_ROWS * TILE_SIZE  # 256

def day_to_night_pixel(r, g, b, a):
    if a == 0:
        return (0, 0, 0, 0)
    
    rf, gf, bf = r / 255.0, g / 255.0, b / 255.0
    h, s, v = colorsys.rgb_to_hsv(rf, gf, bf)
    
    # Foliage / Green (h between 0.18 and 0.45)
    if 0.18 <= h <= 0.45:
        # Shift to cool nocturnal moonlit teal
        h = 0.50 + (h - 0.25) * 0.18
        s = min(1.0, s * 0.72 + 0.12)
        v = v * 0.48 + 0.04
    # Earth / Dirt / Wood (h between 0.04 and 0.18)
    elif 0.04 <= h < 0.18:
        # Shift to deep nocturnal slate-navy loam
        h = 0.62 + (h - 0.10) * 0.15
        s = s * 0.35
        v = v * 0.38 + 0.03
    # Stone / Grey / Rock (low saturation)
    elif s < 0.15:
        h = 0.60
        s = 0.25
        v = v * 0.42 + 0.03
    # Bright flowers / accents
    elif v > 0.7 and s > 0.4:
        # Turn flowers into glowing night-blooms
        h = (h + 0.4) % 1.0
        v = v * 0.7 + 0.15
    else:
        h = (h + 0.5) % 1.0
        v = v * 0.40
        
    nr, ng, nb = colorsys.hsv_to_rgb(h, s, v)
    return (int(nr * 255), int(ng * 255), int(nb * 255), a)

def convert_image_to_night(img):
    out = Image.new("RGBA", img.size)
    pixels = img.load()
    out_pixels = out.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            out_pixels[x, y] = day_to_night_pixel(*pixels[x, y])
    return out

def build_nature_assets():
    base_dir = "assets/sprites/environment"
    day_dir = os.path.join(base_dir, "nature_day")
    night_dir = os.path.join(base_dir, "nature_night")
    os.makedirs(day_dir, exist_ok=True)
    os.makedirs(night_dir, exist_ok=True)
    
    # 1. Load source LPC images
    terr_src = Image.open("/tmp/asset_download/lpc_terrain_outside.png").convert("RGBA")
    obj_src = Image.open("/tmp/asset_download/lpc_outside_objects.png").convert("RGBA")
    
    # 2. Extract Key Base Tiles (32x32)
    # Grass tiles from terrain
    t_grass_plain = terr_src.crop((32, 192, 64, 224))
    t_grass_alt1 = terr_src.crop((64, 192, 96, 224))
    t_grass_alt2 = terr_src.crop((32, 224, 64, 256))
    t_grass_alt3 = terr_src.crop((64, 224, 96, 256))
    
    # Dirt tiles from terrain
    t_dirt_plain = terr_src.crop((32, 0, 64, 32))
    t_dirt_alt1 = terr_src.crop((64, 0, 96, 32))
    t_dirt_alt2 = terr_src.crop((32, 32, 64, 64))
    t_dirt_alt3 = terr_src.crop((64, 32, 96, 64))
    
    # Dirt-to-grass transitions
    t_trans_top = terr_src.crop((32, 64, 64, 96))
    t_trans_bottom = terr_src.crop((32, 128, 64, 160))
    t_trans_left = terr_src.crop((0, 96, 32, 128))
    t_trans_right = terr_src.crop((64, 96, 96, 128))
    t_trans_tl = terr_src.crop((0, 64, 32, 96))
    t_trans_tr = terr_src.crop((64, 64, 96, 96))
    t_trans_bl = terr_src.crop((0, 128, 32, 160))
    t_trans_br = terr_src.crop((64, 128, 96, 160))
    
    # Props and decorations (from obj_src)
    # Rocks, flowers, bushes, stumps
    t_rock_small = obj_src.crop((0, 32, 32, 64))
    t_rock_boulder = obj_src.crop((32, 32, 64, 64))
    t_bush_small = obj_src.crop((64, 32, 96, 64))
    t_flowers = obj_src.crop((96, 32, 128, 64))
    t_stump = obj_src.crop((128, 32, 160, 64))
    t_mushrooms = obj_src.crop((160, 32, 192, 64))
    t_shrub = obj_src.crop((0, 64, 32, 96))
    t_tall_grass = obj_src.crop((32, 64, 64, 96))
    
    # Compose 8x8 Day Nature Tileset (256x256)
    sheet_day = Image.new("RGBA", (SHEET_W, SHEET_H), (0, 0, 0, 0))
    
    # Row 0: Grass variations (0..7)
    grass_row = [t_grass_plain, t_grass_alt1, t_grass_alt2, t_grass_alt3,
                 t_grass_plain, t_grass_alt1, t_grass_alt2, t_grass_alt3]
    for c, t in enumerate(grass_row):
        sheet_day.paste(t, (c * TILE_SIZE, 0 * TILE_SIZE))
        
    # Row 1: Dirt variations (8..15)
    dirt_row = [t_dirt_plain, t_dirt_alt1, t_dirt_alt2, t_dirt_alt3,
                t_dirt_plain, t_dirt_alt1, t_dirt_alt2, t_dirt_alt3]
    for c, t in enumerate(dirt_row):
        sheet_day.paste(t, (c * TILE_SIZE, 1 * TILE_SIZE))
        
    # Row 2: Transitions Dirt to Grass (16..23)
    trans_row = [t_trans_top, t_trans_bottom, t_trans_left, t_trans_right,
                 t_trans_tl, t_trans_tr, t_trans_bl, t_trans_br]
    for c, t in enumerate(trans_row):
        sheet_day.paste(t, (c * TILE_SIZE, 2 * TILE_SIZE))
        
    # Row 3: Props on transparent ground (can be layered or blended with grass)
    props_row = [t_rock_small, t_rock_boulder, t_bush_small, t_flowers,
                 t_stump, t_mushrooms, t_shrub, t_tall_grass]
    for c, t in enumerate(props_row):
        # Composite over grass base so it can be used directly as a ground tile!
        composed = t_grass_plain.copy()
        composed.paste(t, (0, 0), t)
        sheet_day.paste(composed, (c * TILE_SIZE, 3 * TILE_SIZE))
        
    # Row 4: Props on transparent background
    for c, t in enumerate(props_row):
        sheet_day.paste(t, (c * TILE_SIZE, 4 * TILE_SIZE))
        
    # Row 5: Central Tower Cleared Foundation Border (Cobblestone / Earth rim)
    # 8 tiles defining the outer ring of the clearing
    for c in range(8):
        # Cobblestone / foundation rim over dirt
        rim_tile = t_dirt_plain.copy()
        draw = ImageDraw.Draw(rim_tile)
        draw.rectangle([2, 2, 29, 29], outline=(90, 85, 75, 255))
        draw.line([(0, 15), (31, 15)], fill=(75, 70, 60, 255))
        draw.line([(15, 0), (15, 31)], fill=(75, 70, 60, 255))
        # Anchor bolt
        draw.ellipse([12, 12, 19, 19], fill=(50, 50, 55, 255), outline=(130, 130, 140, 255))
        sheet_day.paste(rim_tile, (c * TILE_SIZE, 5 * TILE_SIZE))
        
    # Row 6: Empty Center Foundation Floor (64x64 or 32x32 tiles)
    for c in range(8):
        pit_tile = t_dirt_plain.copy()
        draw = ImageDraw.Draw(pit_tile)
        # Circular mounting guide groove
        draw.ellipse([4, 4, 27, 27], outline=(60, 55, 50, 255))
        draw.point((15, 15), fill=(180, 170, 150, 255))
        sheet_day.paste(pit_tile, (c * TILE_SIZE, 6 * TILE_SIZE))
        
    # Row 7: Deep Wilderness Border (Dense shrubs & cliff grass)
    for c in range(8):
        dense_tile = t_grass_plain.copy()
        dense_tile.paste(t_bush_small, ((c * 4) % 16, (c * 3) % 16), t_bush_small)
        sheet_day.paste(dense_tile, (c * TILE_SIZE, 7 * TILE_SIZE))
        
    # Save Day Tileset
    sheet_day_path = os.path.join(base_dir, "nature_tileset_day.png")
    sheet_day.save(sheet_day_path)
    print(f"Generated {sheet_day_path} (256x256)")
    
    # 3. Generate Night Tileset via authentic palette shift
    sheet_night = convert_image_to_night(sheet_day)
    
    # Add subtle night bioluminescence to mushrooms and lights
    draw_night = ImageDraw.Draw(sheet_night)
    # On row 3 (prop row), column 5 is mushrooms: add cyan spore glow!
    shroom_x = 5 * TILE_SIZE
    shroom_y = 3 * TILE_SIZE
    draw_night.point((shroom_x + 14, shroom_y + 16), fill=(0, 240, 255, 255))
    draw_night.point((shroom_x + 20, shroom_y + 12), fill=(0, 240, 255, 255))
    
    sheet_night_path = os.path.join(base_dir, "nature_tileset_night.png")
    sheet_night.save(sheet_night_path)
    print(f"Generated {sheet_night_path} (256x256)")
    
    # 4. Extract and Build Standalone Trees
    # Oak Tree (96x160 px: 3 cols x 5 rows)
    tree_oak_day = obj_src.crop((192, 0, 192 + 96, 160))
    tree_oak_night = convert_image_to_night(tree_oak_day)
    # Add subtle moonlight gleam on upper leaf crown
    draw_tree = ImageDraw.Draw(tree_oak_night)
    for lx in range(20, 76, 4):
        draw_tree.point((lx, 8), fill=(120, 200, 220, 200))
        
    oak_day_path = os.path.join(base_dir, "tree_oak_day.png")
    oak_night_path = os.path.join(base_dir, "tree_oak_night.png")
    tree_oak_day.save(oak_day_path)
    tree_oak_night.save(oak_night_path)
    print(f"Generated {oak_day_path} and {oak_night_path} (96x160)")
    
    # Pine Tree (64x128 px)
    tree_pine_day = obj_src.crop((288, 0, 288 + 96, 160)).crop((16, 16, 80, 144))
    tree_pine_night = convert_image_to_night(tree_pine_day)
    pine_day_path = os.path.join(base_dir, "tree_pine_day.png")
    pine_night_path = os.path.join(base_dir, "tree_pine_night.png")
    tree_pine_day.save(pine_day_path)
    tree_pine_night.save(pine_night_path)
    print(f"Generated {pine_day_path} and {pine_night_path} (64x128)")
    
    # 5. Build Central Tower Empty Clearing (128x128)
    # A natural circular clearing in the earth with mounting anchor points
    # leaving the center completely open for the tower as requested!
    clearing_day = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    draw_cl = ImageDraw.Draw(clearing_day)
    
    # Packed earth clearing base
    for y in range(0, 128, 32):
        for x in range(0, 128, 32):
            clearing_day.paste(t_dirt_plain, (x, y))
            
    # Circular foundation trench & outer boundary
    draw_cl.ellipse([4, 4, 123, 123], outline=(95, 75, 55, 255), width=3)
    draw_cl.ellipse([14, 14, 113, 113], outline=(65, 50, 35, 255), width=2)
    # Empty center mounting pad (where Comm Core will sit)
    draw_cl.ellipse([32, 32, 95, 95], outline=(120, 115, 100, 255), width=2)
    draw_cl.ellipse([44, 44, 83, 83], outline=(80, 75, 65, 255), fill=(45, 38, 30, 255))
    
    # 4 Heavy foundation anchor pins
    anchors = [(63, 16), (63, 111), (16, 63), (111, 63)]
    for ax, ay in anchors:
        draw_cl.ellipse([ax-5, ay-5, ax+5, ay+5], fill=(70, 70, 80, 255), outline=(140, 140, 155, 255))
        draw_cl.point((ax, ay), fill=(220, 180, 40, 255))
        
    clearing_night = convert_image_to_night(clearing_day)
    draw_cl_n = ImageDraw.Draw(clearing_night)
    # Standby alignment guides glowing in the empty clearing at night
    draw_cl_n.ellipse([32, 32, 95, 95], outline=(0, 220, 255, 255))
    draw_cl_n.ellipse([44, 44, 83, 83], outline=(0, 160, 220, 255))
    for ax, ay in anchors:
        draw_cl_n.point((ax, ay), fill=(0, 255, 255, 255))
        
    clearing_day_path = os.path.join(base_dir, "tower_clearing_day.png")
    clearing_night_path = os.path.join(base_dir, "tower_clearing_night.png")
    clearing_day.save(clearing_day_path)
    clearing_night.save(clearing_night_path)
    print(f"Generated {clearing_day_path} and {clearing_night_path} (128x128)")

if __name__ == "__main__":
    print("=== Building Nature Assets (Day & Night) from LPC ===")
    build_nature_assets()
    print("=== Done! ===")
