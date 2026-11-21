extends Area2D
class_name Shockwave

@export var max_radius: float = 150.0
@export var duration: float = 0.4
@export var damage: int = 150
@export var stun_duration: float = 3.0

@onready var sprite: Sprite2D = $Sprite2D
@onready var collision_shape: CollisionShape2D = $CollisionShape2D
@onready var circle_shape: CircleShape2D = collision_shape.shape

var hit_enemies: Array[Node2D] = []

func _ready() -> void:
	circle_shape.radius = 10.0
	scale = Vector2(0.1, 0.1)
	modulate = Color(0.2, 0.8, 1.0, 0.9)
	
	# Tween expansion
	var tween = create_tween().set_parallel(true)
	tween.tween_property(self, "scale", Vector2(1.0, 1.0), duration).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	tween.tween_property(self, "modulate:a", 0.0, duration).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
	tween.finished.connect(queue_free)
	
	area_entered.connect(_on_area_entered)
	body_entered.connect(_on_body_entered)
	
	# Play shockwave sound
	var sfx = $AudioStreamPlayer2D
	if sfx:
		sfx.play()

func _physics_process(_delta: float) -> void:
	circle_shape.radius = max_radius * scale.x

func _on_body_entered(body: Node2D) -> void:
	_try_hit(body)

func _on_area_entered(area: Area2D) -> void:
	_try_hit(area)

func _try_hit(target: Node2D) -> void:
	if target in hit_enemies:
		return
		
	if target.is_in_group("Enemies"):
		hit_enemies.append(target)
		if target.has_method("take_damage"):
			target.take_damage(damage)
		if target.has_method("apply_em_stun"):
			target.apply_em_stun(stun_duration)
