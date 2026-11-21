extends Node2D

@onready var arena: Node2D = $Arena
@onready var player: CharacterBody2D = $SamiPlayer
@onready var camera: Camera2D = $Camera2D
@onready var day_music: AudioStreamPlayer = $Audio/DayMusic
@onready var night_music: AudioStreamPlayer = $Audio/NightMusic
@onready var dusk_siren: AudioStreamPlayer = $Audio/DuskSiren

var scrap_pile_scene = preload("res://scenes/entities/ScrapPile.tscn")
var enemy_scene = preload("res://scenes/entities/EnemyAmalgam.tscn")
var sentry_scene = preload("res://scenes/entities/ScrapSentry.tscn")

var spawn_timer: float = 0.0
var spawn_interval: float = 5.0
var enemies_to_spawn: int = 0

func _ready() -> void:
	EventBus.day_phase_started.connect(_on_day_started)
	EventBus.dusk_warning_started.connect(_on_dusk_warning)
	EventBus.night_phase_started.connect(_on_night_started)
	EventBus.turret_placed.connect(_on_turret_placed)
	
	if day_music:
		day_music.play()
		
	# Spawn initial day 1 scrap piles around the compound
	_spawn_initial_scrap_piles()
	
	# Spawn initial scout enemies so the player immediately sees monster assets & combat!
	_spawn_initial_scout_enemies()
	
	print("[GAME LEVEL READY] Scrap piles spawned: ", get_tree().get_nodes_in_group("ScrapPiles").size())
	print("[GAME LEVEL READY] Scout enemies spawned: ", get_tree().get_nodes_in_group("Enemies").size())
	
	# Initial welcome dialogue from Tower OS
	get_tree().create_timer(0.8).timeout.connect(func():
		EventBus.dialogue_requested.emit(
			"TOWER_OS",
			"TOWER_OS v2.9 online. Solar day active. Purify the inert scrap piles before dusk attenuates our frequency umbrella! Press [N] to toggle Night Wave.",
			preload("res://assets/sprites/ui/portrait_tower_os.png")
		)
	)

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_N:
			# Toggle Day / Night Phase immediately for quick testing & combat
			if GameManager.is_night_phase():
				GameManager.start_day_phase()
			else:
				GameManager.start_night_phase()

func _process(delta: float) -> void:
	if player and camera:
		camera.position = player.position
		
	# Night wave enemy spawning
	if GameManager.is_night_phase():
		spawn_timer -= delta
		if spawn_timer <= 0.0 and enemies_to_spawn > 0:
			spawn_timer = spawn_interval
			enemies_to_spawn -= 1
			_spawn_perimeter_enemy()

func _spawn_initial_scrap_piles() -> void:
	var positions = [
		Vector2(950, 720),
		Vector2(1100, 740),
		Vector2(970, 840),
		Vector2(1080, 850),
		Vector2(880, 760),
		Vector2(1160, 780)
	]
	for pos in positions:
		var pile = scrap_pile_scene.instantiate()
		pile.global_position = pos
		add_child(pile)

func _spawn_initial_scout_enemies() -> void:
	# Showcase all 3 normalized tiers on initial spawn
	# Lv.1 Scout: Same size as Sami (30px), fast scout
	var scout1 = enemy_scene.instantiate()
	scout1.global_position = Vector2(850, 820)
	scout1.monster_tier = 1
	add_child(scout1)
	
	# Lv.2 Amalgam: Scaled up logically (~1.2x), bronze tone, tougher
	var scout2 = enemy_scene.instantiate()
	scout2.global_position = Vector2(1250, 820)
	scout2.monster_tier = 2
	add_child(scout2)
	
	# Lv.3 Behemoth: Logically normalized boss (~1.45x), crimson tone, heavy brute
	var scout3 = enemy_scene.instantiate()
	scout3.global_position = Vector2(1480, 750)
	scout3.monster_tier = 3
	add_child(scout3)

func _spawn_perimeter_enemy() -> void:
	# Spawn from outer perimeter
	var angle = randf() * TAU
	var spawn_dist = 680.0
	var spawn_pos = Vector2(1024, 768) + Vector2(cos(angle), sin(angle)) * spawn_dist
	
	spawn_pos.x = clamp(spawn_pos.x, 60.0, 1980.0)
	spawn_pos.y = clamp(spawn_pos.y, 60.0, 1470.0)
	
	var enemy = enemy_scene.instantiate()
	enemy.global_position = spawn_pos
	
	# Dynamic tier weighting by night day
	var day = GameManager.current_day
	var r = randf()
	var tier = 1
	if day <= 1:
		tier = 1 if r < 0.80 else 2
	elif day == 2:
		if r < 0.50:
			tier = 1
		elif r < 0.85:
			tier = 2
		else:
			tier = 3
	else:
		if r < 0.25:
			tier = 1
		elif r < 0.65:
			tier = 2
		else:
			tier = 3
			
	enemy.monster_tier = tier
	add_child(enemy)

func _on_day_started() -> void:
	if arena and arena.has_method("apply_night_mode"):
		arena.apply_night_mode(false)
	if night_music: night_music.stop()
	if day_music and not day_music.playing: day_music.play()
	
	var current_piles = get_tree().get_nodes_in_group("ScrapPiles").size()
	if current_piles < 4:
		_spawn_initial_scrap_piles()

func _on_dusk_warning(_dur: float) -> void:
	if dusk_siren:
		dusk_siren.play()

func _on_night_started(wave: int) -> void:
	if arena and arena.has_method("apply_night_mode"):
		arena.apply_night_mode(true)
	if day_music: day_music.stop()
	if night_music: night_music.play()
	
	# Wave scaling
	enemies_to_spawn = 4 + wave * 3
	spawn_interval = max(2.5, 5.0 - wave * 0.4)
	spawn_timer = 1.5

func _on_turret_placed(type: String, pos: Vector2) -> void:
	if type == "ScrapSentry":
		var sentry = sentry_scene.instantiate()
		sentry.global_position = pos
		add_child(sentry)
