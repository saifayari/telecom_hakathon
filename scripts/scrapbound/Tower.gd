extends StaticBody2D
class_name ScrapboundTower

signal tower_health_changed(tower_id: int, current_hp: int, max_hp: int)
signal tower_destroyed(tower_id: int)

@export var tower_id: int = 1:
	set(val):
		tower_id = val
		if is_node_ready():
			_update_team_visuals()

@export var max_health: int = 1000
var health: int = 1000

@onready var tower_sprite: Sprite2D = $TowerSprite
@onready var health_bar: ProgressBar = $HealthBar
@onready var name_label: Label = $NameLabel
@onready var spawn_point: Marker2D = $SpawnPoint
@onready var emission_glow: Sprite2D = get_node_or_null("EmissionGlow")

func _ready() -> void:
	add_to_group("Towers")
	health = max_health
	
	if health_bar:
		health_bar.max_value = max_health
		health_bar.value = health
		
	_update_team_visuals()

func _update_team_visuals() -> void:
	# Keep the authentic, original color of the telecom tower
	var main_tex = "res://assets/sprites/props/telecom_tower_dq2l.png"
	if not ResourceLoader.exists(main_tex):
		main_tex = "res://assets/sprites/environment/telecom_tower_dq2l.png"
	if not ResourceLoader.exists(main_tex):
		main_tex = "res://assets/sprites/environment/telecom_tower_gemini_p1.png" if tower_id == 1 else "res://assets/sprites/environment/telecom_tower_gemini_p2.png"

	if tower_sprite and ResourceLoader.exists(main_tex):
		tower_sprite.texture = load(main_tex)
		tower_sprite.modulate = Color.WHITE

	# Enlarged scale
	if tower_sprite and tower_sprite.texture:
		var tex_h = tower_sprite.texture.get_height()
		if tex_h > 1000:
			tower_sprite.position = Vector2(0, -48)
			tower_sprite.scale = Vector2(0.24, 0.24)
		else:
			tower_sprite.position = Vector2(0, -20)
			tower_sprite.scale = Vector2(0.42, 0.42)

	if tower_id == 1:
		if name_label:
			name_label.text = "P1 TELECOM TOWER"
			name_label.modulate = Color(0.2, 0.85, 1.0)
		if emission_glow:
			emission_glow.modulate = Color(0.2, 0.85, 1.0, 0.8)
	else:
		if name_label:
			name_label.text = "P2 TELECOM TOWER"
			name_label.modulate = Color(1.0, 0.65, 0.2)
		if emission_glow:
			emission_glow.modulate = Color(1.0, 0.65, 0.2, 0.8)

func _process(delta: float) -> void:
	if emission_glow:
		var epulse = sin(Time.get_ticks_msec() * 0.008) * 0.12 + 0.88
		emission_glow.scale = Vector2(0.8, 0.8) * epulse

func take_damage_server(amount: int) -> void:
	if not multiplayer.is_server() or health <= 0:
		return
	health = max(0, health - amount)
	sync_tower_hp_net.rpc(health)
	
	if health <= 0:
		tower_destroyed.emit(tower_id)

func repair_server(amount: int) -> void:
	if not multiplayer.is_server() or health <= 0:
		return
	health = min(max_health, health + amount)
	sync_tower_hp_net.rpc(health)

@rpc("call_local", "reliable")
func sync_tower_hp_net(new_hp: int) -> void:
	health = new_hp
	if health_bar:
		health_bar.value = health
		
	tower_health_changed.emit(tower_id, health, max_health)
	
	# Damage impact flash
	if tower_sprite:
		tower_sprite.modulate = Color(2.4, 0.4, 0.4)
		var t = get_tree().create_timer(0.14)
		t.timeout.connect(func():
			if is_instance_valid(self) and tower_sprite:
				tower_sprite.modulate = Color.WHITE
		)

func get_spawn_position() -> Vector2:
	if spawn_point:
		return spawn_point.global_position
	return global_position + Vector2(60 if tower_id == 1 else -60, 20)
