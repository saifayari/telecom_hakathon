extends Area2D
class_name ScrapboundBullet

@export var speed: float = 520.0
@export var damage: int = 25
@export var lifetime: float = 2.0
@export var is_piercing: bool = false
@export var shooter_player_id: int = 1

var direction: Vector2 = Vector2.RIGHT

@onready var sprite: Sprite2D = $Sprite2D
@onready var collision_shape: CollisionShape2D = $CollisionShape2D

var pierced_count: int = 0
const MAX_PIERCE: int = 3

func _ready() -> void:
	add_to_group("Projectiles")
	rotation = direction.angle()
	
	body_entered.connect(_on_body_entered)
	area_entered.connect(_on_area_entered)
	
	var timer = get_tree().create_timer(lifetime)
	timer.timeout.connect(queue_free)

func set_bullet_color(color: Color) -> void:
	if sprite:
		sprite.modulate = color

func _physics_process(delta: float) -> void:
	position += direction * speed * delta

func _on_body_entered(body: Node2D) -> void:
	_handle_hit(body)

func _on_area_entered(area: Area2D) -> void:
	_handle_hit(area)

func _handle_hit(target: Node2D) -> void:
	if target.is_in_group("Enemies"):
		if target.has_method("take_damage"):
			target.take_damage(damage, shooter_player_id)
		
		if not is_piercing:
			queue_free()
		else:
			pierced_count += 1
			if pierced_count >= MAX_PIERCE:
				queue_free()
	elif target.is_in_group("Obstacles") or target.is_in_group("WorldBounds"):
		queue_free()
