extends Area2D
class_name ScrapRecycler

@export var recycler_id: int = 1
@export var scrap_cost_per_cycle: int = 15

@onready var sprite: Sprite2D = $Sprite2D
@onready var label: Label = $Label
@onready var prompt_label: Label = $PromptLabel
@onready var process_audio: AudioStreamPlayer2D = $ProcessAudio

var is_processing: bool = false

# Five recycling outputs as specified:
# 1. Battery (Special resource, cannot be crafted)
# 2. Material A
# 3. Material B
# 4. Material C
# 5. Material D
const OUTPUT_TABLE = [
	{"name": "battery", "weight": 15},     # Rare special battery
	{"name": "material_a", "weight": 25},  # Material A
	{"name": "material_b", "weight": 25},  # Material B
	{"name": "material_c", "weight": 20},  # Material C
	{"name": "material_d", "weight": 15}   # Material D
]

func _ready() -> void:
	add_to_group("Recyclers")
	body_entered.connect(_on_body_entered)
	body_exited.connect(_on_body_exited)
	
	if prompt_label:
		prompt_label.visible = false
		
	label.text = "RECYCLER P%d" % recycler_id
	label.modulate = Color(0.2, 0.85, 1.0) if recycler_id == 1 else Color(1.0, 0.6, 0.2)

func _on_body_entered(body: Node2D) -> void:
	if body is ScrapboundPlayer and body.is_multiplayer_authority():
		body.nearby_recycler = self
		if prompt_label:
			prompt_label.visible = true
			prompt_label.text = "[E] RECYCLE (15 Scrap)"

func _on_body_exited(body: Node2D) -> void:
	if body is ScrapboundPlayer and body.nearby_recycler == self:
		body.nearby_recycler = null
		if prompt_label:
			prompt_label.visible = false

@rpc("call_local", "reliable")
func play_recycle_effect_net(reward: String) -> void:
	if process_audio:
		process_audio.play()
		
	var tween = create_tween()
	tween.tween_property(sprite, "rotation", TAU * 2.0, 0.5).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	await tween.finished
	sprite.rotation = 0.0
	
	if prompt_label:
		prompt_label.visible = true
		prompt_label.text = "+1 " + reward.to_upper()
		prompt_label.modulate = Color.GREEN
		var t = get_tree().create_timer(1.2)
		t.timeout.connect(func():
			if is_instance_valid(prompt_label):
				prompt_label.modulate = Color.WHITE
				prompt_label.text = "[E] RECYCLE (15 Scrap)"
		)

func pick_weighted_output() -> String:
	var total_weight = 0
	for entry in OUTPUT_TABLE:
		total_weight += entry["weight"]
		
	var roll = randi_range(1, total_weight)
	var current = 0
	for entry in OUTPUT_TABLE:
		current += entry["weight"]
		if roll <= current:
			return entry["name"]
			
	return "material_a"
