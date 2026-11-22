extends Area2D
class_name ScrapItem

@export var item_type: String = "scrap"
@export var amount: int = 15

@onready var sprite: Sprite2D = $Sprite2D
@onready var label: Label = $Label

var is_collected: bool = false
var magnet_speed: float = 0.0

func _ready() -> void:
	add_to_group("Collectibles")
	body_entered.connect(_on_body_entered)
	_update_appearance()
	
	# Spawn pop-in animation
	scale = Vector2(0.2, 0.2)
	var pop_tween = create_tween()
	pop_tween.tween_property(self, "scale", Vector2(1.0, 1.0), 0.22).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	
	# Hover bobbing animation
	var bob_tween = create_tween().set_loops()
	bob_tween.tween_property(sprite, "position:y", -4.0, 0.45).set_trans(Tween.TRANS_SINE)
	bob_tween.tween_property(sprite, "position:y", 4.0, 0.45).set_trans(Tween.TRANS_SINE)

func setup(type: String, qty: int = 15) -> void:
	item_type = type
	amount = qty
	_update_appearance()

func _update_appearance() -> void:
	if not sprite or not label:
		return
		
	match item_type:
		"scrap", "garbage":
			label.text = "SCRAP +%d" % amount
			label.modulate = Color(1.0, 0.88, 0.3)
			sprite.modulate = Color(1.0, 0.88, 0.3)
		"wood":
			label.text = "WOOD"
			label.modulate = Color(0.8, 0.55, 0.3)
			sprite.modulate = Color(0.7, 0.45, 0.2)
		"plastic":
			label.text = "PLASTIC"
			label.modulate = Color(0.4, 0.85, 1.0)
			sprite.modulate = Color(0.3, 0.8, 0.95)
		"iron":
			label.text = "IRON"
			label.modulate = Color(0.85, 0.85, 0.9)
			sprite.modulate = Color(0.85, 0.85, 0.9)

func _physics_process(delta: float) -> void:
	if is_collected:
		return
		
	# Magnet attraction towards nearby active local player
	var players = get_tree().get_nodes_in_group("Players")
	for p in players:
		if p is ScrapboundPlayer and is_instance_valid(p) and not p.is_dead and p.is_multiplayer_authority():
			var dist = global_position.distance_to(p.global_position)
			if dist < 85.0:
				magnet_speed = move_toward(magnet_speed, 420.0, delta * 900.0)
				global_position = global_position.move_toward(p.global_position, delta * magnet_speed)
				if dist < 18.0:
					_collect_by_player(p)
				break

func _on_body_entered(body: Node2D) -> void:
	if is_collected:
		return
	if body is ScrapboundPlayer and body.is_multiplayer_authority():
		_collect_by_player(body)

func _collect_by_player(p: ScrapboundPlayer) -> void:
	if is_collected:
		return
	is_collected = true
	var main = get_tree().get_first_node_in_group("Main") as ScrapboundMain
	if not main:
		main = get_parent() as ScrapboundMain
	if main:
		main.request_collect_scrap.rpc_id(1, name, p.player_id)
