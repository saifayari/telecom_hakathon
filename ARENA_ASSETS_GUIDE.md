# 🪖 Metal Slug Wasteland Arena Assets Guide (دليل أصول مساحة اللعب - نمط ميتال سلاج)
**Project:** FACTORY RESET — Act 1: The Tower Base  
**Setting:** Ground-level Post-Apocalyptic Military Wasteland & Forest Edge  
**Art Style:** Gritty 90s SNK Metal Slug / Presentation Aesthetic (32x32 Grid)  
**Day/Night System:** Shader-Free Dual Texture Swap (Direct Asset Swap via Code)  

---

## 🎯 Overview & Design Philosophy

The play arena matches the authentic aesthetic of **Metal Slug** and the **official project presentation mockups** (`gameplay_arena_day.png`, `gameplay_arena_night.png`, `lore_universe_tower.png`). It is an open military ground clearing with distressed earth, weathered steel plates, and gnarled post-apocalyptic forest trees framing the battlefield.

### Core Map Specifications:
* **Size:** Expanded large battlefield of **64 columns × 48 rows (2048 × 1536 pixels)**.
* **Empty Play Space for Incremental Building:** The entire interior battlefield is completely open and clean, with **NOTHING in it except the central tower foundation clearing**. Turrets, barricades, and defenses will be introduced step-by-step as instructed by the user.
* **Sparse Perimeter Natural Framing:** Reduced from 70 dense trees down to **14 sparse landmark trees and weathered stumps** spaced wide apart along the outer borders (~400-600 px apart), keeping the wasteland open, desolate, and uncluttered with Y-sorting and collision shapes.

---

## 🎨 Day vs Night Dual Asset System

Every part of the map has two distinct hand-crafted versions swapped directly at runtime without any programmatic shaders or CanvasModulate:

1. **Day Palette (Warm Military Olive & Weathered Rust):**
   * **Earth & Soil:** Earthy olive-drab khaki dirt (`#687256`, `#4e5640`, `#8a9674`).
   * **Metal & Concrete:** Weathered military gray steel (`#5c605a`, `#80847c`) with orange oxidized rust patches (`#8a4826`) and industrial hazard yellow chevrons (`#c39b23`).
   * **Foliage:** Olive-drab and khaki leaves with deep shadow clusters (`#192014` to `#879b4e`).
   * **Trunks:** Weathered dark post-apocalyptic timber (`#18120e` to `#7d5c3a`).

2. **Night Palette (Nocturnal Slate-Teal & Cyber Neon):**
   * **Earth & Soil:** Deep nocturnal slate-olive ground (`#2a3026`, `#1a1e18`).
   * **Metal & Concrete:** Cold midnight steel (`#1e242a`, `#343e48`).
   * **Foliage:** Deep midnight slate with cold moonlit rim highlights (`#0c1212`, `#1c2d2a`, `#375850`).
   * **Conduits & Status Nodes:** Electric cyan glow (`#00f0ff`) pulsing along power conduits to the tower collar.
   * **Beacon Nodes:** High-visibility amber LEDs (`#ff8c00`) at the perimeter corners.

---

## 📦 Assets Catalog

