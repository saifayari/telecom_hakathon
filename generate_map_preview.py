import numpy as np
from PIL import Image

# Load day and night tilesets
day_tileset = Image.open('assets/sprites/environment/metalslug_tileset_day.png')
night_tileset = Image.open('assets/sprites/environment/metalslug_tileset_night.png')

# Load tree props
oak_lg_d = Image.open('assets/sprites/environment/tree_oak_large_day.png')
oak_lg_n = Image.open('assets/sprites/environment/tree_oak_large_night.png')

oak_md_d = Image.open('assets/sprites/environment/tree_oak_med_day.png')
oak_md_n = Image.open('assets/sprites/environment/tree_oak_med_night.png')

pine_d = Image.open('assets/sprites/environment/tree_pine_day.png')
pine_n = Image.open('assets/sprites/environment/tree_pine_night.png')

dead_d = Image.open('assets/sprites/environment/tree_dead_day.png')
dead_n = Image.open('assets/sprites/environment/tree_dead_night.png')

stump_d = Image.open('assets/sprites/environment/tree_stump_day.png')
stump_n = Image.open('assets/sprites/environment/tree_stump_night.png')

# 64 cols x 48 rows = 2048 x 1536
cols, rows = 64, 48
tile_size = 32
w, h = cols * tile_size, rows * tile_size

# Deterministic layout
np.random.seed(1337)

# Grid cells: (tile_col, tile_row)
grid = np.zeros((rows, cols, 2), dtype=int)

for r in range(rows):
    for c in range(cols):
        # Base dirt default
        tc, tr = 0, 0
        rand_v = np.random.rand()
        if rand_v < 0.12:
            tc, tr = 1, 0 # fissure
        elif rand_v < 0.22:
            tc, tr = 2, 0 # gravel
        elif rand_v < 0.30:
            tc, tr = 3, 0 # weed
        elif rand_v < 0.35:
            tc, tr = 4, 0 # metal plate
        elif rand_v < 0.40:
            tc, tr = 5, 0 # tread mark
        elif rand_v < 0.45:
            tc, tr = 6, 0 # scrap shard
        elif rand_v < 0.50:
            tc, tr = 4, 3 # earth var 2
        elif rand_v < 0.55:
            tc, tr = 5, 3 # earth var 3
        elif rand_v < 0.60:
            tc, tr = 6, 3 # earth var 4
        else:
            tc, tr = 0, 0 # base dirt
        grid[r, c] = [tc, tr]

# Central Tower Platform: (col: 27..36, row: 19..28) -> 10x10 tiles = 320x320 px
# Top-left at col 27, row 19. Bottom-right at col 36, row 28.
c_start, c_end = 27, 36
r_start, r_end = 19, 28

for r in range(r_start, r_end + 1):
    for c in range(c_start, c_end + 1):
        if r == r_start and c == c_start:
            grid[r, c] = [0, 1] # TL corner
        elif r == r_start and c == c_end:
            grid[r, c] = [2, 1] # TR corner
        elif r == r_end and c == c_start:
            grid[r, c] = [6, 1] # BL corner
        elif r == r_end and c == c_end:
            grid[r, c] = [0, 2] # BR corner
        elif r == r_start:
            grid[r, c] = [1, 1] # Top edge
        elif r == r_end:
            grid[r, c] = [7, 1] # Bottom edge
        elif c == c_start:
            grid[r, c] = [3, 1] # Left edge
        elif c == c_end:
            grid[r, c] = [5, 1] # Right edge
        else:
            # Interior platform floor
            grid[r, c] = [4, 1]

# Conduits and Central Socket:
# Center is cols 31, 32 and rows 23, 24
grid[23, 31] = [4, 2] # Tower mounting socket TL
grid[23, 32] = [4, 2] # Tower mounting socket TR
grid[24, 31] = [4, 2] # Tower mounting socket BL
grid[24, 32] = [4, 2] # Tower mounting socket BR

# Horizontal conduits leading in from left and right
for c in range(c_start + 1, 31):
    grid[23, c] = [1, 2]
    grid[24, c] = [1, 2]
