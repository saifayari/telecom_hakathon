extends Area2D
class_name ScrapItem

@export var item_type: String = "scrap"
@export var amount: int = 1

@onready var sprite: Sprite2D = $Sprite2D
@onready var label: Label = $Label

var is_collected: bool = false

func _ready() -> void:
	add_to_group("Collectibles")
	body_entered.connect(_on_body_entered)
	_update_appearance()
	
	var tween = create_tween().set_loops()
	tween.tween_property(sprite, "position:y", -3.0, 0.4).set_trans(Tween.TRANS_SINE)
	tween.tween_property(sprite, "position:y", 3.0, 0.4).set_trans(Tween.TRANS_SINE)

func setup(type: String, qty: int = 1) -> void:
	item_type = type
	amount = qty
	_update_appearance()

func _update_appearance() -> void:
	if not sprite or not label:
		return
		
	match item_type:
		"scrap":
			label.text = "SCRAP +%d" % amount
			label.modulate = Color(1.0, 0.85, 0.3)
			sprite.modulate = Color(1.0, 0.85, 0.3)
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

func _on_body_entered(body: Node2D) -> void:
	if is_collected:
		return
	if body is ScrapboundPlayer:
		if body.is_multiplayer_authority():
			is_collected = true
			var main = get_parent() as ScrapboundMain
			if main:
				main.request_collect_scrap.rpc_id(1, name, body.player_id)
