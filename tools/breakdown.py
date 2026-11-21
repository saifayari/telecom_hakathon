import os
from PIL import Image
import numpy as np

def analyze_sheet(folder, filename):
    p = os.path.join(folder, filename)
    im = Image.open(p)
    w, h = im.size
    
    # Analyze color clusters
    small = im.resize((128, 72))
    arr = np.array(small).astype(float)
    
    # Estimate background from borders
    border = np.concatenate([arr[0:3, :, :].reshape(-1, 3), arr[-3:, :, :].reshape(-1, 3), arr[:, 0:3, :].reshape(-1, 3), arr[:, -3:, :].reshape(-1, 3)])
    bg = np.median(border, axis=0)
    
    diff = np.sqrt(np.sum((arr - bg)**2, axis=2))
    thresh = diff > 25.0
    
    # Projections
    v_proj = np.mean(thresh, axis=0) # along X
    h_proj = np.mean(thresh, axis=1) # along Y
    
    # Count horizontal slices (rows) and vertical slices (cols)
    def count_segments(proj, min_val=0.03):
        active = proj > min_val
        diffs = np.diff(active.astype(int))
        starts = np.where(diffs == 1)[0]
        ends = np.where(diffs == -1)[0]
        return len(starts)
        
    rows = count_segments(h_proj, 0.05)
    cols = count_segments(v_proj, 0.05)
    
    return w, h, rows, cols, bg

print("=== DETAILED BREAKDOWN OF ASSET FOLDERS ===")
for cat in ['agent_new', 'monsters', 'Drone', 'Gun', 'Craft_new', 'day_back', 'night_back']:
    folder = os.path.join(r"art (2)\art", cat)
    if not os.path.exists(folder): continue
    files = sorted([f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.png'))])
    print(f"\n--- {cat} ({len(files)} files) ---")
    for f in files:
        w, h, r, c, bg = analyze_sheet(folder, f)
        print(f"{f}: {w}x{h} | rows={r}, cols={c} | bg={[int(x) for x in bg]}")
