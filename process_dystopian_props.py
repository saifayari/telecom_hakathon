import os
import numpy as np
from PIL import Image

im = Image.open('clean_props_sheet.png')

# 1. Toxic Barrel (x: 20 to 450, y: 30 to 410)
b1 = im.crop((20, 30, 450, 410))
b1 = b1.crop(b1.getbbox())

# 2. Barricade (x: 480 to 990, y: 20 to 370 - avoid antenna wire at bottom)
b2 = im.crop((480, 20, 990, 365))
b2 = b2.crop(b2.getbbox())

# 3. Surveillance Pylon (x: 1070 to 1285, y: 25 to 370 - avoid drum at bottom)
b3 = im.crop((1070, 25, 1285, 365))
b3 = b3.crop(b3.getbbox())

# 4. E-Waste Pile (x: 40 to 620, y: 440 to 765)
b4 = im.crop((40, 440, 620, 765))
b4 = b4.crop(b4.getbbox())

# 5. Rusted Oil Drum (x: 1080 to 1320, y: 450 to 765)
b5 = im.crop((1080, 450, 1320, 765))
b5 = b5.crop(b5.getbbox())

def clean_internal_white(img):
    arr = np.array(img).convert('RGBA') if hasattr(img, 'convert') else np.array(img)
    mask = (arr[:, :, 0] > 235) & (arr[:, :, 1] > 235) & (arr[:, :, 2] > 235)
    arr[mask, 3] = 0
    return Image.fromarray(arr)

b1 = clean_internal_white(b1)
b2 = clean_internal_white(b2)
b3 = clean_internal_white(b3)
b4 = clean_internal_white(b4)
b5 = clean_internal_white(b5)

# Target scales:
p1_d = b1.resize((96, 76), Image.Resampling.NEAREST)
p2_d = b2.resize((128, 96), Image.Resampling.NEAREST)
p3_d = b3.resize((48, 96), Image.Resampling.NEAREST)
p4_d = b4.resize((128, 68), Image.Resampling.NEAREST)
p5_d = b5.resize((40, 56), Image.Resampling.NEAREST)

os.makedirs('assets/sprites/environment/dystopian', exist_ok=True)

# Save Day versions
p1_d.save('assets/sprites/environment/dystopian/prop_toxic_barrel_day.png')
p2_d.save('assets/sprites/environment/dystopian/prop_scrap_barricade_day.png')
p3_d.save('assets/sprites/environment/dystopian/prop_surveillance_day.png')
p4_d.save('assets/sprites/environment/dystopian/prop_ewaste_day.png')
p5_d.save('assets/sprites/environment/dystopian/prop_drum_day.png')

# ----------------- CREATE NIGHT VERSIONS -----------------

# Helper for basic nocturnal shift
def night_shift(img):
    arr = np.array(img).astype(float)
    alpha = arr[:, :, 3]
    rgb = arr[:, :, :3]
    lum = (0.299 * rgb[:,:,0] + 0.587 * rgb[:,:,1] + 0.114 * rgb[:,:,2]) / 255.0
    c_dark = np.array([14, 18, 22])
    c_mid = np.array([32, 42, 50])
    c_light = np.array([65, 82, 95])
    night_base = np.where(lum[:,:,None] < 0.5,
                          c_dark + (c_mid - c_dark) * (lum[:,:,None] / 0.5),
                          c_mid + (c_light - c_mid) * ((lum[:,:,None] - 0.5) / 0.5))
    out = np.zeros_like(arr)
    out[:, :, :3] = np.clip(night_base, 0, 255)
    out[:, :, 3] = alpha
    return out

# 1. Toxic Barrel Night: Glowing radioactive green acid!
arr_p1 = night_shift(p1_d)
arr_p1_orig = np.array(p1_d)
for y in range(arr_p1.shape[0]):
    for x in range(arr_p1.shape[1]):
        if arr_p1_orig[y, x, 3] > 0:
            r, g, b = arr_p1_orig[y, x, :3]
            # Acid pixels are green (g > 130, g > r)
            if g > 110 and g > r:
                arr_p1[y, x, :3] = [40, 255, 60] # intense radioactive neon green!
            elif g > 60 and g > r * 0.9:
                arr_p1[y, x, :3] = [15, 180, 40]
Image.fromarray(arr_p1.astype(np.uint8)).save('assets/sprites/environment/dystopian/prop_toxic_barrel_night.png')

# 2. Scrap Barricade Night
arr_p2 = night_shift(p2_d)
Image.fromarray(arr_p2.astype(np.uint8)).save('assets/sprites/environment/dystopian/prop_scrap_barricade_night.png')

# 3. Surveillance Night: Glowing red camera eye!
arr_p3 = night_shift(p3_d)
arr_p3_orig = np.array(p3_d)
# Camera eye is around top left
for y in range(int(arr_p3.shape[0] * 0.35)):
    for x in range(int(arr_p3.shape[1] * 0.45)):
        if arr_p3_orig[y, x, 3] > 0:
            r, g, b = arr_p3_orig[y, x, :3]
            if r > 120 and b < 60:
                arr_p3[y, x, :3] = [255, 40, 10] # red surveillance lens
Image.fromarray(arr_p3.astype(np.uint8)).save('assets/sprites/environment/dystopian/prop_surveillance_night.png')

# 4. E-Waste Night: Flickering cyan & green LEDs
arr_p4 = night_shift(p4_d)
arr_p4_orig = np.array(p4_d)
for y in range(arr_p4.shape[0]):
    for x in range(arr_p4.shape[1]):
        if arr_p4_orig[y, x, 3] > 0:
            r, g, b = arr_p4_orig[y, x, :3]
            # Circuit board green
            if g > 70 and g > r * 1.2:
                if (x + y) % 5 == 0:
                    arr_p4[y, x, :3] = [0, 240, 255] # cyan micro-LED
                elif (x + y) % 5 == 1:
                    arr_p4[y, x, :3] = [50, 255, 80] # green micro-LED
Image.fromarray(arr_p4.astype(np.uint8)).save('assets/sprites/environment/dystopian/prop_ewaste_night.png')

# 5. Drum Night
arr_p5 = night_shift(p5_d)
Image.fromarray(arr_p5.astype(np.uint8)).save('assets/sprites/environment/dystopian/prop_drum_night.png')

print('All 5 dystopian props saved with Day and Night pairs!')
