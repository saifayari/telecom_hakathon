extends StaticBody2D
class_name ScrapboundTower

signal tower_health_changed(tower_id: int, current_hp: int, max_hp: int)
signal tower_destroyed(tower_id: int)

@export var tower_id: int = 1
@export var max_health: int = 1000
var health: int = 1000

@onready var health_bar: ProgressBar = $HealthBar
@onready var name_label: Label = $NameLabel
@onready var sprite: Sprite2D = $Sprite2D
@onready var spawn_point: Marker2D = $SpawnPoint

func _ready() -> void:
	add_to_group("Towers")
	health = max_health
	
	if health_bar:
		health_bar.max_value = max_health
		health_bar.value = health
		
	if tower_id == 1:
		name_label.text = "P1 TOWER"
		name_label.modulate = Color(0.2, 0.8, 1.0)
		if sprite:
			sprite.modulate = Color(0.7, 0.9, 1.0)
	else:
		name_label.text = "P2 TOWER"
		name_label.modulate = Color(1.0, 0.5, 0.2)
		if sprite:
			sprite.modulate = Color(1.0, 0.8, 0.7)

func take_damage_server(amount: int) -> void:
	if not multiplayer.is_server() or health <= 0:
		return
	health = max(0, health - amount)
	sync_tower_hp_net.rpc(health)
	
	if health <= 0:
		tower_destroyed.emit(tower_id)

@rpc("call_local", "reliable")
func sync_tower_hp_net(new_hp: int) -> void:
	health = new_hp
	if health_bar:
		health_bar.value = health
		
	tower_health_changed.emit(tower_id, health, max_health)
	
	if sprite:
		sprite.modulate = Color(2.0, 0.5, 0.5)
		var t = get_tree().create_timer(0.12)
		t.timeout.connect(func():
			if is_instance_valid(self) and sprite:
				sprite.modulate = Color(0.7, 0.9, 1.0) if tower_id == 1 else Color(1.0, 0.8, 0.7)
		)

func get_spawn_position() -> Vector2:
	if spawn_point:
		return spawn_point.global_position
	return global_position + Vector2(40 if tower_id == 1 else -40, 0)
