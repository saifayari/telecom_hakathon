import os
from PIL import Image
import numpy as np
from scipy import ndimage

ART = r"art (2)\art\monsters"
OUT = r"FACTORY_RESET-main\assets\sprites\monsters\amalgam"
os.makedirs(OUT, exist_ok=True)

def clean_rgba_adaptive(im_crop):
    arr = np.array(im_crop).astype(float)
    h, w, _ = arr.shape
    sat = np.max(arr, axis=2) - np.min(arr, axis=2)
    val = np.mean(arr, axis=2)
    
    border = np.concatenate([arr[0:3,:,:], arr[-3:,:,:], arr[:,0:3,:], arr[:,-3:,:]], axis=None).reshape(-1, 3)
    b_sat = np.max(border, axis=1) - np.min(border, axis=1)
    b_val = np.mean(border, axis=1)
    
    max_sat = max(28, float(np.percentile(b_sat, 85)) + 8)
    bg_lo = max(10, float(np.percentile(b_val, 5)) - 15)
    bg_hi = min(245, float(np.percentile(b_val, 95)) + 15)
    
    is_bg = (sat <= max_sat) & (val >= bg_lo) & (val <= bg_hi)
    border_mask = np.zeros((h, w), dtype=bool)
    border_mask[0:3, :] = True
    border_mask[-3:, :] = True
    border_mask[:, 0:3] = True
    border_mask[:, -3:] = True
    seeds = border_mask & is_bg
    bg_conn = ndimage.binary_propagation(seeds, mask=is_bg)
    bg_conn = ndimage.binary_dilation(bg_conn, iterations=1)
    
    alpha = np.where(bg_conn, 0, 255).astype(np.uint8)
    rgba = np.dstack([np.array(im_crop), alpha])
    
    # Strictly keep the largest connected component
    mask = alpha > 20
    lbl, num = ndimage.label(mask)
    if num > 1:
        objs = ndimage.find_objects(lbl)
        largest_idx = 0
        max_area = 0
        for idx, o in enumerate(objs):
            area = (lbl[o] == (idx + 1)).sum()
            if area > max_area:
                max_area = area
                largest_idx = idx + 1
        clean_alpha = np.where(lbl == largest_idx, alpha, 0).astype(np.uint8)
        rgba[:, :, 3] = clean_alpha
        
    return Image.fromarray(rgba)

def make_uniform(crop_rgba, canvas_size=(128, 128), target_h=96):
    bbox = crop_rgba.getbbox()
    if not bbox:
        return Image.new('RGBA', canvas_size, (0, 0, 0, 0))
    c = crop_rgba.crop(bbox)
    scale = target_h / float(c.height)
    new_w = max(1, int(round(c.width * scale)))
    new_h = target_h
    c = c.resize((new_w, new_h), Image.Resampling.LANCZOS)
    canvas = Image.new('RGBA', canvas_size, (0, 0, 0, 0))
    paste_x = (canvas_size[0] - new_w) // 2
    paste_y = canvas_size[1] - 8 - new_h # 8px margin from bottom
    canvas.paste(c, (paste_x, paste_y), c)
    return canvas

print("1. Extracting Walk Cycle (6 frames) from puu42epuu42epuu4.jpg...")
im_walk = Image.open(os.path.join(ART, "Gemini_Generated_Image_puu42epuu42epuu4.jpg"))
walk_boxes = [
    (57, 319, 634, 983),
    (617, 326, 1064, 922),
    (1168, 322, 1519, 877),
    (1598, 318, 2029, 876),
    (2082, 318, 2570, 1050),
    (2600, 318, 3144, 955)
]
for i, box in enumerate(walk_boxes):
    c = clean_rgba_adaptive(im_walk.crop(box))
    u = make_uniform(c, canvas_size=(128, 128), target_h=96)
    out_p = os.path.join(OUT, f"amalgam_walk_{i}.png")
    u.save(out_p)
    print(f"Saved: {out_p} ({u.size})")

print("2. Extracting Attack Cycle (4 frames) from gbfa28gbfa28gbfa.jpg...")
im_atk = Image.open(os.path.join(ART, "Gemini_Generated_Image_gbfa28gbfa28gbfa.jpg"))
atk_boxes = [
    (50, 195, 489, 644),
    (523, 209, 976, 655),
    (1019, 228, 1520, 615),
    (1604, 223, 1987, 647)
]
for i, box in enumerate(atk_boxes):
    c = clean_rgba_adaptive(im_atk.crop(box))
    u = make_uniform(c, canvas_size=(128, 128), target_h=96)
    out_p = os.path.join(OUT, f"amalgam_attack_{i}.png")
    u.save(out_p)
    print(f"Saved: {out_p} ({u.size})")

print("3. Extracting Hit frame from gbfa28gbfa28gbfa.jpg...")
c_hit = clean_rgba_adaptive(im_atk.crop((2049, 227, 2608, 658)))
u_hit = make_uniform(c_hit, canvas_size=(128, 128), target_h=96)
out_hit = os.path.join(OUT, "amalgam_hit.png")
u_hit.save(out_hit)
print(f"Saved: {out_hit} ({u_hit.size})")

print("4. Extracting Idle frame from mebcbfmebcbfmebc.jpg...")
im_idle = Image.open(os.path.join(ART, "Gemini_Generated_Image_mebcbfmebcbfmebc.jpg"))
c_idle = clean_rgba_adaptive(im_idle.crop((725, 236, 2122, 1257)))
u_idle = make_uniform(c_idle, canvas_size=(128, 128), target_h=96)
out_idle = os.path.join(OUT, "amalgam_idle.png")
u_idle.save(out_idle)
print(f"Saved: {out_idle} ({u_idle.size})")

print("SUCCESS: All monster amalgam frames cleaned and standardized to 128x128!")
