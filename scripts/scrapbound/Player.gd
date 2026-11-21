extends CharacterBody2D
class_name ScrapboundPlayer

signal player_died(player_id: int, respawn_time: float)
signal player_respawned(player_id: int)
signal inventory_changed(player_id: int, inventory: Dictionary)
signal weapon_upgraded(player_id: int, weapon_name: String)

@export var player_id: int = 1
@export var speed: float = 190.0
@export var max_health: int = 100
var health: int = 100

var death_count: int = 0
var is_dead: bool = false
var respawn_timer: float = 0.0

var current_weapon: String = "Basic"
var shoot_cooldown: float = 0.0
var shoot_rate: float = 0.22
var bullet_damage: int = 25
var bullet_speed: float = 520.0
var is_piercing: bool = false

var aim_direction: Vector2 = Vector2.RIGHT

var inventory: Dictionary = {
	"scrap": 0,
	"battery": 0,
	"material_a": 0,
	"material_b": 0,
	"material_c": 0,
	"material_d": 0,
	"wood": 0,
	"plastic": 0,
	"iron": 0
}

var nearby_recycler: Node2D = null

var bullet_scene = preload("res://scenes/scrapbound/Bullet.tscn")

@onready var anim_sprite: AnimatedSprite2D = $AnimatedSprite2D
@onready var health_bar: ProgressBar = $HealthBar
@onready var name_label: Label = $NameLabel
@onready var respawn_label: Label = $RespawnLabel
@onready var collision_shape: CollisionShape2D = $CollisionShape2D
@onready var weapon_pivot: Node2D = $WeaponPivot
@onready var gun_sprite: Sprite2D = $WeaponPivot/GunSprite
@onready var shoot_audio: AudioStreamPlayer2D = $ShootAudio

# Target transform for remote interpolation
var remote_target_pos: Vector2 = Vector2.ZERO

func _ready() -> void:
	add_to_group("Players")
	health = max_health
	remote_target_pos = global_position
	
	if health_bar:
		health_bar.max_value = max_health
		health_bar.value = health
		
	if respawn_label:
		respawn_label.visible = false
		
	_apply_visual_theme()

func setup_network_authority(peer_id: int, assigned_id: int) -> void:
	player_id = assigned_id
	set_multiplayer_authority(peer_id)
	_apply_visual_theme()
	aim_direction = Vector2.RIGHT if player_id == 1 else Vector2.LEFT

func _apply_visual_theme() -> void:
	if not is_inside_tree():
		return
	if player_id == 1:
		if name_label:
			name_label.text = "P1 (YOU)" if is_multiplayer_authority() else "P1"
			name_label.modulate = Color(0.2, 0.85, 1.0)
		if anim_sprite:
			anim_sprite.self_modulate = Color(0.65, 0.9, 1.0)
		if gun_sprite:
			gun_sprite.modulate = Color(0.4, 0.9, 1.0)
	else:
		if name_label:
			name_label.text = "P2 (YOU)" if is_multiplayer_authority() else "P2"
			name_label.modulate = Color(1.0, 0.6, 0.2)
		if anim_sprite:
			anim_sprite.self_modulate = Color(1.0, 0.75, 0.5)
		if gun_sprite:
			gun_sprite.modulate = Color(1.0, 0.65, 0.3)

func _physics_process(delta: float) -> void:
	if is_dead:
		if multiplayer.is_server():
			_process_respawn_server(delta)
		return
		
	shoot_cooldown -= delta
	
	# Only the player who owns this character processes local inputs
	if is_multiplayer_authority():
		_handle_local_input()
		# Broadcast position and animation state
		var anim_name = anim_sprite.animation if anim_sprite else "idle"
		var flip_h = anim_sprite.flip_h if anim_sprite else false
		sync_transform.rpc(global_position, velocity, anim_name, flip_h, aim_direction)
	else:
		# Remote puppet: smoothly interpolate towards received network position
		if global_position.distance_to(remote_target_pos) > 1.0:
			global_position = global_position.lerp(remote_target_pos, delta * 20.0)

