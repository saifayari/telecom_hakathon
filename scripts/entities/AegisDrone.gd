extends Node2D
class_name AegisDrone

signal barter_requested()

@onready var anim_sprite: AnimatedSprite2D = $AnimatedSprite2D
@onready var interaction_area: Area2D = $InteractionArea
@onready var prompt_label: Label = $PromptLabel
@onready var scan_light: PointLight2D = $ScanLight

var player_in_range: bool = false
var base_y: float = 0.0

func _ready() -> void:
	add_to_group("AEGIS")
	base_y = position.y
	if prompt_label:
		prompt_label.visible = false
		prompt_label.text = "[F] TRADE WITH PROTOCOL AEGIS"
		
	if anim_sprite:
		anim_sprite.play("idle")
		
	if interaction_area:
		interaction_area.body_entered.connect(_on_body_entered)
		interaction_area.body_exited.connect(_on_body_exited)
		
	EventBus.day_phase_started.connect(_on_day_started)
	EventBus.night_phase_started.connect(_on_night_started)

func _process(_delta: float) -> void:
	# Gentle hover bobbing
	position.y = base_y + sin(Time.get_ticks_msec() * 0.003) * 6.0
	
	if player_in_range and Input.is_action_just_pressed("repair_build"): # Key F
		trigger_barter()

func _on_body_entered(body: Node2D) -> void:
	if body.is_in_group("Player"):
		player_in_range = true
		if prompt_label:
			prompt_label.visible = true
		if anim_sprite:
			anim_sprite.play("scan")

func _on_body_exited(body: Node2D) -> void:
	if body.is_in_group("Player"):
		player_in_range = false
		if prompt_label:
			prompt_label.visible = false
		if anim_sprite:
			anim_sprite.play("idle")

func trigger_barter() -> void:
	barter_requested.emit()
	var hud = get_tree().get_first_node_in_group("HUD")
	if hud and hud.has_method("open_aegis_barter"):
		hud.open_aegis_barter()

func _on_day_started() -> void:
	visible = true
	if anim_sprite:
		anim_sprite.play("idle")
	EventBus.dialogue_requested.emit(
		"PROTOCOL AEGIS",
		"Protocol AEGIS v4.2 active. Contractor Sami identified. Provide Pure Alloys to purchase Lithium Batteries.",
		preload("res://assets/sprites/ui/portrait_aegis.png")
	)

func _on_night_started(_wave: int) -> void:
	# Enters protective high-altitude holding pattern during night combat
	if anim_sprite:
		anim_sprite.play("idle")
