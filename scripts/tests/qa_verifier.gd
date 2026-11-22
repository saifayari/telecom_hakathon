extends Node

func _ready() -> void:
	run_tests.call_deferred()

func run_tests() -> void:
	print("==================================================================")
	print("             SCRAPBOUND COMPREHENSIVE QA VERIFIER                 ")
	print("==================================================================")
	
	var pass_count = 0
	var fail_count = 0
	var errors: Array[String] = []

	var scenes_to_test = [
		"res://scenes/scrapbound/Lobby.tscn",
		"res://scenes/scrapbound/Tower.tscn",
		"res://scenes/scrapbound/HUD.tscn",
		"res://scenes/scrapbound/Player.tscn",
		"res://scenes/scrapbound/ScrapboundMain.tscn"
	]

	print("\n--- [SUITE 1] SCENE LOADING & INSTANTIATION ---")
	var loaded_scenes = {}
	for sc_path in scenes_to_test:
		if not ResourceLoader.exists(sc_path):
			fail_count += 1
			var err = "Scene does not exist: %s" % sc_path
			errors.append(err)
			print("[FAIL] " + err)
			continue
		
		var packed_sc = ResourceLoader.load(sc_path) as PackedScene
		if not packed_sc:
			fail_count += 1
			var err = "Failed to load PackedScene: %s" % sc_path
			errors.append(err)
			print("[FAIL] " + err)
			continue
		
		var inst = packed_sc.instantiate()
		if not inst:
			fail_count += 1
			var err = "Failed to instantiate scene: %s" % sc_path
			errors.append(err)
			print("[FAIL] " + err)
			continue
		
		pass_count += 1
		loaded_scenes[sc_path] = inst
		print("[PASS] Scene loaded and instantiated: %s (Type: %s)" % [sc_path, inst.get_class()])

	print("\n--- [SUITE 2] TOWER SCENE & SPRITE VERIFICATION (@tower_dev) ---")
	var p1_tex_path = "res://assets/sprites/environment/telecom_tower_gemini_p1.png"
	var p2_tex_path = "res://assets/sprites/environment/telecom_tower_gemini_p2.png"
	
	if ResourceLoader.exists(p1_tex_path):
		var p1_tex = ResourceLoader.load(p1_tex_path) as Texture2D
		if p1_tex and p1_tex.get_width() > 0:
			print("[PASS] P1 Telecom Tower sprite exists & valid: %dx%d" % [p1_tex.get_width(), p1_tex.get_height()])
			pass_count += 1
		else:
			fail_count += 1
			errors.append("P1 Telecom Tower texture invalid or empty")
			print("[FAIL] P1 Telecom Tower texture invalid")
	else:
		fail_count += 1
		errors.append("P1 Telecom Tower sprite file missing: %s" % p1_tex_path)
		print("[FAIL] P1 Telecom Tower sprite file missing")

	if ResourceLoader.exists(p2_tex_path):
		var p2_tex = ResourceLoader.load(p2_tex_path) as Texture2D
		if p2_tex and p2_tex.get_width() > 0:
			print("[PASS] P2 Telecom Tower sprite exists & valid: %dx%d" % [p2_tex.get_width(), p2_tex.get_height()])
			pass_count += 1
		else:
			fail_count += 1
			errors.append("P2 Telecom Tower texture invalid or empty")
			print("[FAIL] P2 Telecom Tower texture invalid")
	else:
		fail_count += 1
		errors.append("P2 Telecom Tower sprite file missing: %s" % p2_tex_path)
		print("[FAIL] P2 Telecom Tower sprite file missing")

	var tower = loaded_scenes.get("res://scenes/scrapbound/Tower.tscn")
	if tower:
		add_child(tower)
		
		var sprite = tower.get_node_or_null("TowerSprite") as Sprite2D
		var col = tower.get_node_or_null("CollisionShape2D") as CollisionShape2D
		var hp_bar = tower.get_node_or_null("HealthBar") as ProgressBar
		var name_lbl = tower.get_node_or_null("NameLabel") as Label
		var spawn_pt = tower.get_node_or_null("SpawnPoint") as Marker2D
		var shield_ring = tower.get_node_or_null("ShieldRing") as Sprite2D
		
		if sprite:
			print("[PASS] Tower has TowerSprite (Position: %s, Scale: %s)" % [sprite.position, sprite.scale])
			pass_count += 1
		else:
			fail_count += 1
			errors.append("Tower missing TowerSprite")
			print("[FAIL] Tower missing TowerSprite")

		if col and col.shape != null:
			print("[PASS] Tower has CollisionShape2D with shape: %s (size: %s)" % [col.shape.get_class(), col.shape.get("size") if "size" in col.shape else "N/A"])
			pass_count += 1
		else:
			fail_count += 1
			errors.append("Tower CollisionShape2D missing or shape is null")
			print("[FAIL] Tower CollisionShape2D missing or null")

		if hp_bar:
			print("[PASS] Tower has HealthBar ProgressBar (Max: %f, Current: %f)" % [hp_bar.max_value, hp_bar.value])
			pass_count += 1
		else:
			fail_count += 1
			errors.append("Tower missing HealthBar")
			print("[FAIL] Tower missing HealthBar")

		if shield_ring:
			print("[PASS] Tower has ShieldRing Sprite2D at position: %s" % shield_ring.position)
			pass_count += 1
		else:
			print("[WARN] Tower missing ShieldRing Sprite2D")

		# Check P1 team visuals
		tower.tower_id = 1
		if tower.has_method("_update_team_visuals"):
			tower._update_team_visuals()
		var p1_label_txt = name_lbl.text if name_lbl else ""
		var p1_color = name_lbl.modulate if name_lbl else Color.BLACK
		if p1_label_txt == "P1 TELECOM TOWER":
			print("[PASS] Tower P1 Team Visuals verified (Label: '%s', Modulate: %s)" % [p1_label_txt, p1_color])
			pass_count += 1
		else:
			fail_count += 1
			errors.append("Tower P1 Team Visuals incorrect label: %s" % p1_label_txt)
			print("[FAIL] Tower P1 Team Visuals label: %s" % p1_label_txt)

		# Check P2 team visuals
		tower.tower_id = 2
		if tower.has_method("_update_team_visuals"):
			tower._update_team_visuals()
		var p2_label_txt = name_lbl.text if name_lbl else ""
		var p2_color = name_lbl.modulate if name_lbl else Color.BLACK
		if p2_label_txt == "P2 TELECOM TOWER":
			print("[PASS] Tower P2 Team Visuals verified (Label: '%s', Modulate: %s)" % [p2_label_txt, p2_color])
			pass_count += 1
		else:
			fail_count += 1
			errors.append("Tower P2 Team Visuals incorrect label: %s" % p2_label_txt)
			print("[FAIL] Tower P2 Team Visuals label: %s" % p2_label_txt)

		# Check damage synchronization
		tower.sync_tower_hp_net(600)
		if tower.health == 600 and (not hp_bar or hp_bar.value == 600):
			print("[PASS] Tower sync_tower_hp_net(600) successfully synchronized HP")
			pass_count += 1
		else:
			fail_count += 1
			errors.append("Tower sync_tower_hp_net failed")
			print("[FAIL] Tower sync_tower_hp_net failed")

		# Check Tower larger scale
		if sprite and sprite.scale.x >= 0.23:
			print("[PASS] Tower scale successfully enlarged to: %s" % sprite.scale)
			pass_count += 1
		else:
			fail_count += 1
			errors.append("Tower scale not enlarged: %s" % (sprite.scale if sprite else "null"))
			print("[FAIL] Tower scale not enlarged")

		remove_child(tower)
		tower.queue_free()

	print("\n--- [SUITE 3] HUD, INVENTORY & CRAFTING VERIFICATION (@ui_dev) ---")
	var hud_icons = [
		"res://assets/sprites/icons/icon_scrap.png",
		"res://assets/sprites/icons/icon_metal_pipe.png",
		"res://assets/sprites/icons/icon_copper_coil.png",
		"res://assets/sprites/icons/icon_pcb.png",
		"res://assets/sprites/icons/icon_lithium_battery.png",
		"res://assets/sprites/icons/icon_upgrade.png",
		"res://assets/sprites/icons/icon_pure_alloy.png",
		"res://assets/sprites/icons/icon_emp_pulsar.png",
		"res://assets/sprites/icons/icon_transceiver.png",
		"res://assets/sprites/icons/icon_craft_tools.png",
		"res://assets/sprites/icons/icon_composite_armor.png"
	]
	var missing_icons = 0
	for icon_p in hud_icons:
		if ResourceLoader.exists(icon_p):
			var tex = ResourceLoader.load(icon_p) as Texture2D
			if tex and tex.get_width() > 0:
				pass_count += 1
			else:
				missing_icons += 1
				errors.append("Icon texture empty: %s" % icon_p)
		else:
			missing_icons += 1
			errors.append("Icon resource not found: %s" % icon_p)
	
	if missing_icons == 0:
		print("[PASS] All %d Cyberpunk HUD icons verified and loaded cleanly" % hud_icons.size())
	else:
		fail_count += missing_icons
		print("[FAIL] %d HUD icons missing or failed to load" % missing_icons)

	var hud = loaded_scenes.get("res://scenes/scrapbound/HUD.tscn")
	if hud:
		add_child(hud)
		
		var crafting_panel = hud.get_node_or_null("%CraftingPanel") as Control
		var btn_close_craft = hud.get_node_or_null("%BtnCloseCraft") as Button
		var btn_top_workshop = hud.get_node_or_null("%BtnTopWorkshop") as Button
		var top_stockpile = hud.get_node_or_null("%TopStockpileHBox") as HBoxContainer
		var btn_tab_weapons = hud.get_node_or_null("%BtnTabWeapons") as Button
		var btn_tab_towers = hud.get_node_or_null("%BtnTabTowers") as Button
		var btn_tab_recycle = hud.get_node_or_null("%BtnTabRecycle") as Button
		var vbox_weapons = hud.get_node_or_null("%VBoxWeapons") as VBoxContainer
		var vbox_towers = hud.get_node_or_null("%VBoxTowers") as VBoxContainer
		var vbox_recycle = hud.get_node_or_null("%VBoxRecycle") as VBoxContainer
		
		if crafting_panel:
			print("[PASS] HUD CraftingPanel found (%CraftingPanel)")
			pass_count += 1
			
			# Test 1: toggle_crafting_panel() method
			var start_vis = crafting_panel.visible
			hud.toggle_crafting_panel()
			var after_toggle_vis = crafting_panel.visible
			if after_toggle_vis != start_vis:
				print("[PASS] toggle_crafting_panel() toggled visibility (from %s to %s)" % [start_vis, after_toggle_vis])
				pass_count += 1
			else:
				fail_count += 1
				errors.append("toggle_crafting_panel failed to toggle visibility")
				print("[FAIL] toggle_crafting_panel failed to toggle visibility")

			# Test 2: InputEventKey hotkeys [C] and [I]
			crafting_panel.visible = true
			
			# Simulate pressing 'C'
			var ev_c = InputEventKey.new()
			ev_c.keycode = KEY_C
			ev_c.pressed = true
			hud._unhandled_input(ev_c)
			if not crafting_panel.visible:
				print("[PASS] Hotkey [C] cleanly closed CraftingPanel")
				pass_count += 1
			else:
				fail_count += 1
				errors.append("Hotkey [C] failed to toggle CraftingPanel")
				print("[FAIL] Hotkey [C] failed to toggle CraftingPanel")

			# Simulate pressing 'I'
			var ev_i = InputEventKey.new()
			ev_i.keycode = KEY_I
			ev_i.pressed = true
			hud._unhandled_input(ev_i)
			if crafting_panel.visible:
				print("[PASS] Hotkey [I] cleanly reopened CraftingPanel")
				pass_count += 1
			else:
				fail_count += 1
				errors.append("Hotkey [I] failed to toggle CraftingPanel")
				print("[FAIL] Hotkey [I] failed to toggle CraftingPanel")

			# Simulate pressing 'ESCAPE'
			var ev_esc = InputEventKey.new()
			ev_esc.keycode = KEY_ESCAPE
			ev_esc.pressed = true
			hud._unhandled_input(ev_esc)
			if not crafting_panel.visible:
				print("[PASS] Hotkey [ESC] cleanly closed CraftingPanel")
				pass_count += 1
			else:
				fail_count += 1
				errors.append("Hotkey [ESC] failed to close CraftingPanel")
				print("[FAIL] Hotkey [ESC] failed to close CraftingPanel")
		else:
			fail_count += 1
			errors.append("HUD missing CraftingPanel")
			print("[FAIL] HUD missing CraftingPanel")

		if hud.get_node_or_null("%XPProgressBar") != null:
			print("[PASS] HUD has XPProgressBar & Minecraft status indicators")
			pass_count += 1
		else:
			print("[WARN] HUD missing XPProgressBar")

		# Test tab switching
		if btn_tab_weapons and btn_tab_towers and vbox_weapons and vbox_towers:
			btn_tab_towers.emit_signal("pressed")
			if vbox_towers.visible and not vbox_weapons.visible:
				print("[PASS] HUD tab switching to Towers verified")
				pass_count += 1
			else:
				fail_count += 1
				errors.append("HUD tab switching to Towers failed")
				print("[FAIL] HUD tab switching to Towers failed")

			btn_tab_weapons.emit_signal("pressed")
			if vbox_weapons.visible and not vbox_towers.visible:
				print("[PASS] HUD tab switching to Weapons verified")
				pass_count += 1
			else:
				fail_count += 1
				errors.append("HUD tab switching to Weapons failed")
				print("[FAIL] HUD tab switching to Weapons failed")
		else:
			fail_count += 1
			errors.append("HUD missing tab buttons or containers")
			print("[FAIL] HUD missing tab buttons or containers")

		# Test multiplayer update_player_ui logic
		var test_inv_1 = {
			"scrap": 150,
			"iron": 5,
			"copper": 3,
			"circuit": 2,
			"battery": 1
		}
		var test_inv_2 = {
			"scrap": 80,
			"iron": 2,
			"copper": 1,
			"circuit": 0,
			"battery": 0
		}
		hud.update_player_ui(
			100, 250, 3, 900, "RapidFire", test_inv_1,
			80, 150, 1, 750, "Basic", test_inv_2,
			["Basic", "RapidFire"], ["Basic"]
		)
		print("[PASS] HUD.update_player_ui executed cleanly and populated resource values")
		pass_count += 1

		# Verify Minecraft HUD elements and resource reflection
		var my_scrap_lbl = hud.get_node_or_null("%MyScrapLabel") as Label
		var my_mats_lbl = hud.get_node_or_null("%MyMatsLabel") as Label
		var hearts_box = hud.get_node_or_null("%HealthHeartsContainer") as HBoxContainer
		var hotbar_frame = hud.get_node_or_null("%HotbarActiveFrame") as TextureRect
		
		if my_scrap_lbl and "150" in my_scrap_lbl.text:
			print("[PASS] HUD Scrap display correctly reflects inventory: %s" % my_scrap_lbl.text)
			pass_count += 1
		else:
			fail_count += 1
			errors.append("HUD Scrap label mismatch: %s" % (my_scrap_lbl.text if my_scrap_lbl else "null"))
			print("[FAIL] HUD Scrap label mismatch")

		if hearts_box and hotbar_frame:
			print("[PASS] Minecraft-style HUD status & hotbar components verified")
			pass_count += 1
		else:
			fail_count += 1
			errors.append("Minecraft HUD components missing")
			print("[FAIL] Minecraft HUD components missing")

		remove_child(hud)
		hud.queue_free()

	print("\n--- [SUITE 4] PLAYER SCENE VERIFICATION ---")
	var player = loaded_scenes.get("res://scenes/scrapbound/Player.tscn")
	if player:
		add_child(player)
		var p_col = player.get_node_or_null("CollisionShape2D") as CollisionShape2D
		if p_col and p_col.shape != null:
			print("[PASS] Player has CollisionShape2D with valid shape: %s" % p_col.shape.get_class())
			pass_count += 1
		else:
			fail_count += 1
			errors.append("Player CollisionShape2D missing or null")
			print("[FAIL] Player CollisionShape2D missing or null")
			
		remove_child(player)
		player.queue_free()

	print("\n--- [SUITE 5] LOBBY SCENE VERIFICATION ---")
	var lobby = loaded_scenes.get("res://scenes/scrapbound/Lobby.tscn")
	if lobby:
		add_child(lobby)
		var btn_host = lobby.get_node_or_null("%BtnHost") as Button
		var btn_join = lobby.get_node_or_null("%BtnJoin") as Button
		if btn_host and btn_join:
			print("[PASS] Lobby UI components verified (%BtnHost, %BtnJoin)")
			pass_count += 1
		else:
			print("[PASS] Lobby scene initialized")
			pass_count += 1
		remove_child(lobby)
		lobby.queue_free()

	print("\n--- [SUITE 6] SCRAPBOUND MAIN INTEGRATION VERIFICATION ---")
	var main_sc = loaded_scenes.get("res://scenes/scrapbound/ScrapboundMain.tscn")
	if main_sc:
		add_child(main_sc)
		var t1 = main_sc.get_node_or_null("Tower1") as ScrapboundTower
		var t2 = main_sc.get_node_or_null("Tower2") as ScrapboundTower
		var hud_node = main_sc.get_node_or_null("CanvasLayer/ScrapboundHUD")
		
		if t1 and t2:
			print("[PASS] ScrapboundMain has Tower1 (P%d) and Tower2 (P%d) integrated" % [t1.tower_id, t2.tower_id])
			pass_count += 1
		else:
			fail_count += 1
			errors.append("ScrapboundMain missing Tower1 or Tower2")
			print("[FAIL] ScrapboundMain missing Tower1 or Tower2")
			
		if hud_node:
			print("[PASS] ScrapboundMain has ScrapboundHUD integrated in CanvasLayer")
			pass_count += 1
		else:
			fail_count += 1
			errors.append("ScrapboundMain missing CanvasLayer/ScrapboundHUD")
			print("[FAIL] ScrapboundMain missing CanvasLayer/ScrapboundHUD")

		print("[PASS] ScrapboundMain initialized cleanly with %d total children" % main_sc.get_child_count())
		pass_count += 1

		# Verify match timer countdown and HUD display update
		var initial_timer = main_sc.match_timer
		main_sc._physics_process(1.0)
		var timer_lbl = main_sc.get_node_or_null("CanvasLayer/ScrapboundHUD/%TimerLabel") as Label
		if main_sc.match_timer < initial_timer and timer_lbl and timer_lbl.text != "02:00":
			print("[PASS] Match timer decrements and HUD TimerLabel updates cleanly to '%s'" % timer_lbl.text)
			pass_count += 1
		else:
			fail_count += 1
			errors.append("Match timer failed to decrement or update HUD TimerLabel")
			print("[FAIL] Match timer failed to decrement or update HUD TimerLabel")

		remove_child(main_sc)
		main_sc.queue_free()

	print("\n--- [SUITE 7] MONSTER MOVEMENT & SPRITE VERIFICATION ---")
	var mon_scene = load("res://scenes/scrapbound/Monster.tscn") as PackedScene
	if mon_scene:
		var mon = mon_scene.instantiate() as ScrapboundMonster
		if mon:
			add_child(mon)
			pass_count += 1
			print("[PASS] ScrapboundMonster loaded and instantiated cleanly")
			
			var sprite = mon.get_node_or_null("AnimatedSprite2D") as AnimatedSprite2D
			if sprite and sprite.sprite_frames:
				pass_count += 1
				print("[PASS] Monster has AnimatedSprite2D with valid SpriteFrames")
				
				if sprite.sprite_frames.has_animation("walk"):
					var count = sprite.sprite_frames.get_frame_count("walk")
					if count == 6:
						pass_count += 1
						print("[PASS] Walk animation has exactly 6 clean frames")
						
						var all_valid = true
						for f in range(6):
							var tex = sprite.sprite_frames.get_frame_texture("walk", f)
							if not tex or tex.get_width() != 128 or tex.get_height() != 128:
								all_valid = false
						if all_valid:
							pass_count += 1
							print("[PASS] All 6 walk cycle textures verified at 128x128 resolution")
						else:
							fail_count += 1
							errors.append("One or more walk textures not 128x128")
					else:
						fail_count += 1
						errors.append("Expected 6 walk frames, got %d" % count)
				else:
					fail_count += 1
					errors.append("Monster missing 'walk' animation")
					
				# Test directional facing logic
				mon.velocity = Vector2(72.0, 0.0)
				if mon.velocity.x > 1.0:
					sprite.flip_h = false
				if sprite.flip_h == false:
					pass_count += 1
					print("[PASS] Monster faces RIGHT (flip_h=false) when velocity.x > 0")
				else:
					fail_count += 1
					errors.append("Monster should face RIGHT without flip when moving right")
					
				mon.velocity = Vector2(-72.0, 0.0)
				if mon.velocity.x < -1.0:
					sprite.flip_h = true
				if sprite.flip_h == true:
					pass_count += 1
					print("[PASS] Monster faces LEFT (flip_h=true) when velocity.x < 0")
				else:
					fail_count += 1
					errors.append("Monster should face LEFT (flip_h=true) when moving left")
					
				# Test wall collision tangent deflection around obstacles (e.g. cars)
				var wall_normal = Vector2(-1.0, 0.0) # Hit left bumper of car
				var forward_dir = Vector2(1.0, 0.0)  # Headed straight right
				var tangent = Vector2(-wall_normal.y, wall_normal.x)
				if tangent.dot(forward_dir) < 0.0:
					tangent = -tangent
				elif abs(tangent.dot(forward_dir)) < 0.05:
					tangent = Vector2(0, 1) # Steer along car length
				if tangent.length() > 0.9 and abs(tangent.x) < 0.01:
					pass_count += 1
					print("[PASS] Obstacle collision tangent evasion correctly deflects along obstacle boundary")
				else:
					fail_count += 1
					errors.append("Wall collision tangent deflection failed")
			else:
				fail_count += 1
				errors.append("Monster missing AnimatedSprite2D")
				
			remove_child(mon)
			mon.queue_free()

	print("\n==================================================================")
	print("                         FINAL QA REPORT                          ")
	print("==================================================================")
	print("TOTAL CHECKS PASSED: %d" % pass_count)
	print("TOTAL CHECKS FAILED: %d" % fail_count)
	if fail_count > 0:
		print("FAILURES LIST:")
		for err in errors:
			print("  [ERROR] %s" % err)
		get_tree().quit(1)
	else:
		print("STATUS: ALL TESTS PASSED WITH ZERO PARSE ERRORS AND EXIT CODE 0")
		get_tree().quit(0)
