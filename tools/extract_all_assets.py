import os
from PIL import Image
import numpy as np
from scipy import ndimage

def clean_rgba(im, bg_lo=20, bg_hi=220, max_sat=20):
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
    rgba = np.dstack([np.array(im), alpha])
    return Image.fromarray(rgba)

def crop_and_save(img, box, out_path, max_dim=None):
    c = img.crop(box)
    bbox = c.getbbox()
    if bbox:
        c = c.crop(bbox)
    if max_dim:
        c.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    c.save(out_path)
    print(f"Saved: {out_path} ({c.size})")

ROOT = r"FACTORY_RESET-main\assets\sprites"
ART = r"art (2)\art"

print("Starting master asset extraction...")

# ============================================================
# 1. SAMI (PLAYER) SPRITES
# ============================================================
# agent_new_0: Gemini_Generated_Image_8ezuri8ezuri8ezu (1).jpg (2752x1536)
im_sami = clean_rgba(Image.open(os.path.join(ART, r"agent_new\Gemini_Generated_Image_8ezuri8ezuri8ezu (1).jpg")), bg_lo=130, bg_hi=220)

# Idle front / side
crop_and_save(im_sami, (580, 20, 750, 240), f"{ROOT}/characters/sami/sami_idle.png", max_dim=96)
# Aim / Shoot
crop_and_save(im_sami, (1000, 240, 1260, 480), f"{ROOT}/characters/sami/sami_shoot.png", max_dim=96)
# Aiming stance
crop_and_save(im_sami, (200, 20, 400, 240), f"{ROOT}/characters/sami/sami_aim.png", max_dim=96)

# Sami Walk (from agent_new_6: Gemini_Generated_Image_cmjisxcmjisxcmji (1).jpg - 2752x1536)
im_sami_walk = clean_rgba(Image.open(os.path.join(ART, r"agent_new\Gemini_Generated_Image_cmjisxcmjisxcmji (1).jpg")), bg_lo=130, bg_hi=220)
# Top row: Sprinting South (6 frames)
walk_boxes = [
    (40, 70, 240, 270),
    (240, 70, 440, 270),
    (440, 70, 640, 270),
    (640, 70, 840, 270),
    (840, 70, 1040, 270),
    (1040, 70, 1240, 270)
]
for i, wb in enumerate(walk_boxes[:4]):
    crop_and_save(im_sami_walk, wb, f"{ROOT}/characters/sami/sami_walk_{i}.png", max_dim=96)

# Sami Technician Welding / Repair (from agent_new_3: Gemini_Generated_Image_8qlfnd8qlfnd8qlf (1).jpg)
im_sami_tech = clean_rgba(Image.open(os.path.join(ART, r"agent_new\Gemini_Generated_Image_8qlfnd8qlfnd8qlf (1).jpg")), bg_lo=130, bg_hi=220)
# Tightening / Multimeter / Circuit repair
crop_and_save(im_sami_tech, (760, 220, 960, 430), f"{ROOT}/characters/sami/sami_weld.png", max_dim=96)
crop_and_save(im_sami_tech, (760, 10, 960, 220), f"{ROOT}/characters/sami/sami_repair.png", max_dim=96)

# ============================================================
# 2. MONSTER (UNIT-R17 SCRAP AMALGAM)
# ============================================================
# monsters_7: Gemini_Generated_Image_puu42epuu42epuu4.jpg (3168x1344)
im_mon_walk = clean_rgba(Image.open(os.path.join(ART, r"monsters\Gemini_Generated_Image_puu42epuu42epuu4.jpg")), bg_lo=30, bg_hi=180)
fw = im_mon_walk.width / 6.0
for i in range(6):
    crop_and_save(im_mon_walk, (int(i*fw), 280, int((i+1)*fw), 1080), f"{ROOT}/monsters/amalgam/amalgam_walk_{i}.png", max_dim=160)

