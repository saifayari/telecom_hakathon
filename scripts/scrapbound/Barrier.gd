extends StaticBody2D
class_name ScrapboundBarrier

@export var max_health: int = 150
var health: int = 150
@export var built_by_player_id: int = 1

@onready var sprite: Sprite2D = $Sprite2D
@onready var health_bar: ProgressBar = $HealthBar
@onready var collision_shape: CollisionShape2D = $CollisionShape2D

func _ready() -> void:
	add_to_group("Barriers")
	add_to_group("Obstacles")
	health = max_health
	
	if health_bar:
		health_bar.max_value = max_health
		health_bar.value = health
		
	if sprite:
		sprite.modulate = Color(0.3, 0.85, 1.0) if built_by_player_id == 1 else Color(1.0, 0.65, 0.3)

func setup(p_id: int) -> void:
	built_by_player_id = p_id
	if sprite:
		sprite.modulate = Color(0.3, 0.85, 1.0) if built_by_player_id == 1 else Color(1.0, 0.65, 0.3)

func take_damage_server(amount: int) -> void:
	if not multiplayer.is_server():
		return
	health -= amount
	sync_barrier_hp_net.rpc(health)
	if health <= 0:
		remove_barrier_net.rpc()

@rpc("call_local", "reliable")
func sync_barrier_hp_net(new_hp: int) -> void:
	health = new_hp
	if health_bar:
		health_bar.value = health
	if sprite:
		sprite.modulate = Color(2.0, 0.4, 0.4)
		var t = get_tree().create_timer(0.1)
		t.timeout.connect(func():
			if is_instance_valid(self) and sprite:
				sprite.modulate = Color(0.3, 0.85, 1.0) if built_by_player_id == 1 else Color(1.0, 0.65, 0.3)
		)

@rpc("call_local", "reliable")
func remove_barrier_net() -> void:
	queue_free()
