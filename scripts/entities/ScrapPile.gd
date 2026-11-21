extends Area2D
class_name ScrapPile

enum State { INERT, GLOWING, SPORES, ERUPTING, PURIFIED }

var current_state: State = State.INERT
var purify_progress: float = 0.0
const PURIFY_DURATION: float = 0.8 # 0.8s as per GDD

var mutation_timer: float = 20.0
const MUTATION_DURATION: float = 20.0

@onready var sprite: Sprite2D = $Sprite2D
@onready var progress_bar: ProgressBar = $ProgressBar
@onready var prompt_label: Label = $PromptLabel
@onready var sfx_pickup: AudioStreamPlayer2D = $AudioPickup
@onready var sfx_purify: AudioStreamPlayer2D = $AudioPurify

var tex_inert = preload("res://assets/sprites/environment/scrap_pile/scrap_pile_inert.png")
var tex_glow = preload("res://assets/sprites/environment/scrap_pile/scrap_pile_glow.png")
var tex_spores = preload("res://assets/sprites/environment/scrap_pile/scrap_pile_spores.png")
var tex_erupting = preload("res://assets/sprites/environment/scrap_pile/scrap_pile_erupting.png")
var shockwave_scene = preload("res://scenes/entities/Shockwave.tscn")
var enemy_scene = preload("res://scenes/entities/EnemyAmalgam.tscn")

var is_being_purified: bool = false
var player_is_nearby: bool = false

func _ready() -> void:
	add_to_group("ScrapPiles")
	sprite.texture = tex_inert
	if progress_bar:
		progress_bar.visible = false
		progress_bar.max_value = PURIFY_DURATION
		progress_bar.value = 0.0
	if prompt_label:
		prompt_label.visible = false
	
	area_entered.connect(_on_area_entered)
	body_entered.connect(_on_body_entered)

func set_player_nearby(nearby: bool) -> void:
	player_is_nearby = nearby
	if prompt_label and not is_being_purified:
		prompt_label.visible = player_is_nearby

func _process(delta: float) -> void:
	# Handling player RF Welder purification
	if is_being_purified:
		purify_progress += delta
		if progress_bar:
			progress_bar.visible = true
			progress_bar.value = purify_progress
		if prompt_label:
			prompt_label.visible = false
		
		# Welder visual jitter/sparkle
		sprite.modulate = Color(0.6, 0.9, 1.0).lerp(Color.WHITE, sin(Time.get_ticks_msec() * 0.02) * 0.5 + 0.5)
		
		if purify_progress >= PURIFY_DURATION:
			complete_purification()
			return
	else:
		if purify_progress > 0.0:
			purify_progress = max(0.0, purify_progress - delta * 2.0)
			if progress_bar:
				progress_bar.value = purify_progress
				if purify_progress <= 0.0:
					progress_bar.visible = false
					if player_is_nearby and prompt_label:
						prompt_label.visible = true
		sprite.modulate = Color.WHITE
		
	# Handling Dusk & Night Mutation
	var signal_strength = GameManager.jamming_signal_strength
	if signal_strength < 0.6: # Tower frequency drops at dusk/night!
		mutation_timer -= delta
		var ratio = mutation_timer / MUTATION_DURATION
		
		if ratio > 0.66:
			set_state(State.GLOWING)
		elif ratio > 0.33:
			set_state(State.SPORES)
		elif ratio > 0.0:
			set_state(State.ERUPTING)
		else:
			trigger_monster_reformation()
	else:
		# Protected by daytime tower jamming umbrella!
		set_state(State.INERT)
		mutation_timer = MUTATION_DURATION

func set_state(new_state: State) -> void:
	if current_state == new_state:
		return
	current_state = new_state
	match current_state:
		State.INERT:
			sprite.texture = tex_inert
		State.GLOWING:
			sprite.texture = tex_glow
		State.SPORES:
			sprite.texture = tex_spores
		State.ERUPTING:
			sprite.texture = tex_erupting

func start_purifying() -> void:
	is_being_purified = true

func cancel_purifying() -> void:
	is_being_purified = false

func complete_purification() -> void:
	is_being_purified = false
	current_state = State.PURIFIED
	
	# Spawn Resonant Shockwave (150 radius, 150 damage, 3s stun)
	var sw = shockwave_scene.instantiate()
	sw.global_position = global_position
	get_parent().add_child(sw)
	
	# Reward Player
	InventoryManager.add_pure_alloys(1)
	InventoryManager.add_raw_scrap(randi_range(15, 25))
	
	EventBus.scrap_purified.emit(global_position)
	EventBus.shockwave_triggered.emit(global_position, 150.0, 150)
	
	_spawn_floating_text("+1 PURE ALLOY  +20 SCRAP", Color(0.2, 0.9, 1.0))
	
	if sfx_purify:
		sfx_purify.reparent(get_parent())
		sfx_purify.play()
		sfx_purify.finished.connect(sfx_purify.queue_free)
		
	queue_free()

func trigger_monster_reformation() -> void:
	# Unpurified scrap reassembles into an enemy at dusk/night!
	var enemy = enemy_scene.instantiate()
	enemy.global_position = global_position
	get_parent().add_child(enemy)
	
	EventBus.monster_reformed.emit(global_position)
	_spawn_floating_text("NANO AWAKENING!", Color(1.0, 0.2, 0.2))
	queue_free()

func _on_body_entered(body: Node2D) -> void:
	# If a monster passes near unpurified scrap at night, it devours it!
	if GameManager.is_night_phase() and body.is_in_group("Enemies") and body.has_method("devour_scrap"):
		body.devour_scrap(self)
		EventBus.scrap_devoured.emit(body)
		_spawn_floating_text("DEVOUR MUTATION!", Color(1.0, 0.4, 0.1))
		queue_free()

func _on_area_entered(_area: Area2D) -> void:
	pass

func _spawn_floating_text(msg: String, color: Color) -> void:
	var label = Label.new()
	label.text = msg
	label.modulate = color
	label.global_position = global_position + Vector2(-60, -30)
	label.z_index = 100
	get_parent().add_child(label)
	
	var tween = label.create_tween().set_parallel(true)
	tween.tween_property(label, "position:y", label.position.y - 25.0, 1.2)
	tween.tween_property(label, "modulate:a", 0.0, 1.2)
	tween.finished.connect(label.queue_free)