# Idle front from monsters_5: Gemini_Generated_Image_mebcbfmebcbfmebc.jpg (2816x1536)
im_mon_idle = clean_rgba(Image.open(os.path.join(ART, r"monsters\Gemini_Generated_Image_mebcbfmebcbfmebc.jpg")), bg_lo=30, bg_hi=180)
crop_and_save(im_mon_idle, (600, 150, 2200, 1400), f"{ROOT}/monsters/amalgam/amalgam_idle.png", max_dim=160)

# Attack Smash from monsters_2: Gemini_Generated_Image_gbfa28gbfa28gbfa.jpg (3168x1344)
im_mon_atk = clean_rgba(Image.open(os.path.join(ART, r"monsters\Gemini_Generated_Image_gbfa28gbfa28gbfa.jpg")), bg_lo=30, bg_hi=180)
fw_atk = im_mon_atk.width / 5.0
for i in range(4):
    crop_and_save(im_mon_atk, (int(i*fw_atk), 250, int((i+1)*fw_atk), 1100), f"{ROOT}/monsters/amalgam/amalgam_attack_{i}.png", max_dim=160)

# Hit reaction / stunned
crop_and_save(im_mon_atk, (int(4*fw_atk), 250, int(5*fw_atk), 1100), f"{ROOT}/monsters/amalgam/amalgam_hit.png", max_dim=160)

# ============================================================
# 3. SCRAP PILE & NANO AWAKENING / MUTATION
# ============================================================
# monsters_6: Gemini_Generated_Image_niobamniobamniob.jpg (2752x1536)
im_scrap_sheet = Image.open(os.path.join(ART, r"monsters\Gemini_Generated_Image_niobamniobamniob.jpg"))
# 8 frames: 4 on top, 4 on bottom
# Row 0: 0=inert scrap, 1=slight green glow, 2=spores sprouting, 3=active nano swarm
sw = im_scrap_sheet.width / 4.0
sh = im_scrap_sheet.height / 2.0
# Frame 0: Inert scrap pile
crop_and_save(im_scrap_sheet, (int(0*sw), int(0*sh), int(1*sw), int(1*sh)), f"{ROOT}/environment/scrap_pile/scrap_pile_inert.png", max_dim=96)
# Frame 1: Awakening glow
crop_and_save(im_scrap_sheet, (int(1*sw), int(0*sh), int(2*sw), int(1*sh)), f"{ROOT}/environment/scrap_pile/scrap_pile_glow.png", max_dim=96)
# Frame 2: Spores
crop_and_save(im_scrap_sheet, (int(2*sw), int(0*sh), int(3*sw), int(1*sh)), f"{ROOT}/environment/scrap_pile/scrap_pile_spores.png", max_dim=96)
# Frame 3: Violent Nano Eruption / Mutation
crop_and_save(im_scrap_sheet, (int(3*sw), int(0*sh), int(4*sw), int(1*sh)), f"{ROOT}/environment/scrap_pile/scrap_pile_erupting.png", max_dim=96)

# ============================================================
# 4. AEGIS AUTONOMOUS DRONE
# ============================================================
# Drone_1: Gemini_Generated_Image_4ti7g44ti7g44ti7.jpg (2816x1536)
im_drone_sheet = clean_rgba(Image.open(os.path.join(ART, r"Drone\Gemini_Generated_Image_4ti7g44ti7g44ti7.jpg")), bg_lo=10, bg_hi=120)
# Top row has drone hover frames
dw = 280
dh = 200
# 4 hover frames
for i in range(4):
    crop_and_save(im_drone_sheet, (60 + i*260, 20, 60 + (i+1)*260, 220), f"{ROOT}/characters/drone/drone_idle_{i}.png", max_dim=96)

# Scan beam / laser harvester frames (row 2 / row 3)
for i in range(4):
    crop_and_save(im_drone_sheet, (60 + i*260, 480, 60 + (i+1)*260, 720), f"{ROOT}/characters/drone/drone_scan_{i}.png", max_dim=112)

