extends Node2D
class_name ScrapboundMain

@export var match_duration: float = 120.0
var match_timer: float = 120.0
var is_match_running: bool = true

var p1_score: int = 0
var p1_kills: int = 0
var p2_score: int = 0
var p2_kills: int = 0

var spawn_timer: float = 1.0
var spawn_interval: float = 3.5
var next_entity_id: int = 1

var monster_scene = preload("res://scenes/scrapbound/Monster.tscn")
var scrap_item_scene = preload("res://scenes/scrapbound/ScrapItem.tscn")
var barrier_scene = preload("res://scenes/scrapbound/Barrier.tscn")

@onready var p1: ScrapboundPlayer = $Player1
@onready var p2: ScrapboundPlayer = $Player2
@onready var tower1: ScrapboundTower = $Tower1
@onready var tower2: ScrapboundTower = $Tower2
@onready var recycler1: ScrapRecycler = $Recycler1
@onready var recycler2: ScrapRecycler = $Recycler2
@onready var hud: ScrapboundHUD = $CanvasLayer/ScrapboundHUD

func _ready() -> void:
	match_timer = match_duration
	is_match_running = true
	
	# Determine peer authorities
	var client_peer_id = 1
	for id in NetworkManager.players:
		if id != 1:
			client_peer_id = id
			break
			
	if p1: p1.setup_network_authority(1, 1)
	if p2: p2.setup_network_authority(client_peer_id, 2)
	
	var my_local_id = NetworkManager.get_my_player_id()
	if hud:
		hud.set_local_player(my_local_id)
		hud.rematch_requested.connect(_on_rematch_pressed)
		
	if tower1: tower1.tower_destroyed.connect(_on_tower_destroyed)
	if tower2: tower2.tower_destroyed.connect(_on_tower_destroyed)
	
	_broadcast_full_hud_sync()
	print("[SCRAPBOUND ONLINE] Arena loaded! Local Player ID: %d | Is Host: %s" % [my_local_id, multiplayer.is_server()])

func _physics_process(delta: float) -> void:
	if not is_match_running:
		return
		
	# Match timing and monster spawning are strictly server-authoritative
	if multiplayer.is_server():
		match_timer -= delta
		sync_timer_net.rpc(match_timer)
		
		if match_timer <= 0.0:
			end_match_server()
			return
			
		spawn_timer -= delta
		if spawn_timer <= 0.0:
			spawn_timer = spawn_interval
			spawn_interval = max(1.8, 3.5 - ((120.0 - match_timer) / 120.0) * 1.5)
			_spawn_monster_server()

@rpc("unreliable")
func sync_timer_net(time_left: float) -> void:
	match_timer = time_left
	if hud:
		hud.update_timer(match_timer)

func _spawn_monster_server() -> void:
	if not multiplayer.is_server():
		return
		
	var spawn_points = [
		Vector2(randf_range(350, 730), 45),
		Vector2(randf_range(350, 730), 555),
		Vector2(randf_range(200, 400), 50),
		Vector2(randf_range(680, 880), 550),
		Vector2(540, 45)
	]
	var pos = spawn_points[randi() % spawn_points.size()]
	next_entity_id += 1
	spawn_monster_net.rpc(next_entity_id, pos)

@rpc("call_local", "reliable")
func spawn_monster_net(m_id: int, pos: Vector2) -> void:
	var m = monster_scene.instantiate()
	m.name = "Monster_%d" % m_id
	m.global_position = pos
	add_child(m)

func on_monster_destroyed_server(_monster: Node2D, killer_id: int, pos: Vector2) -> void:
	if not multiplayer.is_server():
		return
		
	if killer_id == 1:
		p1_kills += 1
		p1_score += 100
	elif killer_id == 2:
		p2_kills += 1
		p2_score += 100
		
	# Spawn scrap drop
	next_entity_id += 1
	spawn_scrap_drop_net.rpc(next_entity_id, "scrap", randi_range(10, 20), pos)
	
	# Spawn random building material drop
	var mats = ["wood", "plastic", "iron"]
	var chosen_mat = mats[randi() % mats.size()]
	next_entity_id += 1
	spawn_scrap_drop_net.rpc(next_entity_id, chosen_mat, 1, pos + Vector2(randf_range(-16, 16), randf_range(-16, 16)))
	
	_broadcast_full_hud_sync()

