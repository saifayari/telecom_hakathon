import os
from PIL import Image
import numpy as np
from scipy import ndimage

def get_bounding_boxes(image_path, bg_lo=0, bg_hi=255, max_sat=20, min_area=500):
    im = Image.open(image_path)
    arr = np.array(im).astype(float)
    h, w, _ = arr.shape
    
    sat = np.max(arr, axis=2) - np.min(arr, axis=2)
    val = np.mean(arr, axis=2)
    
    is_bg_candidate = (sat <= max_sat) & (val >= bg_lo) & (val <= bg_hi)
    
    border_mask = np.zeros((h, w), dtype=bool)
    border_mask[0, :] = True
    border_mask[-1, :] = True
    border_mask[:, 0] = True
    border_mask[:, -1] = True
    
    seeds = border_mask & is_bg_candidate
    bg = ndimage.binary_propagation(seeds, mask=is_bg_candidate)
    fg = ~bg
    
    # Label connected components of foreground
    labeled, num_features = ndimage.label(fg)
    objs = ndimage.find_objects(labeled)
    
    boxes = []
    for idx, sl in enumerate(objs):
        y_slice, x_slice = sl
        area = (y_slice.stop - y_slice.start) * (x_slice.stop - x_slice.start)
        if area >= min_area:
            boxes.append((x_slice.start, y_slice.start, x_slice.stop, y_slice.stop, area))
            
    # Sort boxes left-to-right, top-to-bottom
    boxes.sort(key=lambda b: (b[1] // 100, b[0]))
    return im, fg, boxes

# Test on Unit-R17 walk cycle (monsters_7: Gemini_Generated_Image_puu42epuu42epuu4.jpg)
p_mon = r"art (2)\art\monsters\Gemini_Generated_Image_puu42epuu42epuu4.jpg"
im, fg, boxes = get_bounding_boxes(p_mon, bg_lo=70, bg_hi=160, min_area=5000)
print(f"monsters_7: found {len(boxes)} main sprites")
for i, b in enumerate(boxes):
    print(f"  Frame {i}: box=({b[0]}, {b[1]}, {b[2]}, {b[3]}), w={b[2]-b[0]}, h={b[3]-b[1]}")
