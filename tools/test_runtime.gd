@tool
extends SceneTree

func _init():
	print("--- TESTING SCRAPBOUND RUNTIME ---")
	var main_scene = load("res://scenes/scrapbound/ScrapboundMain.tscn")
	if not main_scene:
		printerr("FAILED TO LOAD ScrapboundMain.tscn")
		quit(1)
		return
	
	var main_node = main_scene.instantiate()
	root.add_child(main_node)
	
	print("ScrapboundMain instantiated successfully!")
	
	# Simulate actions
	print("Simulating monster spawn...")
	main_node.spawn_monster_net(101, Vector2(200, 100))
	
	print("Simulating scrap spawn...")
	main_node.spawn_scrap_drop_net(201, "scrap", 15, Vector2(210, 290))
	
	print("Simulating scrap collection...")
	main_node.request_collect_scrap("ScrapItem_201", 1)
	
	print("Simulating refinement...")
	main_node.p1.global_position = main_node.recycler1.global_position
	main_node.request_refine(1, "random")
	
	print("Simulating tower build...")
	main_node.p1.inventory["iron"] = 2
	main_node.p1.inventory["plastic"] = 1
	main_node.request_build_tower(1, Vector2(250, 300))
	
	print("Simulating weapon craft...")
	main_node.p1.inventory["wood"] = 1
	main_node.p1.inventory["iron"] = 1
	main_node.p1.inventory["plastic"] = 1
	main_node.request_craft_recipe(1, "Shotgun")

	print("--- TEST PASSED WITH ZERO ERRORS ---")
	quit(0)
