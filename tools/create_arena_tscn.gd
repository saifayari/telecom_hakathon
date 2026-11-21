@tool
extends SceneTree

func _init():
    print("Generating res://scenes/environment/Arena.tscn...")
    
    var root = Node2D.new()
    root.name = "Arena"
    root.set_script(load("res://scripts/environment/Arena.gd"))
    
    # 1. Background layer
    var bg = CanvasLayer.new()
    bg.name = "Background"
    bg.layer = -10
    root.add_child(bg)
    bg.owner = root
    
    var sky = Sprite2D.new()
    sky.name = "SkySprite"
    sky.texture = load("res://assets/sprites/environment/bg_day_sky.png")
    sky.position = Vector2(448, 320)
    # Scale to cover arena (896x640)
    sky.scale = Vector2(1.5, 1.8)
    bg.add_child(sky)
    sky.owner = root
    
    # 2. TileMapLayer
    var tilemap = TileMapLayer.new()
    tilemap.name = "TileMapLayer"
    var tileset = load("res://scenes/environment/arena_tileset.tres")
    tilemap.tile_set = tileset
    root.add_child(tilemap)
    tilemap.owner = root
    
    var COLS = 28
    var ROWS = 20
    
    # Helper to set cell
    # source_id = 0, coords = Vector2i(col, row)
    for y in range(ROWS):
        for x in range(COLS):
            var cell = Vector2i(x, y)
            
            # --- Perimeters (Row 3 in tileset) ---
            # Corners
            if x == 0 and y == 0:
                tilemap.set_cell(cell, 0, Vector2i(4, 3)) # Beacon TL
            elif x == COLS - 1 and y == 0:
                tilemap.set_cell(cell, 0, Vector2i(5, 3)) # Beacon TR
            elif x == 0 and y == ROWS - 1:
                tilemap.set_cell(cell, 0, Vector2i(6, 3)) # Beacon BL
            elif x == COLS - 1 and y == ROWS - 1:
                tilemap.set_cell(cell, 0, Vector2i(7, 3)) # Beacon BR
            # Top railing & breach
            elif y == 0:
                if x == 12:
                    tilemap.set_cell(cell, 0, Vector2i(0, 4)) # Breach left
                elif x == 13 or x == 14:
                    tilemap.set_cell(cell, 0, Vector2i(1, 4)) # Breach center
                elif x == 15:
                    tilemap.set_cell(cell, 0, Vector2i(2, 4)) # Breach right
                else:
                    tilemap.set_cell(cell, 0, Vector2i(0, 3)) # Railing top
            # Bottom lip & cable breach
            elif y == ROWS - 1:
                if x == 13:
                    tilemap.set_cell(cell, 0, Vector2i(3, 4)) # Lift left
                elif x == 14:
                    tilemap.set_cell(cell, 0, Vector2i(4, 4)) # Lift right
                else:
                    tilemap.set_cell(cell, 0, Vector2i(1, 3)) # Railing bottom
            # Left & Right railings
            elif x == 0:
                tilemap.set_cell(cell, 0, Vector2i(2, 3)) # Railing left
            elif x == COLS - 1:
                tilemap.set_cell(cell, 0, Vector2i(3, 3)) # Railing right
                
            # --- Hazard Caution Borders (Row 2 in tileset) ---
            elif x == 1 and y == 1:
                tilemap.set_cell(cell, 0, Vector2i(4, 2)) # Corner TL
            elif x == COLS - 2 and y == 1:
                tilemap.set_cell(cell, 0, Vector2i(5, 2)) # Corner TR
            elif x == 1 and y == ROWS - 2:
                tilemap.set_cell(cell, 0, Vector2i(6, 2)) # Corner BL
            elif x == COLS - 2 and y == ROWS - 2:
                tilemap.set_cell(cell, 0, Vector2i(7, 2)) # Corner BR
            elif y == 1:
                if 12 <= x and x <= 15:
                    tilemap.set_cell(cell, 0, Vector2i(0, 0)) # Open at breach
                else:
                    tilemap.set_cell(cell, 0, Vector2i(0, 2)) # Hazard top
            elif y == ROWS - 2:
                tilemap.set_cell(cell, 0, Vector2i(1, 2)) # Hazard bottom
            elif x == 1:
                tilemap.set_cell(cell, 0, Vector2i(2, 2)) # Hazard left
            elif x == COLS - 2:
                tilemap.set_cell(cell, 0, Vector2i(3, 2)) # Hazard right
                
            # --- Conduits (Row 1 in tileset) ---
            # Horizontal conduits on y = 10
            elif y == 10 and ((5 <= x and x <= 11) or (16 <= x and x <= 22)):
                tilemap.set_cell(cell, 0, Vector2i(0, 1)) # Conduit H
            # Vertical conduits on x = 13 (breach to center, and center to bottom)
            elif (x == 13 or x == 14) and (y <= 7 or y >= 12):
                tilemap.set_cell(cell, 0, Vector2i(1, 1)) # Conduit V
                
            # --- Center Tower Footprint (4x4 tiles: cols 12..15, rows 8..11) ---
            elif (12 <= x and x <= 15) and (8 <= y and y <= 11):
                # Recessed foundation empty bay
                tilemap.set_cell(cell, 0, Vector2i(4, 5)) # tower_base_empty_pit
                
            # --- Interior floor tiles with rich variety ---
            else:
                var pattern = (x * 7 + y * 13) % 29
                if pattern in [0, 1, 2]:
                    tilemap.set_cell(cell, 0, Vector2i(1, 0)) # Quad plates
                elif pattern in [3, 4]:
                    tilemap.set_cell(cell, 0, Vector2i(3, 0)) # Diamond tread
                elif pattern in [5, 6]:
                    tilemap.set_cell(cell, 0, Vector2i(2, 0)) # Vent grate
                elif pattern == 7:
                    tilemap.set_cell(cell, 0, Vector2i(6, 0)) # Rust
                elif pattern == 8:
                    tilemap.set_cell(cell, 0, Vector2i(7, 0)) # Battle scratch
                elif pattern == 9:
                    tilemap.set_cell(cell, 0, Vector2i(4, 0)) # Hex plate
                elif pattern == 10:
                    tilemap.set_cell(cell, 0, Vector2i(5, 0)) # Corrugated
                elif pattern == 11:
                    tilemap.set_cell(cell, 0, Vector2i(3, 6)) # Floor floodlight
                else:
                    tilemap.set_cell(cell, 0, Vector2i(0, 0)) # Base steel plate

    # 3. Landmark Props
    # Empty Central Tower Bay (128x128, centered at (448, 320))
    var tower = Sprite2D.new()
    tower.name = "CentralTowerBay"
    tower.texture = load("res://assets/sprites/environment/central_tower_bay_day.png")
    tower.position = Vector2(448, 320)
    root.add_child(tower)
    tower.owner = root
    
    # Scrap Depot (64x64, West at (128, 320))
    var scrap = Sprite2D.new()
    scrap.name = "ScrapDepot"
    scrap.texture = load("res://assets/sprites/environment/scrap_depot_zone_day.png")
    scrap.position = Vector2(128, 320)
    root.add_child(scrap)
    scrap.owner = root
    
    # AEGIS Landing Pad (64x64, East at (768, 320))
    var aegis = Sprite2D.new()
    aegis.name = "AegisPad"
    aegis.texture = load("res://assets/sprites/environment/aegis_landing_pad_day.png")
    aegis.position = Vector2(736, 320)
    root.add_child(aegis)
    aegis.owner = root
    
    # 4 Turret Mounting Pads (64x64 each)
    var turret_positions = {
        "TurretPadNW": Vector2(160, 128),
        "TurretPadNE": Vector2(704, 128),
        "TurretPadSW": Vector2(160, 480),
        "TurretPadSE": Vector2(704, 480),
    }
    for pad_name in turret_positions:
        var pad = Sprite2D.new()
        pad.name = pad_name
        pad.texture = load("res://assets/sprites/environment/turret_mount_pad_day.png")
        pad.position = turret_positions[pad_name]
        root.add_child(pad)
        pad.owner = root
        
    var scene = PackedScene.new()
    scene.pack(root)
    var err = ResourceSaver.save(scene, "res://scenes/environment/Arena.tscn")
    if err == OK:
        print("Successfully generated res://scenes/environment/Arena.tscn!")
    else:
        printerr("Failed to save Arena.tscn: ", err)
    quit()