### 1. Master Ground Tileset (256x128 px, 32x32 Tiles, 8 Cols × 4 Rows)
* **Day Tileset:** [metalslug_tileset_day.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/metalslug_tileset_day.png)
* **Night Tileset:** [metalslug_tileset_night.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/metalslug_tileset_night.png)
* **Godot TileSet Resource:** [nature_tileset.tres](file:///home/askri/Projects/FACTORY_RESET/scenes/environment/nature_tileset.tres)

#### Tiles Breakdown:
* **Row 0: Wasteland Earth & Ground Textures:**
  * `(0, 0)`: Base Wasteland Dirt (seamless organic soil texture).
  * `(1, 0)`: Fissure & Dry Mud Fractures (cracked wasteland earth).
  * `(2, 0)`: Gravel & Small Rocks (scattered stones and pebbles).
  * `(3, 0)`: Olive Weed Tufts (hardy post-apocalyptic vegetation).
  * `(4, 0)`: Embedded Metal Scrap Plate with Rivets (sunken industrial plate).
  * `(5, 0)`: Crawler / Vehicle Tread Mark (heavy tread imprints).
  * `(6, 0)`: Rusted Scrap Shards (metal debris embedded in soil).
  * `(7, 0)`: Scorched Earth Crater (dark charred crater spot).
* **Row 1: Central Foundation Outer Edges:**
  * `(0, 1)`: Platform Top-Left Corner (steel border with hazard stripes & beacon).
  * `(1, 1)`: Platform Top Edge (hazard warning trim).
  * `(2, 1)`: Platform Top-Right Corner (hazard stripes & beacon).
  * `(3, 1)`: Platform Left Edge (hazard warning trim).
  * `(4, 1)`: Platform Inner Floor Plate (reinforced steel plate with 4-corner rivets).
  * `(5, 1)`: Platform Right Edge (hazard warning trim).
  * `(6, 1)`: Platform Bottom-Left Corner (hazard stripes & beacon).
  * `(7, 1)`: Platform Bottom Edge (hazard warning trim).
* **Row 2: Power Conduits & Central Tower Socket:**
  * `(0, 2)`: Platform Bottom-Right Corner (hazard stripes & beacon).
  * `(1, 2)`: Power Conduit Horizontal (Day: copper/steel; Night: glowing cyan energy line).
  * `(2, 2)`: Power Conduit Vertical (Day: copper/steel; Night: glowing cyan energy line).
  * `(3, 2)`: Power Conduit Cross Junction (distribution junction box).
  * `(4, 2)`: Central Tower Mounting Socket (empty circular collar reserved for the tower!).
  * `(5, 2)`: Heavy Ventilation Grate (industrial airflow grate).
  * `(6, 2)`: Conduit Cable Terminus.
  * `(7, 2)`: Warning Beacon Mount Pad (Day: hazard yellow; Night: glowing amber LED).
* **Row 3: Perimeter Barricades & Extra Ground Variations:**
  * `(0, 3)`: Scrap Wire Fence Post (wood post with barbed wire).
  * `(1, 3)`: Scrap Wire Fence Horizontal (barbed wire strands).
  * `(2, 3)`: Corrugated Scrap Sheet Barricade (heavy corrugated sheet metal).
  * `(3, 3)`: Reinforced Corner Post.
  * `(4, 3) - (6, 3)`: Organic Ground Dirt Variations 2, 3, 4.
  * `(7, 3)`: Crater Rim Border.

---

### 2. Standalone Trees & Nature Props
* **Ancient Wasteland Oak (130x165 px):**
  * Day: [tree_oak_large_day.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/tree_oak_large_day.png)
  * Night: [tree_oak_large_night.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/tree_oak_large_night.png)
  * Massive spreading oak with gnarled roots anchoring into the dirt.
* **Gnarled Medium Oak (96x108 px):**
  * Day: [tree_oak_med_day.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/tree_oak_med_day.png)
  * Night: [tree_oak_med_night.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/tree_oak_med_night.png)
  * Twisted trunk with heavy SNK-style shading and olive leaf clusters.
* **Wasteland Pine Tree (64x140 px):**
  * Day: [tree_pine_day.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/tree_pine_day.png)
  * Night: [tree_pine_night.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/tree_pine_night.png)
  * Tall rugged coniferous pine with tiered needle boughs.
* **Scorched Dead Tree (96x116 px):**
  * Day: [tree_dead_day.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/tree_dead_day.png)
  * Night: [tree_dead_night.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/tree_dead_night.png)
  * Leafless gnarled trunk with broken limbs and knotholes (classic battlefield silhouette).
* **Tree Stump (48x48 px):**
  * Day: [tree_stump_day.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/tree_stump_day.png)
  * Night: [tree_stump_night.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/tree_stump_night.png)

### 3. Dystopian Wasteland Props & Environmental Hazards (AI-Generated & Hand-Tuned)
* **Toxic Chemical Drum / Sludge Spill (96x76 px):**
  * Day: [prop_toxic_barrel_day.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/dystopian/prop_toxic_barrel_day.png)
  * Night: [prop_toxic_barrel_night.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/dystopian/prop_toxic_barrel_night.png)
  * Rusted biohazard drum leaking acid into a puddle (Day: pungent yellow-green; Night: intense radioactive neon glow).
* **Scrap Metal & Barbed Wire Barricade (128x96 px):**
  * Day: [prop_scrap_barricade_day.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/dystopian/prop_scrap_barricade_day.png)
  * Night: [prop_scrap_barricade_night.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/dystopian/prop_scrap_barricade_night.png)
  * Improvised defensive wall crafted from welded vehicle armor, truck tires, and coiled razor wire.
* **Surveillance Camera Tripod / Sensor Post (48x96 px):**
  * Day: [prop_surveillance_day.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/dystopian/prop_surveillance_day.png)
  * Night: [prop_surveillance_night.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/dystopian/prop_surveillance_night.png)
  * Tripod-mounted CCTV lens tracking movement (Day: matte military lens; Night: ominous ruby-red scanning laser optic).
* **E-Waste & Circuit Scrap Heap (128x68 px):**
  * Day: [prop_ewaste_day.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/dystopian/prop_ewaste_day.png)
  * Night: [prop_ewaste_night.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/dystopian/prop_ewaste_night.png)
  * Dumped cathode-ray monitors, cracked motherboard PCBs, drone frames (Night: blinking micro-LEDs & cyan circuitry).
* **Reinforced Steel Drum / Hazard Barrel (40x56 px):**
  * Day: [prop_drum_day.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/dystopian/prop_drum_day.png)
  * Night: [prop_drum_night.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/dystopian/prop_drum_night.png)
  * Industrial 55-gallon container with biohazard stenciling and heavy bullet dents.

### 3. Dystopian Wasteland Props & Environmental Hazards (AI-Generated & Hand-Tuned)
* **Toxic Chemical Drum / Sludge Spill (96x76 px):**
  * Day: [prop_toxic_barrel_day.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/dystopian/prop_toxic_barrel_day.png)
  * Night: [prop_toxic_barrel_night.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/dystopian/prop_toxic_barrel_night.png)
  * Rusted biohazard drum leaking acid into a puddle (Day: pungent yellow-green; Night: intense radioactive neon glow).
* **Scrap Metal & Barbed Wire Barricade (128x96 px):**
  * Day: [prop_scrap_barricade_day.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/dystopian/prop_scrap_barricade_day.png)
  * Night: [prop_scrap_barricade_night.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/dystopian/prop_scrap_barricade_night.png)
  * Improvised defensive wall crafted from welded vehicle armor, truck tires, and coiled razor wire.
* **Surveillance Camera Tripod / Sensor Post (48x96 px):**
  * Day: [prop_surveillance_day.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/dystopian/prop_surveillance_day.png)
  * Night: [prop_surveillance_night.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/dystopian/prop_surveillance_night.png)
  * Tripod-mounted CCTV lens tracking movement (Day: matte military lens; Night: ominous ruby-red scanning laser optic).
* **E-Waste & Circuit Scrap Heap (128x68 px):**
  * Day: [prop_ewaste_day.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/dystopian/prop_ewaste_day.png)
  * Night: [prop_ewaste_night.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/dystopian/prop_ewaste_night.png)
  * Dumped cathode-ray monitors, cracked motherboard PCBs, drone frames (Night: blinking micro-LEDs & cyan circuitry).
* **Reinforced Steel Drum / Hazard Barrel (40x56 px):**
  * Day: [prop_drum_day.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/dystopian/prop_drum_day.png)
  * Night: [prop_drum_night.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/dystopian/prop_drum_night.png)
  * Industrial 55-gallon container with biohazard stenciling and heavy bullet dents.

### 4. Compact Telecommunication Antenna Tower (96x232 px, Low-Profile Base)
* **Design Philosophy:** Sized compactly to sit directly over the central socket collar while leaving massive open space across the 10x10 tile platform (320x320 px) for player structures, turrets, defense drones, and generators.
* **Base:** Short, low-profile octagonal armored steel pedestal with yellow/black hazard trim (~35 px tall in-game), leaving >110 px of clear platform floor on all 4 sides.
* **Mast:** Slender military lattice transmission mast with microwave transceiver dishes and red beacon at summit.
* **Day Asset:** [telecom_tower_day.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/telecom_tower_day.png)
  * Weathered olive-drab steel, hazard caution rim, dish antennas, ladder rungs.
* **Night Asset:** [telecom_tower_night.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/telecom_tower_night.png)
  * Nocturnal dark slate steel, pulsing ruby-red warning beacon with glowing halo, electric cyan (`#00f0ff`) central power conduits, and amber hazard LED nodes.
* **Previews on 10x10 Platform:**
  * Day: [metalslug_arena_with_tower_day.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/metalslug_arena_with_tower_day.png)
  * Night: [metalslug_arena_with_tower_night.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/metalslug_arena_with_tower_night.png)
  * Day: [prop_surveillance_day.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/dystopian/prop_surveillance_day.png)
  * Night: [prop_surveillance_night.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/dystopian/prop_surveillance_night.png)
  * Tripod-mounted CCTV lens tracking movement (Day: matte military lens; Night: ominous ruby-red scanning laser optic).
* **E-Waste & Circuit Scrap Heap (128x68 px):**
  * Day: [prop_ewaste_day.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/dystopian/prop_ewaste_day.png)
  * Night: [prop_ewaste_night.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/dystopian/prop_ewaste_night.png)
  * Dumped cathode-ray monitors, cracked motherboard PCBs, drone frames (Night: blinking micro-LEDs & cyan circuitry).
* **Reinforced Steel Drum / Hazard Barrel (40x56 px):**
  * Day: [prop_drum_day.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/dystopian/prop_drum_day.png)
  * Night: [prop_drum_night.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/dystopian/prop_drum_night.png)
  * Industrial 55-gallon container with biohazard stenciling and heavy bullet dents.

### 4. Telecommunication Tower Bunker Base (280x386 px, AI-Generated Metal Slug Art)
* **Day Asset:** [telecom_tower_day.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/telecom_tower_day.png)
  * Armored octagonal bunker base in olive-drab steel with heavy rivets, rust streaks, ladder, dishes, transmission mast, and top red beacon.
* **Night Asset:** [telecom_tower_night.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/telecom_tower_night.png)
  * Nocturnal cold slate armor with a pulsing glowing ruby-red beacon at the summit, electric cyan (`#00f0ff`) status conduits, and amber hazard LEDs.
* **Preview with Tower:**
  * Day: [metalslug_arena_with_tower_day.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/metalslug_arena_with_tower_day.png)
  * Night: [metalslug_arena_with_tower_night.png](file:///home/askri/Projects/FACTORY_RESET/assets/sprites/environment/metalslug_arena_with_tower_night.png)

---

## 🗺️ Map Architecture (64 × 48 Tiles = 2048 × 1536 px)

```
0                              32 (Center: 1024)                              63
0  ┌─────────────────────────[ Perimeter Trees & Forest ]────────────────────────┐
   │ 🌲       🌲              🌲                🌲              🌲        🌲     │
   │                                                                            │
   │                                                                            │
   │                      [ Vast Open Wasteland Battlefield ]                   │
   │                                                                            │
19 │                      ┌───────────────────────────────┐                     │
   │                      │  Central Tower Foundation     │                     │
   │                      │       (10x10 Platform)        │                     │
   │ 🌲                   │   Empty Center Socket Waiting │                  🌲 │
   │                      │        for Telecom Tower      │                     │
28 │                      └───────────────────────────────┘                     │
   │                                                                            │
   │                                                                            │
   │                      [ Vast Open Wasteland Battlefield ]                   │
   │                                                                            │
   │ 🌲       🌲              🌲                🌲              🌲        🌲     │
47 └─────────────────────────[ Perimeter Trees & Forest ]────────────────────────┘
```

---

## 🕹️ Live Testing & Controls
* **Movement:** `WASD` / Arrow keys to move Sami across the 2048x1536 map.
* **Day/Night Toggle:** Press `[N]` or `[TAB]` to instantly swap all tiles and tree assets between Day and Night.
* **Launch:** `DISPLAY=:1 godot` (or via Antigravity MCP runner).