# ============================================================
# 5. WEAPONS, PROJECTILES & VFX
# ============================================================
# Gun_1: Machine gun (Gemini_Generated_Image_7mt0ri7mt0ri7mt0.jpg)
im_gun1 = clean_rgba(Image.open(os.path.join(ART, r"Gun\Gemini_Generated_Image_7mt0ri7mt0ri7mt0.jpg")), bg_lo=80, bg_hi=180)
# Main weapon
crop_and_save(im_gun1, (50, 70, 550, 300), f"{ROOT}/weapons/gun_rifle.png", max_dim=80)
# Muzzle flash
crop_and_save(im_gun1, (650, 390, 850, 520), f"{ROOT}/weapons/muzzle_flash.png", max_dim=48)

# Gun_2: RF Resonator / Welder (Gemini_Generated_Image_b9btccb9btccb9bt.jpg)
im_gun2 = clean_rgba(Image.open(os.path.join(ART, r"Gun\Gemini_Generated_Image_b9btccb9btccb9bt.jpg")), bg_lo=80, bg_hi=180)
crop_and_save(im_gun2, (70, 40, 780, 260), f"{ROOT}/weapons/gun_welder.png", max_dim=80)
# Blue EM Discharge / Shockwave ring (#10)
crop_and_save(im_gun2, (1550, 360, 1850, 540), f"{ROOT}/weapons/shockwave_ring.png", max_dim=128)
# EM projectile burst (#09)
crop_and_save(im_gun2, (1200, 390, 1500, 530), f"{ROOT}/weapons/emp_burst.png", max_dim=64)

# ============================================================
# 6. RESOURCE & CRAFTING ICONS
# ============================================================
# Gun_0: Gemini_Generated_Image_1tg6gq1tg6gq1tg6.jpg (2752x1536)
im_icons = clean_rgba(Image.open(os.path.join(ART, r"Gun\Gemini_Generated_Image_1tg6gq1tg6gq1tg6.jpg")), bg_lo=80, bg_hi=180)
# Row 0: Resources
# 01 Recycled scrap (50, 40, 450, 230)
crop_and_save(im_icons, (60, 40, 420, 230), f"{ROOT}/icons/icon_scrap.png", max_dim=48)
# 02 Copper wire (550, 40, 800, 230)
crop_and_save(im_icons, (520, 40, 780, 230), f"{ROOT}/icons/icon_copper_coil.png", max_dim=48)
# 03 Metal pipe (850, 40, 1150, 230)
crop_and_save(im_icons, (840, 40, 1140, 230), f"{ROOT}/icons/icon_metal_pipe.png", max_dim=48)
# 04 PCB (1200, 40, 1500, 230)
crop_and_save(im_icons, (1200, 40, 1500, 230), f"{ROOT}/icons/icon_pcb.png", max_dim=48)
# 05 Battery Cell (1550, 40, 1780, 230)
crop_and_save(im_icons, (1550, 40, 1780, 230), f"{ROOT}/icons/icon_lithium_battery.png", max_dim=48)
# 06 Induction coil / Transformer (1800, 40, 2100, 230)
crop_and_save(im_icons, (1800, 40, 2100, 230), f"{ROOT}/icons/icon_induction_coil.png", max_dim=48)
# 07 Scrap armor plate (2120, 40, 2400, 230)
crop_and_save(im_icons, (2120, 40, 2400, 230), f"{ROOT}/icons/icon_composite_armor.png", max_dim=48)

# Row 1: UI icons
# 13 Hammer & wrench
crop_and_save(im_icons, (1620, 560, 1920, 800), f"{ROOT}/icons/icon_craft_tools.png", max_dim=48)
# 14 Upgrade chevrons
crop_and_save(im_icons, (2020, 560, 2300, 800), f"{ROOT}/icons/icon_upgrade.png", max_dim=48)

