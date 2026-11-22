extends StaticBody2D
class_name ScrapboundTower

signal tower_health_changed(tower_id: int, current_hp: int, max_hp: int)
signal tower_destroyed(tower_id: int)

@export var tower_id: int = 1
@export var max_health: int = 1000
var health: int = 1000

@onready var tower_sprite: Sprite2D = $TowerSprite
@onready var health_bar: ProgressBar = $HealthBar
@onready var name_label: Label = $NameLabel
@onready var spawn_point: Marker2D = $SpawnPoint

func _ready() -> void:
	add_to_group("Towers")
	health = max_health
	
	if health_bar:
		health_bar.max_value = max_health
		health_bar.value = health
		
	# Dynamically load authentic high-detail telecom tower texture with team frequency lights
	var p_tex = "res://assets/sprites/environment/telecom_tower_p1.png" if tower_id == 1 else "res://assets/sprites/environment/telecom_tower_p2.png"
	var global_path = ProjectSettings.globalize_path(p_tex)
	if FileAccess.file_exists(global_path) and tower_sprite:
		var img = Image.new()
		if img.load(global_path) == OK:
			tower_sprite.texture = ImageTexture.create_from_image(img)
	
	# Solid fixed scale: stationary, no wobbling or blinking
	if tower_sprite:
		tower_sprite.scale = Vector2(0.85, 0.85)
		
	if tower_id == 1:
		if name_label:
			name_label.text = "P1 TELECOM TOWER"
			name_label.modulate = Color(0.2, 0.85, 1.0)
	else:
		if name_label:
			name_label.text = "P2 TELECOM TOWER"
			name_label.modulate = Color(1.0, 0.65, 0.2)

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
	
	# Damage impact flash: flashes red briefly, then cleanly restores normal appearance
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