@rpc("call_local", "reliable")
func spawn_scrap_drop_net(item_id: int, item_type: String, qty: int, pos: Vector2) -> void:
	var item = scrap_item_scene.instantiate()
	item.name = "ScrapItem_%d" % item_id
	item.global_position = pos
	item.setup(item_type, qty)
	add_child(item)

# Client -> Server: Request to collect scrap
@rpc("any_peer", "call_local", "reliable")
func request_collect_scrap(item_node_name: String, collector_id: int) -> void:
	if not multiplayer.is_server():
		return
		
	var item_node = get_node_or_null(item_node_name) as ScrapItem
	if item_node and is_instance_valid(item_node):
		var target_player = p1 if collector_id == 1 else p2
		if target_player:
			target_player.add_resource(item_node.item_type, item_node.amount)
			sync_inventory_net.rpc(collector_id, target_player.inventory)
			remove_scrap_item_net.rpc(item_node_name)

@rpc("call_local", "reliable")
func remove_scrap_item_net(item_node_name: String) -> void:
	var item_node = get_node_or_null(item_node_name)
	if item_node and is_instance_valid(item_node):
		item_node.queue_free()

# Client -> Server: Request to recycle scrap
@rpc("any_peer", "call_local", "reliable")
func request_recycle(r_id: int, player_id: int) -> void:
	if not multiplayer.is_server():
		return
		
	var target_player = p1 if player_id == 1 else p2
	if not target_player or target_player.inventory["scrap"] < 15:
		return
		
	target_player.inventory["scrap"] -= 15
	var recycler = recycler1 if r_id == 1 else recycler2
	var reward = recycler.pick_weighted_output() if recycler else "material_a"
	target_player.add_resource(reward, 1)
	
	if recycler:
		recycler.play_recycle_effect_net.rpc(reward)
	sync_inventory_net.rpc(player_id, target_player.inventory)

# Client -> Server: Request to craft weapon
@rpc("any_peer", "call_local", "reliable")
func request_craft(player_id: int) -> void:
	if not multiplayer.is_server():
		return
		
	var p = p1 if player_id == 1 else p2
	if not p: return
	
	# Recipe 1: A + B = RapidFire
	if p.inventory["material_a"] >= 1 and p.inventory["material_b"] >= 1 and p.current_weapon != "RapidFire":
		p.inventory["material_a"] -= 1
		p.inventory["material_b"] -= 1
		p.set_weapon("RapidFire")
		sync_weapon_net.rpc(player_id, "RapidFire", p.inventory)
		return
		
	# Recipe 2: A + C = HighDamage
	if p.inventory["material_a"] >= 1 and p.inventory["material_c"] >= 1 and p.current_weapon != "HighDamage":
		p.inventory["material_a"] -= 1
		p.inventory["material_c"] -= 1
		p.set_weapon("HighDamage")
		sync_weapon_net.rpc(player_id, "HighDamage", p.inventory)
		return

@rpc("call_local", "reliable")
func sync_weapon_net(player_id: int, weapon_name: String, updated_inv: Dictionary) -> void:
	var p = p1 if player_id == 1 else p2
	if p:
		p.set_weapon(weapon_name)
		p.inventory = updated_inv
	_broadcast_full_hud_sync()

# Client -> Server: Request to build barrier
@rpc("any_peer", "call_local", "reliable")
func request_build_barrier(builder_id: int, spawn_pos: Vector2) -> void:
	if not multiplayer.is_server():
		return
		
	var p = p1 if builder_id == 1 else p2
	if not p: return
	
	var total_mats = p.inventory["wood"] + p.inventory["plastic"] + p.inventory["iron"]
	if total_mats < 2:
		return
		
	var needed = 2
	for mat in ["wood", "plastic", "iron"]:
		while p.inventory[mat] > 0 and needed > 0:
			p.inventory[mat] -= 1
			needed -= 1
			
	next_entity_id += 1
	spawn_barrier_net.rpc(next_entity_id, spawn_pos, builder_id, p.inventory)

