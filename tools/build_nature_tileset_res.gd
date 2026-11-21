@tool
extends SceneTree

func _init():
    print("Building nature_tileset.tres...")
    var tileset = TileSet.new()
    tileset.tile_size = Vector2i(32, 32)
    
    var day_tex = load("res://assets/sprites/environment/nature_tileset_day.png")
    var night_tex = load("res://assets/sprites/environment/nature_tileset_night.png")
    
    # Source 0: Day Atlas
    var src_day = TileSetAtlasSource.new()
    src_day.texture = day_tex
    src_day.texture_region_size = Vector2i(32, 32)
    
    # Source 1: Night Atlas
    var src_night = TileSetAtlasSource.new()
    src_night.texture = night_tex
    src_night.texture_region_size = Vector2i(32, 32)
    
    for row in range(8):
        for col in range(8):
            var coords = Vector2i(col, row)
            src_day.create_tile(coords)
            src_night.create_tile(coords)
            
    tileset.add_source(src_day, 0)
    tileset.add_source(src_night, 1)
    
    # Physics layer for rocks / props (Layer 1: World)
    tileset.add_physics_layer()
    tileset.set_physics_layer_collision_layer(0, 1)
    tileset.set_physics_layer_collision_mask(0, 2 | 4)
    
    # Add collision to rocks on row 3 (col 0: small rock, col 1: boulder)
    for col in [0, 1]:
        for src in [src_day, src_night]:
            var tile_data = src.get_tile_data(Vector2i(col, 3), 0)
            if tile_data:
                tile_data.add_collision_polygon(0)
                var poly = PackedVector2Array([
                    Vector2(-12, -4), Vector2(12, -4),
                    Vector2(12, 12), Vector2(-12, 12)
                ])
                tile_data.set_collision_polygon_points(0, 0, poly)
                
    var err = ResourceSaver.save(tileset, "res://scenes/environment/nature_tileset.tres")
    if err == OK:
        print("Successfully saved res://scenes/environment/nature_tileset.tres!")
    else:
        printerr("Failed to save nature_tileset.tres: ", err)
    quit()