@rpc("unreliable_ordered")
func sync_transform(pos: Vector2, vel: Vector2, anim: String, flip: bool, aim_dir: Vector2) -> void:
	if is_multiplayer_authority():
		return
	remote_target_pos = pos
	velocity = vel
	aim_direction = aim_dir
	if anim_sprite:
		if anim_sprite.animation != anim:
			anim_sprite.play(anim)
		anim_sprite.flip_h = flip
	if weapon_pivot:
		weapon_pivot.rotation = aim_direction.angle()
		weapon_pivot.scale.y = -1.0 if aim_direction.x < 0 else 1.0

func _handle_local_input() -> void:
	var move_vec = Vector2.ZERO
	
	# Unified controls: WASD or Arrow Keys
	if Input.is_key_pressed(KEY_A) or Input.is_key_pressed(KEY_LEFT):
		move_vec.x -= 1.0
	if Input.is_key_pressed(KEY_D) or Input.is_key_pressed(KEY_RIGHT):
		move_vec.x += 1.0
	if Input.is_key_pressed(KEY_W) or Input.is_key_pressed(KEY_UP):
		move_vec.y -= 1.0
	if Input.is_key_pressed(KEY_S) or Input.is_key_pressed(KEY_DOWN):
		move_vec.y += 1.0
		
	if move_vec != Vector2.ZERO:
		move_vec = move_vec.normalized()
		velocity = move_vec * speed
		aim_direction = move_vec
		if anim_sprite and anim_sprite.animation != "walk":
			anim_sprite.play("walk")
		if anim_sprite:
			anim_sprite.flip_h = (aim_direction.x < 0)
	else:
		velocity = velocity.move_toward(Vector2.ZERO, speed)
		if anim_sprite and anim_sprite.animation != "idle":
			anim_sprite.play("idle")
			
	if weapon_pivot:
		weapon_pivot.rotation = aim_direction.angle()
		weapon_pivot.scale.y = -1.0 if aim_direction.x < 0 else 1.0
		
	move_and_slide()
	
	# Attack: SPACE or K or ENTER
	if (Input.is_key_pressed(KEY_SPACE) or Input.is_key_pressed(KEY_K) or Input.is_key_pressed(KEY_ENTER)) and shoot_cooldown <= 0.0:
		shoot_cooldown = shoot_rate
		request_shoot.rpc_id(1, global_position + aim_direction * 18.0, aim_direction)
		
	# Interact / Recycle / Craft: E or L
	if Input.is_key_pressed(KEY_E) or Input.is_key_pressed(KEY_L):
		if nearby_recycler and is_instance_valid(nearby_recycler):
			var main = get_parent() as ScrapboundMain
			if main:
				main.request_recycle.rpc_id(1, nearby_recycler.recycler_id, player_id)
		else:
			var main = get_parent() as ScrapboundMain
			if main:
				main.request_craft.rpc_id(1, player_id)
				
	# Build Barrier: Q or O
	if Input.is_key_pressed(KEY_Q) or Input.is_key_pressed(KEY_O):
		var main = get_parent() as ScrapboundMain
		if main:
			main.request_build_barrier.rpc_id(1, player_id, global_position + aim_direction * 36.0)

@rpc("any_peer", "call_local", "reliable")
func request_shoot(spawn_pos: Vector2, dir: Vector2) -> void:
	if not multiplayer.is_server():
		return
	# Server validates and broadcasts bullet spawn
	spawn_bullet_net.rpc(spawn_pos, dir, bullet_damage, bullet_speed, is_piercing, player_id)

@rpc("call_local", "reliable")
func spawn_bullet_net(spawn_pos: Vector2, dir: Vector2, dmg: int, spd: float, pierce: bool, shooter_id: int) -> void:
	var b = bullet_scene.instantiate()
	b.global_position = spawn_pos
	b.direction = dir
	b.damage = dmg
	b.speed = spd
	b.is_piercing = pierce
	b.shooter_player_id = shooter_id
	b.set_bullet_color(Color(0.3, 0.85, 1.0) if shooter_id == 1 else Color(1.0, 0.6, 0.2))
	get_parent().add_child(b)
	
	if shoot_audio:
		shoot_audio.pitch_scale = randf_range(0.95, 1.05)
		shoot_audio.play()

