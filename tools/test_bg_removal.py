import os
from PIL import Image
import numpy as np
from scipy import ndimage

def remove_checkerboard_bg(img, bg_lo=0, bg_hi=255, max_sat=15):
    arr = np.array(img).astype(float)
    h, w, _ = arr.shape
    
    # Calculate saturation / color difference: max(rgb) - min(rgb)
    sat = np.max(arr, axis=2) - np.min(arr, axis=2)
    val = np.mean(arr, axis=2)
    
    # Candidate background pixels: grey (low saturation) within brightness range
    is_bg_candidate = (sat <= max_sat) & (val >= bg_lo) & (val <= bg_hi)
    
    # We want only the connected component touching the border
    # Create a seed mask touching the borders
    border_mask = np.zeros((h, w), dtype=bool)
    border_mask[0, :] = True
    border_mask[-1, :] = True
    border_mask[:, 0] = True
    border_mask[:, -1] = True
    
    # Only seeds that are actually bg candidates
    seeds = border_mask & is_bg_candidate
    
    # Flood fill / binary dilation to get connected background
    # We can use ndimage.binary_propagation
    bg_connected = ndimage.binary_propagation(seeds, mask=is_bg_candidate)
    
    # Create RGBA
    alpha = np.where(bg_connected, 0, 255).astype(np.uint8)
    
    # Slight edge smoothing / anti-aliasing if needed, or morphological clean
    rgba = np.dstack([np.array(img), alpha])
    return Image.fromarray(rgba)

# Test on Sami
im_sami = Image.open(r"art (2)\art\agent_new\Gemini_Generated_Image_8ezuri8ezuri8ezu (1).jpg")
res_sami = remove_checkerboard_bg(im_sami, bg_lo=130, bg_hi=220, max_sat=18)
os.makedirs(r"FACTORY_RESET-main\test_out", exist_ok=True)
res_sami.save(r"FACTORY_RESET-main\test_out\sami_clean.png")

# Test on Monster
im_mon = Image.open(r"art (2)\art\monsters\Gemini_Generated_Image_a7f8nwa7f8nwa7f8.jpg")
res_mon = remove_checkerboard_bg(im_mon, bg_lo=70, bg_hi=175, max_sat=18)
res_mon.save(r"FACTORY_RESET-main\test_out\monster_clean.png")

print("Saved test_out images successfully!")
