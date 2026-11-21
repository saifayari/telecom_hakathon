import os
from PIL import Image
import numpy as np
from scipy import ndimage

ART = r"art (2)\art\agent_new"
OUT = r"FACTORY_RESET-main\assets\sprites\characters\sami"
os.makedirs(OUT, exist_ok=True)

def clean_rgba(im, bg_lo=100, bg_hi=220, max_sat=25):
    arr = np.array(im).astype(float)
    h, w, _ = arr.shape
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
    bg_conn = ndimage.binary_dilation(bg_conn, iterations=1)
    alpha = np.where(bg_conn, 0, 255).astype(np.uint8)
    return Image.fromarray(np.dstack([np.array(im), alpha]))

def extract_single_component(crop_img):
    """Ensure strictly ONE connected component (the main character), removing any neighbor stray pixels."""
    arr = np.array(crop_img)
    if arr.shape[2] != 4:
        return crop_img
    mask = arr[:, :, 3] > 20
    lbl, num = ndimage.label(mask)
    if num <= 1:
        return crop_img
    
    objs = ndimage.find_objects(lbl)
    # Find the largest component by area
    largest_idx = 0
    max_area = 0
    for idx, o in enumerate(objs):
        area = (lbl[o] == (idx + 1)).sum()
        if area > max_area:
            max_area = area
            largest_idx = idx + 1
            
    # Zero out all other components
    clean_alpha = np.where(lbl == largest_idx, arr[:, :, 3], 0).astype(np.uint8)
    arr[:, :, 3] = clean_alpha
    return Image.fromarray(arr)

def make_uniform_frame(crop_img, canvas_size=(96, 96), target_h=72):
    # 1. Isolate strictly 1 character
    clean_single = extract_single_component(crop_img)
    
    # 2. Crop tight bbox
    bbox = clean_single.getbbox()
    if not bbox:
        return Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    c = clean_single.crop(bbox)
    
    # 3. Scale height proportionally to target_h
    scale = target_h / float(c.height)
    new_w = max(1, int(round(c.width * scale)))
    new_h = target_h
    c = c.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # 4. Center horizontally, anchor near bottom
    canvas = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    paste_x = (canvas_size[0] - new_w) // 2
    paste_y = canvas_size[1] - 8 - new_h # 8px margin from bottom
    canvas.paste(c, (paste_x, paste_y), c)
    return canvas

print("1. Extracting walk cycle frames from cmjisxcmjisxcmji (1).jpg...")
sheet_walk = clean_rgba(Image.open(os.path.join(ART, "Gemini_Generated_Image_cmjisxcmjisxcmji (1).jpg")))
walk_boxes = [
    (58, 98, 195, 273),
    (236, 98, 367, 275),
    (408, 98, 542, 272),
    (570, 99, 706, 275),
    (751, 99, 885, 277),
    (931, 98, 1069, 275)
]

for i, wb in enumerate(walk_boxes):
    raw = sheet_walk.crop(wb)
    frame = make_uniform_frame(raw, canvas_size=(96, 96), target_h=72)
    out_file = os.path.join(OUT, f"sami_walk_{i}.png")
    frame.save(out_file)
    print(f"Saved: {out_file} (size={frame.size})")

print("2. Extracting idle frame from 8ezuri8ezuri8ezu (1).jpg...")
sheet_idle = clean_rgba(Image.open(os.path.join(ART, "Gemini_Generated_Image_8ezuri8ezuri8ezu (1).jpg")))
raw_idle = sheet_idle.crop((590, 30, 713, 215))
frame_idle = make_uniform_frame(raw_idle, canvas_size=(96, 96), target_h=72)
frame_idle.save(os.path.join(OUT, "sami_idle.png"))
print("Saved: sami_idle.png")

print("3. Extracting shoot frame from 8ezuri8ezuri8ezu (1).jpg...")
raw_shoot = sheet_idle.crop((1019, 280, 1260, 449))
frame_shoot = make_uniform_frame(raw_shoot, canvas_size=(96, 96), target_h=72)
frame_shoot.save(os.path.join(OUT, "sami_shoot.png"))
print("Saved: sami_shoot.png")

print("4. Extracting weld frame from 8qlfnd8qlfnd8qlf (1).jpg...")
sheet_weld = clean_rgba(Image.open(os.path.join(ART, "Gemini_Generated_Image_8qlfnd8qlfnd8qlf (1).jpg")))
raw_weld = sheet_weld.crop((765, 238, 945, 426))
frame_weld = make_uniform_frame(raw_weld, canvas_size=(96, 96), target_h=72)
frame_weld.save(os.path.join(OUT, "sami_weld.png"))
print("Saved: sami_weld.png")

# Remove any old conflicting sami_walk.png strip if present
old_strip = os.path.join(OUT, "sami_walk.png")
if os.path.exists(old_strip):
    os.remove(old_strip)
    print("Removed obsolete 16-frame strip sami_walk.png")
old_strip_import = os.path.join(OUT, "sami_walk.png.import")
if os.path.exists(old_strip_import):
    os.remove(old_strip_import)
    print("Removed obsolete sami_walk.png.import")

print("SUCCESS: All Sami frames extracted and normalized to exactly 1 single agent per frame!")
