import os
from PIL import Image
import numpy as np
from scipy import ndimage

def clean_sheet(image_path, bg_lo=0, bg_hi=255, max_sat=25):
    im = Image.open(image_path)
    arr = np.array(im).astype(float)
    h, w, _ = arr.shape
    
    # Saturation: max(rgb) - min(rgb)
    sat = np.max(arr, axis=2) - np.min(arr, axis=2)
    val = np.mean(arr, axis=2)
    
    is_bg = (sat <= max_sat) & (val >= bg_lo) & (val <= bg_hi)
    
    border_mask = np.zeros((h, w), dtype=bool)
    border_mask[0:3, :] = True
    border_mask[-3:, :] = True
    border_mask[:, 0:3] = True
    border_mask[:, -3:] = True
    
    seeds = border_mask & is_bg
    bg_conn = ndimage.binary_propagation(seeds, mask=is_bg)
    
    # Expand by 1 pixel to clean jpeg edge ringing
    bg_conn = ndimage.binary_dilation(bg_conn, iterations=1)
    
    alpha = np.where(bg_conn, 0, 255).astype(np.uint8)
    rgba = np.dstack([np.array(im), alpha])
    return Image.fromarray(rgba)

cleaned = clean_sheet(r"art (2)\art\monsters\Gemini_Generated_Image_puu42epuu42epuu4.jpg", bg_lo=60, bg_hi=180, max_sat=25)
cleaned.save(r"FACTORY_RESET-main\test_out\puu_cleaned.png")

# Now crop the 6 frames
frame_w = cleaned.width / 6.0
for i in range(6):
    x0 = int(i * frame_w)
    x1 = int((i + 1) * frame_w)
    cell = cleaned.crop((x0, 280, x1, 1080))
    bbox = cell.getbbox()
    if bbox:
        cell = cell.crop(bbox)
    cell.save(rf"FACTORY_RESET-main\test_out\amalgam_walk\clean_walk_{i}.png")

print("Done cleaning full sheet and cropping!")