for c in range(33, c_end):
    grid[23, c] = [1, 2]
    grid[24, c] = [1, 2]

# Vertical conduits leading in from top and bottom
for r in range(r_start + 1, 23):
    grid[r, 31] = [2, 2]
    grid[r, 32] = [2, 2]
for r in range(25, r_end):
    grid[r, 31] = [2, 2]
    grid[r, 32] = [2, 2]

# Vent grates in 4 corners of platform
grid[r_start + 2, c_start + 2] = [5, 2]
grid[r_start + 2, c_end - 2] = [5, 2]
grid[r_end - 2, c_start + 2] = [5, 2]
grid[r_end - 2, c_end - 2] = [5, 2]

# Warning beacon pads near corners
grid[r_start + 1, c_start + 1] = [7, 2]
grid[r_start + 1, c_end - 1] = [7, 2]
grid[r_end - 1, c_start + 1] = [7, 2]
grid[r_end - 1, c_end - 1] = [7, 2]

# Place trees around perimeter (14 sparse trees):
tree_placements = [
    ('oak_lg', 180, 50),
    ('pine', 650, 45),
    ('oak_md', 1380, 50),
    ('dead', 1860, 45),
    ('dead', 200, 1470),
    ('oak_md', 720, 1480),
    ('pine', 1320, 1475),
    ('oak_lg', 1840, 1470),
    ('dead', 50, 480),
    ('stump', 60, 760),
    ('oak_md', 55, 1040),
    ('pine', 1990, 480),
    ('stump', 1980, 760),
    ('dead', 1995, 1040)
]

# Sort trees by Y for proper Y-sort rendering
tree_placements.sort(key=lambda t: t[2])

def render_map(tileset, tree_dict):
    img = Image.new('RGBA', (w, h))
    # Render tiles
    for r in range(rows):
        for c in range(cols):
            tc, tr = grid[r, c]
            tile = tileset.crop((tc * 32, tr * 32, (tc + 1) * 32, (tr + 1) * 32))
            img.paste(tile, (c * 32, r * 32))
            
    # Render trees
    for t_type, tx, ty in tree_placements:
        t_img = tree_dict[t_type]
        px = tx - t_img.width // 2
        py = ty - t_img.height + 16
        img.paste(t_img, (px, py), t_img)
        
    return img

day_trees = {'oak_lg': oak_lg_d, 'oak_md': oak_md_d, 'pine': pine_d, 'dead': dead_d, 'stump': stump_d}
night_trees = {'oak_lg': oak_lg_n, 'oak_md': oak_md_n, 'pine': pine_n, 'dead': dead_n, 'stump': stump_n}

print('Rendering day map...')
map_day = render_map(day_tileset, day_trees)
map_day.save('assets/sprites/environment/metalslug_arena_day.png')

print('Rendering night map...')
map_night = render_map(night_tileset, night_trees)
map_night.save('assets/sprites/environment/metalslug_arena_night.png')

# Create half-scale thumbnails for fast preview
map_day.resize((1024, 768), Image.Resampling.BILINEAR).save('assets/sprites/environment/metalslug_arena_day_thumb.png')
map_night.resize((1024, 768), Image.Resampling.BILINEAR).save('assets/sprites/environment/metalslug_arena_night_thumb.png')

# Also render with-tower previews
tower_d = Image.open('assets/sprites/environment/telecom_tower_day.png').convert('RGBA')
tower_n = Image.open('assets/sprites/environment/telecom_tower_night.png').convert('RGBA')

with_tower_day = map_day.copy()
# Tower base centered at (1024, 768)
tw_x = 1024 - tower_d.width // 2
tw_y = 768 - tower_d.height + 64
with_tower_day.paste(tower_d, (tw_x, tw_y), tower_d)
with_tower_day.save('assets/sprites/environment/metalslug_arena_with_tower_day.png')

with_tower_night = map_night.copy()
with_tower_night.paste(tower_n, (tw_x, tw_y), tower_n)
with_tower_night.save('assets/sprites/environment/metalslug_arena_with_tower_night.png')

print('Map previews generated successfully!')
