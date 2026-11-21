@tool
extends SceneTree

func _init() -> void:
	print("Building NatureArena.tscn with sparse dystopian tree framing...")
	
	# 1. Load tileset textures
	var tex_day = load("res://assets/sprites/environment/metalslug_tileset_day.png")
	var tex_night = load("res://assets/sprites/environment/metalslug_tileset_night.png")
	
	# 2. Build TileSet resource
	var tileset = TileSet.new()
	tileset.tile_size = Vector2i(32, 32)
	
	var source_day = TileSetAtlasSource.new()
	source_day.texture = tex_day
	source_day.texture_region_size = Vector2i(32, 32)
	for r in range(4):
		for c in range(8):
			source_day.create_tile(Vector2i(c, r))
			
	var source_night = TileSetAtlasSource.new()
	source_night.texture = tex_night
	source_night.texture_region_size = Vector2i(32, 32)
	for r in range(4):
		for c in range(8):
			source_night.create_tile(Vector2i(c, r))
			
	tileset.add_source(source_day, 0)
	tileset.add_source(source_night, 1)
	
	var err = ResourceSaver.save(tileset, "res://scenes/environment/nature_tileset.tres")
	if err != OK:
		printerr("Failed to save nature_tileset.tres: ", err)
		quit(1)
		return
	print("Saved nature_tileset.tres.")
	
	# 3. Build NatureArena scene
	var root = Node2D.new()
	root.name = "NatureArena"
	root.y_sort_enabled = true
	var script = load("res://scripts/environment/NatureArena.gd")
	root.set_script(script)
	
	# TileMapLayer (64 x 48 tiles)
	var tm_layer = TileMapLayer.new()
	tm_layer.name = "TileMapLayer"
	tm_layer.tile_set = tileset
	root.add_child(tm_layer)
	tm_layer.owner = root
	
	var cols = 64
	var rows = 48
	var c_start = 27
	var c_end = 36
	var r_start = 19
	var r_end = 28
	
	# Seeded random for reproducible natural ground variation
	seed(1337)
	
	for r in range(rows):
		for c in range(cols):
			var tc = 0
			var tr = 0
			var rand_v = randf()
			if rand_v < 0.12:
				tc = 1; tr = 0 # fissure
			elif rand_v < 0.22:
				tc = 2; tr = 0 # gravel
			elif rand_v < 0.30:
				tc = 3; tr = 0 # weed
			elif rand_v < 0.35:
				tc = 4; tr = 0 # metal plate
			elif rand_v < 0.40:
				tc = 5; tr = 0 # tread
			elif rand_v < 0.45:
				tc = 6; tr = 0 # scrap shard
			elif rand_v < 0.50:
				tc = 4; tr = 3 # earth var 2
			elif rand_v < 0.55:
				tc = 5; tr = 3 # earth var 3
			elif rand_v < 0.60:
				tc = 6; tr = 3 # earth var 4
			else:
				tc = 0; tr = 0 # base dirt
				
			# Check central platform
			if r >= r_start and r <= r_end and c >= c_start and c <= c_end:
				if r == r_start and c == c_start:
					tc = 0; tr = 1 # TL
				elif r == r_start and c == c_end:
					tc = 2; tr = 1 # TR
				elif r == r_end and c == c_start:
					tc = 6; tr = 1 # BL
				elif r == r_end and c == c_end:
					tc = 0; tr = 2 # BR
				elif r == r_start:
					tc = 1; tr = 1 # Top
				elif r == r_end:
					tc = 7; tr = 1 # Bottom
				elif c == c_start:
					tc = 3; tr = 1 # Left
				elif c == c_end:
					tc = 5; tr = 1 # Right
				else:
					tc = 4; tr = 1 # Inner floor
					
				# Center socket and conduits
				if (r == 23 or r == 24) and (c == 31 or c == 32):
					tc = 4; tr = 2 # Socket
				elif (r == 23 or r == 24) and ((c > c_start and c < 31) or (c > 32 and c < c_end)):
					tc = 1; tr = 2 # Horizontal conduit
				elif (c == 31 or c == 32) and ((r > r_start and r < 23) or (r > 24 and r < r_end)):
					tc = 2; tr = 2 # Vertical conduit
				elif (r == r_start + 2 or r == r_end - 2) and (c == c_start + 2 or c == c_end - 2):
					tc = 5; tr = 2 # Vent grate
				elif (r == r_start + 1 or r == r_end - 1) and (c == c_start + 1 or c == c_end - 1):
					tc = 7; tr = 2 # Beacon pad
					
			tm_layer.set_cell(Vector2i(c, r), 0, Vector2i(tc, tr))
			
	# Trees Container
	var trees_cont = Node2D.new()
	trees_cont.name = "TreesContainer"
	trees_cont.y_sort_enabled = true
	root.add_child(trees_cont)
	trees_cont.owner = root
	
	# Load tree textures
	var t_oak_lg_d = load("res://assets/sprites/environment/tree_oak_large_day.png")
	var t_oak_md_d = load("res://assets/sprites/environment/tree_oak_med_day.png")
	var t_pine_d = load("res://assets/sprites/environment/tree_pine_day.png")
	var t_dead_d = load("res://assets/sprites/environment/tree_dead_day.png")
	var t_stump_d = load("res://assets/sprites/environment/tree_stump_day.png")
	
	var tex_map = {
		"oak_lg": t_oak_lg_d,
		"oak_md": t_oak_md_d,
		"pine": t_pine_d,
		"dead": t_dead_d,
		"stump": t_stump_d
	}
	
	# Reduced sparse tree placements (14 trees instead of 70)
	var tree_positions: Array = [
		# North perimeter (spaced widely across 2048 px)
		{"type": "oak_lg", "pos": Vector2(180, 50)},
		{"type": "pine", "pos": Vector2(650, 45)},
		{"type": "oak_md", "pos": Vector2(1380, 50)},
		{"type": "dead", "pos": Vector2(1860, 45)},
		
		# South perimeter (spaced widely across 2048 px)
		{"type": "dead", "pos": Vector2(200, 1470)},
		{"type": "oak_md", "pos": Vector2(720, 1480)},
		{"type": "pine", "pos": Vector2(1320, 1475)},
		{"type": "oak_lg", "pos": Vector2(1840, 1470)},
		
		# West perimeter (vertical edge)
		{"type": "dead", "pos": Vector2(50, 480)},
		{"type": "stump", "pos": Vector2(60, 760)},
		{"type": "oak_md", "pos": Vector2(55, 1040)},
		
		# East perimeter (vertical edge)
		{"type": "pine", "pos": Vector2(1990, 480)},
		{"type": "stump", "pos": Vector2(1980, 760)},
		{"type": "dead", "pos": Vector2(1995, 1040)}
	]
	
	for i in range(tree_positions.size()):
		var t_info = tree_positions[i]
		var tree_body = StaticBody2D.new()
		tree_body.name = "Tree_" + str(i)
		tree_body.position = t_info["pos"]
		tree_body.set_meta("tree_type", t_info["type"])
		
		trees_cont.add_child(tree_body)
		tree_body.owner = root
		
		var spr = Sprite2D.new()
		spr.name = "Sprite2D"
		spr.texture = tex_map[t_info["type"]]
		spr.offset = Vector2(0, -spr.texture.get_height() / 2.0 + 16)
		tree_body.add_child(spr)
		spr.owner = root
		
		var col = CollisionShape2D.new()
		col.name = "CollisionShape2D"
		var circle = CircleShape2D.new()
		circle.radius = 12.0
		col.shape = circle
		col.position = Vector2(0, 4)
		tree_body.add_child(col)
		col.owner = root
		
	# Save packed scene
	var packed = PackedScene.new()
	var pack_err = packed.pack(root)
	if pack_err != OK:
		printerr("Failed to pack NatureArena: ", pack_err)
		quit(1)
		return
		
	var save_err = ResourceSaver.save(packed, "res://scenes/environment/NatureArena.tscn")
	if save_err != OK:
		printerr("Failed to save NatureArena.tscn: ", save_err)
		quit(1)
		return
		
	print("NatureArena.tscn saved with 14 sparse trees!")
	quit(0)
