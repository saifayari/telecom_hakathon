@tool
extends SceneTree

func _init():
    print("Building arena_tileset.tres...")
    var tileset = TileSet.new()
    tileset.tile_size = Vector2i(32, 32)
    
    var day_tex = load("res://assets/sprites/environment/arena_tileset_day.png")
    var night_tex = load("res://assets/sprites/environment/arena_tileset_night.png")
    
    # Source 0: Day Atlas
    var source_day = TileSetAtlasSource.new()
    source_day.texture = day_tex
    source_day.texture_region_size = Vector2i(32, 32)
    
    # Source 1: Night Atlas
    var source_night = TileSetAtlasSource.new()
    source_night.texture = night_tex
    source_night.texture_region_size = Vector2i(32, 32)
    
    for row in range(8):
        for col in range(8):
            var coords = Vector2i(col, row)
            source_day.create_tile(coords)
            source_night.create_tile(coords)
                    
    tileset.add_source(source_day, 0)
    tileset.add_source(source_night, 1)
    
    # Add physics layer after sources exist
    tileset.add_physics_layer()
    tileset.set_physics_layer_collision_layer(0, 1) # Layer 1: World
    tileset.set_physics_layer_collision_mask(0, 2 | 4) # Player and Enemies
    
    for row in range(8):
        for col in range(8):
            var coords = Vector2i(col, row)
            if row == 3: # Railing row
                for src in [source_day, source_night]:
                    var tile_data = src.get_tile_data(coords, 0)
                    var poly = PackedVector2Array([
                        Vector2(-16, -16), Vector2(16, -16),
                        Vector2(16, 16), Vector2(-16, 16)
                    ])
                    if col == 0: # Top rail
                        poly = PackedVector2Array([Vector2(-16, -16), Vector2(16, -16), Vector2(16, -4), Vector2(-16, -4)])
                    elif col == 1: # Bottom edge
                        poly = PackedVector2Array([Vector2(-16, 4), Vector2(16, 4), Vector2(16, 16), Vector2(-16, 16)])
                    elif col == 2: # Left rail
                        poly = PackedVector2Array([Vector2(-16, -16), Vector2(-4, -16), Vector2(-4, 16), Vector2(-16, 16)])
                    elif col == 3: # Right rail
                        poly = PackedVector2Array([Vector2(4, -16), Vector2(16, -16), Vector2(16, 16), Vector2(4, 16)])
                    
                    tile_data.add_collision_polygon(0)
                    tile_data.set_collision_polygon_points(0, 0, poly)

    var err = ResourceSaver.save(tileset, "res://scenes/environment/arena_tileset.tres")
    if err == OK:
        print("Successfully saved res://scenes/environment/arena_tileset.tres with 0 errors!")
    else:
        printerr("Failed to save tileset: ", err)
    quit()
