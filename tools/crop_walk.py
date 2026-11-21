import os
from PIL import Image
import numpy as np
from scipy import ndimage

im = Image.open(r"art (2)\art\monsters\Gemini_Generated_Image_puu42epuu42epuu4.jpg")
w, h = im.size
print(f"Size: {w}x{h}")

# The walk frames are in the upper portion: y from ~300 to ~1080
# 6 frames across the width
frame_w = w / 6.0
out_dir = r"FACTORY_RESET-main\test_out\amalgam_walk"
os.makedirs(out_dir, exist_ok=True)

for i in range(6):
    x0 = int(i * frame_w)
    x1 = int((i + 1) * frame_w)
    crop = im.crop((x0, 280, x1, 1080))
    
    # Remove background
    arr = np.array(crop).astype(float)
    sat = np.max(arr, axis=2) - np.min(arr, axis=2)
    val = np.mean(arr, axis=2)
    is_bg = (sat <= 18) & (val >= 70) & (val <= 170)
    
    border_mask = np.zeros(is_bg.shape, dtype=bool)
    border_mask[0, :] = True
    border_mask[-1, :] = True
    border_mask[:, 0] = True
    border_mask[:, -1] = True
    seeds = border_mask & is_bg
    bg_conn = ndimage.binary_propagation(seeds, mask=is_bg)
    
    alpha = np.where(bg_conn, 0, 255).astype(np.uint8)
    rgba = np.dstack([np.array(crop), alpha])
    res = Image.fromarray(rgba)
    
    # Trim empty borders
    bbox = res.getbbox()
    if bbox:
        res = res.crop(bbox)
        
    res.save(os.path.join(out_dir, f"walk_{i}.png"))
    print(f"Saved walk_{i}.png, size={res.size}")