# Drone_0: High-Tech Items (Gemini_Generated_Image_3k4k3k3k4k3k3k4k.jpg - 2816x1536)
im_hi_tech = clean_rgba(Image.open(os.path.join(ART, r"Drone\Gemini_Generated_Image_3k4k3k3k4k3k3k4k.jpg")), bg_lo=20, bg_hi=90)
# 1 Nano core crystal
crop_and_save(im_hi_tech, (120, 100, 600, 680), f"{ROOT}/icons/icon_nano_core.png", max_dim=48)
# 3 EMP Reactor Core
crop_and_save(im_hi_tech, (1400, 120, 2050, 680), f"{ROOT}/icons/icon_emp_pulsar.png", max_dim=48)
# 7 Pure Alloy Resonance Crystal
crop_and_save(im_hi_tech, (1500, 850, 2000, 1400), f"{ROOT}/icons/icon_pure_alloy.png", max_dim=48)
# 8 Telecom Radio Transceiver
crop_and_save(im_hi_tech, (2150, 850, 2750, 1400), f"{ROOT}/icons/icon_transceiver.png", max_dim=48)

# ============================================================
# 7. WORKSHOP & ENVIRONMENT PROPS
# ============================================================
# Craft_new_0: Workbenches (Gemini_Generated_Image_81c2sx81c2sx81c2 (3).jpg)
im_craft_bench = clean_rgba(Image.open(os.path.join(ART, r"Craft_new\Gemini_Generated_Image_81c2sx81c2sx81c2 (3).jpg")), bg_lo=130, bg_hi=220)
# Storage crate
crop_and_save(im_craft_bench, (80, 100, 420, 430), f"{ROOT}/props/storage_crate.png", max_dim=64)
# Workshop cabinet
crop_and_save(im_craft_bench, (900, 80, 1300, 440), f"{ROOT}/props/tool_cabinet.png", max_dim=80)

# Craft_new_1: Electronics soldering table (Gemini_Generated_Image_81c2sx81c2sx81c2.jpg)
im_bench1 = clean_rgba(Image.open(os.path.join(ART, r"Craft_new\Gemini_Generated_Image_81c2sx81c2sx81c2.jpg")), bg_lo=130, bg_hi=220)
# Electronics bench with lamp
crop_and_save(im_bench1, (80, 460, 780, 830), f"{ROOT}/props/workbench_electronics.png", max_dim=96)
# Mechanical assembly table with gears
crop_and_save(im_bench1, (100, 960, 1100, 1450), f"{ROOT}/props/workbench_mechanical.png", max_dim=112)

# Craft_new_3: Defensive Traps & Barricades (Gemini_Generated_Image_t7hv3st7hv3st7hv (1).jpg)
im_traps = clean_rgba(Image.open(os.path.join(ART, r"Craft_new\Gemini_Generated_Image_t7hv3st7hv3st7hv (1).jpg")), bg_lo=130, bg_hi=220)
# Steel spike wall / barricade
crop_and_save(im_traps, (1450, 60, 1850, 400), f"{ROOT}/props/barricade_spikes.png", max_dim=80)
# Wire barricade
crop_and_save(im_traps, (1450, 520, 1850, 780), f"{ROOT}/props/barricade_wire.png", max_dim=80)

# night_back_0: Cable spools & utility items (Gemini_Generated_Image_1mqpy91mqpy91mqp.jpg)
im_utility = clean_rgba(Image.open(os.path.join(ART, r"night_back\Gemini_Generated_Image_1mqpy91mqpy91mqp.jpg")), bg_lo=130, bg_hi=220)
# Wooden cable spool
crop_and_save(im_utility, (40, 20, 270, 260), f"{ROOT}/props/cable_spool.png", max_dim=64)
# Telecom junction box
crop_and_save(im_utility, (40, 320, 250, 540), f"{ROOT}/props/telecom_junction_box.png", max_dim=64)

# day_back_1: Power generator & server console (Gemini_Generated_Image_7322hd7322hd7322.jpg)
im_server = clean_rgba(Image.open(os.path.join(ART, r"day_back\Gemini_Generated_Image_7322hd7322hd7322.jpg")), bg_lo=130, bg_hi=220)
# Heavy generator / turbine
crop_and_save(im_server, (750, 1020, 1250, 1430), f"{ROOT}/props/power_generator.png", max_dim=96)
# Computer terminal with dual CRT screens
crop_and_save(im_server, (1450, 1030, 1950, 1420), f"{ROOT}/props/tower_terminal.png", max_dim=80)

print("\nAll assets extracted and optimized successfully into FACTORY_RESET-main/assets/sprites/!")
