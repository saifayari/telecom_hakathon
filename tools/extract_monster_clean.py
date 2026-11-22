import os
from PIL import Image
import numpy as np
from scipy import ndimage

ART = r"art (2)\art\monsters"
if not os.path.exists(ART):
    ART = r"assests\monsters"
OUT = r"FACTORY_RESET-main\assets\sprites\monsters\amalgam"
OUT_DIR = OUT
os.makedirs(OUT, exist_ok=True)

print("1. Extracting Walk Cycle (6 frames) from puu42epuu42epuu4.jpg...")
im_walk_path = os.path.join(ART, "Gemini_Generated_Image_puu42epuu42epuu4.jpg")
im = Image.open(im_walk_path)
arr = np.array(im).astype(float)

diff_rg = np.abs(arr[:,:,0] - arr[:,:,1])
diff_gb = np.abs(arr[:,:,1] - arr[:,:,2])
diff_rb = np.abs(arr[:,:,0] - arr[:,:,2])
max_diff = np.maximum(diff_rg, np.maximum(diff_gb, diff_rb))

splits = [0, 512, 1081, 1565, 2069, 2590, 3168]
CANVAS_SIZE = (128, 128)
TARGET_H = 96
BASELINE_Y = 120
TARGET_CENTER_X = 64

raw_frames = []
for i in range(6):
    x0, x1 = splits[i], splits[i+1]
    crop_rgb = arr[230:1120, x0:x1, :].copy()
    crop_diff = max_diff[230:1120, x0:x1].copy()
    
    is_bg_cand = (crop_diff <= 3.5)
    lbl_bg, num_bg = ndimage.label(is_bg_cand)
    bg = np.zeros(is_bg_cand.shape, dtype=bool)
    for b in range(1, num_bg + 1):
        mask = (lbl_bg == b)
        if mask.sum() > 1500:
            bg |= mask
    bg = ndimage.binary_dilation(bg, iterations=2) & (crop_diff <= 5.5)
    
    fg = ~bg
    lbl, num = ndimage.label(fg)
    sizes = ndimage.sum(fg, lbl, range(num + 1))
    fg_clean = (sizes > 1000)[lbl]
    
    h_c, w_c, _ = crop_rgb.shape
    if i == 5:
        fg_clean[int(h_c*0.8):, int(w_c*0.5):] = False
        
    alpha = np.where(fg_clean, 255, 0).astype(np.uint8)
    rgba = np.dstack([crop_rgb.astype(np.uint8), alpha])
    pil_rgba = Image.fromarray(rgba)
    bbox = pil_rgba.getbbox()
    c_img = pil_rgba.crop(bbox)
    raw_frames.append((c_img, bbox))

heights = [f[0].height for f in raw_frames]
median_h = float(np.median(heights))
scale = TARGET_H / median_h

for i, (c_img, bbox) in enumerate(raw_frames):
    new_w = max(1, int(round(c_img.width * scale)))
    new_h = max(1, int(round(c_img.height * scale)))
    resized = c_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    res_arr = np.array(resized)
    alpha = res_arr[:, :, 3]
    torso_alpha = alpha[int(new_h*0.2):int(new_h*0.6), :]
    col_mass = torso_alpha.sum(axis=0)
    com_x = (np.arange(new_w) * col_mass).sum() / col_mass.sum() if col_mass.sum() > 0 else new_w / 2.0
        
    canvas = Image.new('RGBA', CANVAS_SIZE, (0, 0, 0, 0))
    paste_x = int(round(TARGET_CENTER_X - com_x))
    paste_y = int(round(BASELINE_Y - new_h))
    paste_x = max(0, min(CANVAS_SIZE[0] - new_w, paste_x))
    paste_y = max(0, min(CANVAS_SIZE[1] - new_h, paste_y))
    canvas.paste(resized, (paste_x, paste_y), resized)
    
    canvas_flipped = canvas.transpose(Image.FLIP_LEFT_RIGHT)
    out_path = os.path.join(OUT_DIR, f'amalgam_walk_{i}.png')
    canvas_flipped.save(out_path)
    print(f"Saved: {out_path} ({canvas_flipped.size})")

print("SUCCESS: All 6 Unit-R17 walk frames extracted with uniform scale, torso centering, and baseline alignment.")
