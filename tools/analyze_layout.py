import os
from PIL import Image
import numpy as np

def detect_sprites(img_path):
    # Load and convert to grayscale
    im = Image.open(img_path)
    im_small = im.resize((256, 144))
    arr = np.array(im_small).astype(float)
    
    # Estimate background from corners/edges
    border = np.concatenate([arr[0:5, :, :].reshape(-1, 3), arr[-5:, :, :].reshape(-1, 3), arr[:, 0:5, :].reshape(-1, 3), arr[:, -5:, :].reshape(-1, 3)])
    bg_color = np.median(border, axis=0)
    
    # Distance from background
    diff = np.sqrt(np.sum((arr - bg_color)**2, axis=2))
    mask = diff > 30.0 # foreground
    
    # Check vertical and horizontal projection of foreground
    v_proj = np.mean(mask, axis=0) # along x
    h_proj = np.mean(mask, axis=1) # along y
    
    # Count peaks / columns
    col_active = v_proj > 0.05
    transitions = np.diff(col_active.astype(int))
    num_cols = np.sum(transitions == 1)
    
    fg_ratio = np.mean(mask)
    return {
        'size': im.size,
        'bg_color': [round(x, 1) for x in bg_color],
        'fg_ratio': round(fg_ratio, 3),
        'est_columns': int(num_cols)
    }

for cat in ['agent_new', 'Craft_new', 'day_back', 'Drone', 'Gun', 'monsters', 'night_back']:
    folder = os.path.join(r"art (2)\art", cat)
    if not os.path.exists(folder): continue
    files = [f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.png'))]
    print(f"=== {cat} ({len(files)} files) ===")
    for f in files[:5]:
        p = os.path.join(folder, f)
        res = detect_sprites(p)
        print(f"  {f[:30]} | {res}")