func take_damage_server(amount: int) -> void:
	if not multiplayer.is_server() or is_dead:
		return
	health = max(0, health - amount)
	sync_health_net.rpc(health)
	
	if health <= 0:
		die_server()

@rpc("call_local", "reliable")
func sync_health_net(new_hp: int) -> void:
	health = new_hp
	if health_bar:
		health_bar.value = health
	if anim_sprite:
		anim_sprite.modulate = Color(2.0, 0.4, 0.4)
		var t = get_tree().create_timer(0.12)
		t.timeout.connect(func():
			if is_instance_valid(self) and anim_sprite: anim_sprite.modulate = Color.WHITE
		)

func die_server() -> void:
	if not multiplayer.is_server() or is_dead:
		return
	is_dead = true
	death_count += 1
	respawn_timer = death_count * 5.0
	sync_death_net.rpc(respawn_timer)

@rpc("call_local", "reliable")
func sync_death_net(duration: float) -> void:
	is_dead = true
	respawn_timer = duration
	if anim_sprite: anim_sprite.visible = false
	if weapon_pivot: weapon_pivot.visible = false
	if health_bar: health_bar.visible = false
	if collision_shape: collision_shape.set_deferred("disabled", true)
	if respawn_label:
		respawn_label.visible = true
		respawn_label.text = "RESPAWN: %ds" % int(ceil(respawn_timer))
	player_died.emit(player_id, respawn_timer)

func _process_respawn_server(delta: float) -> void:
	respawn_timer -= delta
	sync_respawn_timer_net.rpc(respawn_timer)
	if respawn_timer <= 0.0:
		respawn_server()

@rpc("call_local", "unreliable")
func sync_respawn_timer_net(time_left: float) -> void:
	respawn_timer = time_left
	if respawn_label:
		respawn_label.text = "RESPAWN: %ds" % int(ceil(max(0.0, respawn_timer)))

func respawn_server() -> void:
	if not multiplayer.is_server():
		return
	is_dead = false
	health = max_health
	
	var towers = get_tree().get_nodes_in_group("Towers")
	var spawn_pos = global_position
	for t in towers:
		if is_instance_valid(t) and t.tower_id == player_id:
			spawn_pos = t.get_spawn_position()
			break
			
	sync_respawn_net.rpc(spawn_pos)

@rpc("call_local", "reliable")
func sync_respawn_net(spawn_pos: Vector2) -> void:
	is_dead = false
	health = max_health
	global_position = spawn_pos
	remote_target_pos = spawn_pos
	
	if health_bar:
		health_bar.value = health
		health_bar.visible = true
	if anim_sprite:
		anim_sprite.visible = true
		anim_sprite.modulate = Color.WHITE
	if weapon_pivot: weapon_pivot.visible = true
	if collision_shape: collision_shape.set_deferred("disabled", false)
	if respawn_label: respawn_label.visible = false
	
	player_respawned.emit(player_id)

func set_weapon(weapon_type: String) -> void:
	current_weapon = weapon_type
	if weapon_type == "RapidFire":
		shoot_rate = 0.11
		bullet_damage = 18
		bullet_speed = 620.0
		is_piercing = false
	elif weapon_type == "HighDamage":
		shoot_rate = 0.38
		bullet_damage = 60
		bullet_speed = 460.0
		is_piercing = true
	else:
		shoot_rate = 0.22
		bullet_damage = 25
		bullet_speed = 520.0
		is_piercing = false
	weapon_upgraded.emit(player_id, current_weapon)

func add_resource(res_name: String, amount: int = 1) -> void:
	if res_name in inventory:
		inventory[res_name] += amount
		inventory_changed.emit(player_id, inventory)
