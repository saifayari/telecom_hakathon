extends StaticBody2D
class_name ScrapboundDefenseTower

@export var builder_player_id: int = 1
@export var max_health: int = 180
var health: int = 180
var attack_range: float = 240.0
var fire_rate: float = 0.50
var fire_cooldown: float = 0.0
var bullet_damage: int = 22

var bullet_scene = preload("res://scenes/scrapbound/Bullet.tscn")

@onready var base_sprite: Sprite2D = $BaseSprite
@onready var pivot: Node2D = $TurretPivot
@onready var gun_sprite: Sprite2D = $TurretPivot/GunSprite
@onready var muzzle: Marker2D = $TurretPivot/Muzzle
@onready var health_bar: ProgressBar = $HealthBar
@onready var label: Label = $Label
@onready var shoot_audio: AudioStreamPlayer2D = $ShootAudio

func _ready() -> void:
	add_to_group("Towers")
	add_to_group("Barriers")
	add_to_group("Obstacles")
	add_to_group("Turrets")
	health = max_health
	if health_bar:
		health_bar.max_value = max_health
		health_bar.value = health
		
	# Dynamically bind Gemini high-detail heavy turret asset
	var turret_tex_path = ProjectSettings.globalize_path("res://assets/sprites/turrets/turret_heavy_gemini_centered.png")
	if FileAccess.file_exists(turret_tex_path) and gun_sprite:
		var img = Image.new()
		if img.load(turret_tex_path) == OK:
			gun_sprite.texture = ImageTexture.create_from_image(img)
			
	_update_team_visuals()

func setup(p_id: int) -> void:
	builder_player_id = p_id
	_update_team_visuals()

func _update_team_visuals() -> void:
	if not label: return
	if builder_player_id == 1:
		label.text = "P1 HEAVY TURRET"
		label.modulate = Color(0.2, 0.85, 1.0)
		if gun_sprite: gun_sprite.modulate = Color(0.85, 1.0, 1.1)
	else:
		label.text = "P2 HEAVY TURRET"
		label.modulate = Color(1.0, 0.65, 0.2)
		if gun_sprite: gun_sprite.modulate = Color(1.1, 0.9, 0.75)

func _physics_process(delta: float) -> void:
	if not multiplayer.is_server():
		return
		
	fire_cooldown -= delta
	
	# Find closest monster on this player's side
	var target = _find_closest_enemy()
	if target and is_instance_valid(target):
		var dir = (target.global_position - global_position).normalized()
		var rot = dir.angle()
		sync_aim_net.rpc(rot)
		if fire_cooldown <= 0.0:
			fire_cooldown = fire_rate
			_fire_bullet_server(dir)

func _find_closest_enemy() -> ScrapboundMonster:
	var closest: ScrapboundMonster = null
	var min_dist = attack_range
	for m in get_tree().get_nodes_in_group("Enemies"):
		if m is ScrapboundMonster and is_instance_valid(m) and not m.is_dead:
			# Keep sentry targeting on player's side of the arena
			var is_on_side = (builder_player_id == 1 and m.global_position.x < 2816) or (builder_player_id == 2 and m.global_position.x > 2816)
			if is_on_side:
				var dist = global_position.distance_to(m.global_position)
				if dist < min_dist:
					min_dist = dist
					closest = m
	return closest

func _fire_bullet_server(dir: Vector2) -> void:
	var spawn_pos = muzzle.global_position if muzzle else global_position + dir * 28.0
	spawn_sentry_bullet_net.rpc(spawn_pos, dir, bullet_damage, builder_player_id)

@rpc("call_local", "reliable")
func spawn_sentry_bullet_net(spawn_pos: Vector2, dir: Vector2, dmg: int, shooter_id: int) -> void:
	var b = bullet_scene.instantiate()
	b.global_position = spawn_pos
	b.direction = dir
	b.damage = dmg
	b.speed = 540.0
	b.is_piercing = false
	b.shooter_player_id = shooter_id
	b.set_bullet_color(Color(0.3, 0.85, 1.0) if shooter_id == 1 else Color(1.0, 0.6, 0.2))
	get_parent().add_child.call_deferred(b)
	
	if shoot_audio:
		shoot_audio.pitch_scale = randf_range(0.95, 1.12)
		shoot_audio.play()

@rpc("call_local", "unreliable")
func sync_aim_net(rot: float) -> void:
	if pivot:
		pivot.rotation = rot

func take_damage_server(amount: int) -> void:
	if not multiplayer.is_server() or health <= 0:
		return
	health = max(0, health - amount)
	sync_defense_hp_net.rpc(health)
	if health <= 0:
		destroy_defense_tower_net.rpc()

@rpc("call_local", "reliable")
func sync_defense_hp_net(new_hp: int) -> void:
	health = new_hp
	if health_bar:
		health_bar.value = health
	if gun_sprite:
		gun_sprite.modulate = Color(2.4, 0.4, 0.4)
		var t = get_tree().create_timer(0.12)
		t.timeout.connect(func():
			if is_instance_valid(self): _update_team_visuals()
		)

@rpc("call_local", "reliable")
func destroy_defense_tower_net() -> void:
	set_physics_process(false)
	var col = get_node_or_null("CollisionShape2D")
	if col: col.set_deferred("disabled", true)
	queue_free()
