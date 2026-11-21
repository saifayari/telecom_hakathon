extends StaticBody2D
class_name ScrapSentry

@export var range_radius: float = 240.0
@export var fire_rate: float = 0.28
@export var damage: int = 20

@onready var sprite: Sprite2D = $Sprite2D
@onready var barrel_pivot: Node2D = $BarrelPivot
@onready var shoot_sfx: AudioStreamPlayer2D = $AudioShoot

var bullet_scene = preload("res://scenes/entities/Bullet.tscn")
var fire_timer: float = 0.0

func _ready() -> void:
	add_to_group("Turrets")

func _physics_process(delta: float) -> void:
	fire_timer -= delta
	
	var enemies = get_tree().get_nodes_in_group("Enemies")
	var target: Node2D = null
	var min_dist = range_radius
	
	for e in enemies:
		if is_instance_valid(e):
			var d = global_position.distance_to(e.global_position)
			if d < min_dist:
				min_dist = d
				target = e
				
	if target:
		var dir = (target.global_position - global_position).normalized()
		if barrel_pivot:
			barrel_pivot.rotation = dir.angle()
			
		if fire_timer <= 0.0:
			fire_timer = fire_rate
			_shoot(dir)

func _shoot(dir: Vector2) -> void:
	var b = bullet_scene.instantiate()
	b.global_position = global_position + dir * 16.0
	b.direction = dir
	b.damage = damage
	get_parent().add_child(b)
	
	if shoot_sfx:
		shoot_sfx.pitch_scale = randf_range(0.9, 1.1)
		shoot_sfx.play()
