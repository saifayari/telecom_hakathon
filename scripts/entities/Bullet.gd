extends Area2D
class_name Bullet

@export var speed: float = 650.0
@export var damage: int = 35
@export var lifetime: float = 1.5

var direction: Vector2 = Vector2.RIGHT

func _ready() -> void:
	rotation = direction.angle()
	var timer = get_tree().create_timer(lifetime)
	timer.timeout.connect(queue_free)
	body_entered.connect(_on_body_entered)

func _physics_process(delta: float) -> void:
	position += direction * speed * delta

func _on_body_entered(body: Node2D) -> void:
	if body.is_in_group("Enemies") and body.has_method("take_damage"):
		body.take_damage(damage)
		queue_free()
	elif body is StaticBody2D or body is TileMapLayer:
		queue_free()