@rpc("call_local", "reliable")
func spawn_barrier_net(b_id: int, spawn_pos: Vector2, builder_id: int, updated_inv: Dictionary) -> void:
	var p = p1 if builder_id == 1 else p2
	if p:
		p.inventory = updated_inv
		
	var b = barrier_scene.instantiate()
	b.name = "Barrier_%d" % b_id
	b.global_position = spawn_pos
	b.setup(builder_id)
	add_child(b)
	_broadcast_full_hud_sync()

@rpc("call_local", "reliable")
func sync_inventory_net(player_id: int, updated_inv: Dictionary) -> void:
	var p = p1 if player_id == 1 else p2
	if p:
		p.inventory = updated_inv
	_broadcast_full_hud_sync()

func _broadcast_full_hud_sync() -> void:
	if not is_instance_valid(hud):
		return
		
	var p1_hp = p1.health if is_instance_valid(p1) else 0
	var p1_wpn = p1.current_weapon if is_instance_valid(p1) else "Basic"
	var p1_inv = p1.inventory if is_instance_valid(p1) else {}
	var t1_hp = tower1.health if is_instance_valid(tower1) else 0
	
	var p2_hp = p2.health if is_instance_valid(p2) else 0
	var p2_wpn = p2.current_weapon if is_instance_valid(p2) else "Basic"
	var p2_inv = p2.inventory if is_instance_valid(p2) else {}
	var t2_hp = tower2.health if is_instance_valid(tower2) else 0
	
	if multiplayer.is_server():
		sync_hud_net.rpc(
			p1_hp, p1_score, p1_kills, t1_hp, p1_wpn, p1_inv,
			p2_hp, p2_score, p2_kills, t2_hp, p2_wpn, p2_inv
		)
	else:
		hud.update_player_ui(
			p1_hp, p1_score, p1_kills, t1_hp, p1_wpn, p1_inv,
			p2_hp, p2_score, p2_kills, t2_hp, p2_wpn, p2_inv
		)

@rpc("call_local", "reliable")
func sync_hud_net(
	p1_hp: int, p1_sc: int, p1_k: int, t1_hp: int, p1_wpn: String, p1_inv: Dictionary,
	p2_hp: int, p2_sc: int, p2_k: int, t2_hp: int, p2_wpn: String, p2_inv: Dictionary
) -> void:
	p1_score = p1_sc
	p1_kills = p1_k
	p2_score = p2_sc
	p2_kills = p2_k
	if hud:
		hud.update_player_ui(
			p1_hp, p1_sc, p1_k, t1_hp, p1_wpn, p1_inv,
			p2_hp, p2_sc, p2_k, t2_hp, p2_wpn, p2_inv
		)

func _on_tower_destroyed(destroyed_tower_id: int) -> void:
	if not multiplayer.is_server():
		return
	print("[SCRAPBOUND ONLINE] Tower %d destroyed! Concluding match." % destroyed_tower_id)
	end_match_server()

func end_match_server() -> void:
	if not multiplayer.is_server() or not is_match_running:
		return
	is_match_running = false
	var t1_hp = tower1.health if is_instance_valid(tower1) else 0
	var t2_hp = tower2.health if is_instance_valid(tower2) else 0
	sync_match_results_net.rpc(p1_kills, p1_score, t1_hp, p2_kills, p2_score, t2_hp)

@rpc("call_local", "reliable")
func sync_match_results_net(p1_k: int, p1_sc: int, t1_hp: int, p2_k: int, p2_sc: int, t2_hp: int) -> void:
	is_match_running = false
	if hud:
		hud.show_results(p1_k, p1_sc, t1_hp, p2_k, p2_sc, t2_hp)

func _on_rematch_pressed() -> void:
	if multiplayer.is_server():
		return_to_lobby_net.rpc()
	else:
		return_to_lobby_net()

@rpc("call_local", "reliable")
func return_to_lobby_net() -> void:
	NetworkManager.disconnect_game()
	get_tree().change_scene_to_file("res://scenes/scrapbound/Lobby.tscn")
