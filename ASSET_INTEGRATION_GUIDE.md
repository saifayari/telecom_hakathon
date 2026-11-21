# 🎮 FACTORY RESET — Asset Integration & Lore Gameplay Guide

## 📖 Overview & Narrative Alignment
All assets from the `art (2)\art` asset collection have been extracted, processed into transparent PNG sprites and animations, and integrated into **FACTORY RESET** according to the official lore documents (`01_ORIGINS_THE_MUTATION.md`, `02_TELECOM_TOWERS_AND_TECHNICIANS.md`, `03_AEGIS_THE_LAST_RESORT.md`, `GDD_FACTORY_RESET.md`):

---

## 📦 Integrated Asset Breakdown

### 1. Sami (The Grid Technician)
* **Location:** `res://assets/sprites/characters/sami/`
* **Source:** `art (2)/art/agent_new/`
* **Animations (`AnimatedSprite2D`):**
  * `idle`: Sami standing vigilant in Faraday hazmat suit & yellow helmet (`sami_idle.png`).
  * `walk`: 4-frame directional sprint cycle (`sami_walk_0.png` to `sami_walk_3.png`).
  * `shoot`: Aiming and firing stance with recoil (`sami_shoot.png`).
  * `weld`: Crouched electrical technician testing/soldering pose (`sami_weld.png`).
* **Weapons & Tools (`res://assets/sprites/weapons/`):**
  * `gun_rifle.png`: Scrap rifle equipped to weapon pivot, aims towards mouse.
  * `muzzle_flash.png`: Firing flash upon shooting.
  * `gun_welder.png`: Signal frequency resonator & plasma welder.

### 2. Unit-R17 Scrap Amalgam (Nano-Scrap Mutant Golem)
* **Location:** `res://assets/sprites/monsters/amalgam/`
* **Source:** `art (2)/art/monsters/`
* **Animations:**
  * `walk`: 6-frame heavy walk cycle (`amalgam_walk_0.png` to `amalgam_walk_5.png`).
  * `idle`: Front-facing imposing posture (`amalgam_idle.png`).
  * `attack`: 4-frame crushing smash sequence (`amalgam_attack_0.png` to `amalgam_attack_3.png`).
  * `hit`: Shock/stun frame (`amalgam_hit.png`).
* **Lore Mechanics:**
  * High health (350 HP), attacks the core tower and Sami.
  * **Devour Mutation:** At night, if unpurified scrap piles exist, it moves to devour them, gaining +30% scale, +50% max health, and increased speed.
  * Drops an inert `ScrapPile` upon death.

### 3. Scrap Piles & Nano Awakening (Core Game Loop USP)
* **Location:** `res://assets/sprites/environment/scrap_pile/`
* **Source:** `art (2)/art/monsters/Gemini_Generated_Image_niobamniobamniob.jpg`
* **Stages:**
  1. `scrap_pile_inert.png`: Inactive scrap under the daytime jamming umbrella.
  2. `scrap_pile_glow.png`: Green spore reactivation at dusk as signal decays.
  3. `scrap_pile_spores.png`: Swarming biological-metallic mesh.
  4. `scrap_pile_erupting.png`: Violent reassembly into a monster if left unpurified.
* **Purification:** Holding `[E]` for 0.8s fires the RF welder, emitting a **150px Resonant Shockwave** (`shockwave_ring.png`, 150 AOE damage, 3s EM stun) and rewarding **Pure Alloys** and **Raw Scrap**.

### 4. Protocol AEGIS (Autonomous Ecological Intervention Drone)
* **Location:** `res://assets/sprites/characters/drone/`
* **Source:** `art (2)/art/Drone/`
* **Visuals:** Hovering idle frames (`drone_idle_0..3.png`) and scanning laser beam (`drone_scan_0..3.png`).
* **Interaction:** Pressing `[F]` opens the **AEGIS Barter Terminal** (`scenes/ui/AegisBarterModal.tscn`), trading Pure Alloys for Lithium Batteries, Sentry Kits, and Core repairs.

### 5. Telecom Tower Compound & Workshop Props
* **Location:** `res://assets/sprites/props/`
* **Source:** `Craft_new_0`, `Craft_new_1`, `day_back_0`, `night_back_0`, `day_back_1`
* **Integrated Props:**
  * `telecom_tower_day.png` & `telecom_tower_night.png`: Central transmission lattice tower.
  * `power_generator.png`: Diesel backup generator wired with high-voltage conduits.
  * `workbench_electronics.png`: Soldering/testing bench with magnifying lamp.
  * `workbench_mechanical.png`: Assembly table with calipers, gears, and vises.
  * `cable_spool.png` & `telecom_junction_box.png`: Telecom wire infrastructure.
  * `tower_terminal.png`: CRT monitoring console.
  * `barricade_spikes.png`: Defensive spiked walls.

### 6. Economy & Crafting Icons
* **Location:** `res://assets/sprites/icons/`
* **Icons:** `icon_scrap.png`, `icon_pure_alloy.png`, `icon_lithium_battery.png`, `icon_nano_core.png`, `icon_copper_coil.png`, `icon_induction_coil.png`, `icon_composite_armor.png`, `icon_emp_pulsar.png`.
* Integrated directly into HUD resource display, Crafting Menu, and AEGIS Barter Modal.

---

## 🕹️ Controls & Keybindings

| Key / Action | Function |
| :--- | :--- |
| **W, A, S, D** / Arrows | Move Sami across the 2048×1536 wasteland battlefield. |
| **Mouse Cursor** | Aim weapon / RF welder in 360 degrees. |
| **Left Click / Space** | Shoot Scrap Rifle (fires bullet projectiles with muzzle flash). |
| **Hold [E]** | Purify adjacent Scrap Pile with RF Welder (triggers shockwave & pure alloys). |
| **[F]** | Trade with Protocol AEGIS Drone (when in range) / Deploy defenses. |
| **[TAB]** | Open / Close Field Crafting Schematics Modal. |
| **[N]** | Toggle Day / Night Phase manually for testing. |

---

## 🚀 Running the Game in Godot
Run the project directly in Godot Engine:
```bash
# Using the bundled Godot engine:
& "art (2)\art\agent_new\Godot_v4.7.2-stable_win64.exe\Godot_v4.7.2-stable_win64.exe" --path "FACTORY_RESET-main"
```
Main Scene: `res://scenes/main/GameLevel.tscn`
