import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Load base preview if exists, or build one
base_day_path = r"FACTORY_RESET-main\assets\sprites\environment\metalslug_arena_with_tower_day.png"
if os.path.exists(base_day_path):
    canvas = Image.open(base_day_path).convert("RGBA")
else:
    # 2048 x 1536
    canvas = Image.new("RGBA", (2048, 1536), (40, 48, 36, 255))

# Crop the central area: center is (1024, 768)
# Let's crop an in-game camera view (640x360 scaled 2x = 1280x720) centered at Sami (1024, 800)
crop_w, crop_h = 1000, 600
cx, cy = 1024, 780
x0 = cx - crop_w // 2
y0 = cy - crop_h // 2
scene = canvas.crop((x0, y0, x0 + crop_w, y0 + crop_h))

ROOT = r"FACTORY_RESET-main\assets\sprites"

def paste_centered(dst, sprite_path, pos_in_scene, scale_f=1.0):
    if not os.path.exists(sprite_path):
        return
    sp = Image.open(sprite_path).convert("RGBA")
    if scale_f != 1.0:
        new_size = (int(sp.width * scale_f), int(sp.height * scale_f))
        sp = sp.resize(new_size, Image.Resampling.LANCZOS)
    px = pos_in_scene[0] - sp.width // 2
    py = pos_in_scene[1] - sp.height // 2
    dst.alpha_composite(sp, (px, py))

# Positions relative to cropped scene center (500, 300)
# Center foundation / Tower base is at (500, 240)
paste_centered(scene, f"{ROOT}/props/power_generator.png", (410, 320), 0.7)
paste_centered(scene, f"{ROOT}/props/workbench_electronics.png", (590, 270), 0.7)
paste_centered(scene, f"{ROOT}/props/workbench_mechanical.png", (600, 340), 0.7)
paste_centered(scene, f"{ROOT}/props/cable_spool.png", (380, 280), 0.7)
paste_centered(scene, f"{ROOT}/props/telecom_junction_box.png", (550, 230), 0.6)

# Scrap Piles
paste_centered(scene, f"{ROOT}/environment/scrap_pile/scrap_pile_inert.png", (360, 360), 0.6)
paste_centered(scene, f"{ROOT}/environment/scrap_pile/scrap_pile_inert.png", (630, 380), 0.6)
paste_centered(scene, f"{ROOT}/environment/scrap_pile/scrap_pile_glow.png", (450, 420), 0.6)

# Turret
paste_centered(scene, f"{ROOT}/turrets/scrap_sentry.png", (570, 390), 0.8)

# AEGIS Drone hovering on upper right
paste_centered(scene, f"{ROOT}/characters/drone/drone_scan_0.png", (620, 180), 0.7)

# Sami Player
paste_centered(scene, f"{ROOT}/characters/sami/sami_shoot.png", (490, 350), 0.5)

# Monster Unit-R17 Scrap Amalgam advancing from bottom-left
paste_centered(scene, f"{ROOT}/monsters/amalgam/amalgam_walk_1.png", (220, 390), 0.6)

# Muzzle flash and bullet
paste_centered(scene, f"{ROOT}/weapons/muzzle_flash.png", (460, 352), 0.5)
paste_centered(scene, f"{ROOT}/weapons/muzzle_flash.png", (350, 365), 0.3)

# Add HUD Overlay
draw = ImageDraw.Draw(scene)
# Top Bar
draw.rectangle([(0, 0), (crop_w, 42)], fill=(15, 18, 24, 230))
draw.line([(0, 42), (crop_w, 42)], fill=(50, 60, 75, 255), width=2)

# Text on HUD
draw.text((15, 12), "DAY 1 - PURIFY SCRAP  00:48", fill=(255, 215, 60))
draw.text((320, 12), "SIGNAL: [||||||||||] 100%", fill=(50, 220, 255))
draw.text((540, 12), "CORE: 1000/1000", fill=(100, 255, 120))

# Resources
paste_centered(scene, f"{ROOT}/icons/icon_scrap.png", (730, 20), 0.5)
draw.text((745, 12), "50", fill=(220, 220, 220))

paste_centered(scene, f"{ROOT}/icons/icon_pure_alloy.png", (800, 20), 0.5)
draw.text((815, 12), "2", fill=(80, 220, 255))

paste_centered(scene, f"{ROOT}/icons/icon_lithium_battery.png", (860, 20), 0.5)
draw.text((875, 12), "1", fill=(60, 240, 200))

# Bottom banner
draw.rectangle([(0, crop_h - 26), (crop_w, crop_h)], fill=(12, 14, 18, 220))
draw.text((15, crop_h - 20), "[WASD] Move Sami  |  [L-Click] Shoot  |  [Hold E] Purify Scrap  |  [F] Trade with AEGIS  |  [TAB] Crafting", fill=(180, 190, 205))

out_preview = r"FACTORY_RESET-main\gameplay_integrated_preview.png"
scene.save(out_preview)
print(f"Saved gameplay integrated preview at {out_preview}")
