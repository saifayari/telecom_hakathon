extends CharacterBody2D
class_name EnemyAmalgam

@export var monster_tier: int = 1

const TIER_DATA = {
	1: {
		"tier": 1,
		"name": "Scrap Scout",
		"label": "Lv.1 Scout",
		"max_health": 100,
		"attack_damage": 12,
		"speed": 85.0,
		"attack_cooldown": 1.0,
		"attack_range": 32.0,
		"sprite_scale": Vector2(0.315, 0.315), # Exact match to Sami's visual height (30.2px)
		"collision_radius": 7.0,
		"collision_height": 22.0,
		"tint": Color(1.0, 1.0, 1.0),
		"scrap_drop": 15,
		"bar_color": Color(0.2, 0.85, 0.3),
		"bar_offset_y": -26.0,
		"label_offset_y": -40.0
	},
	2: {
		"tier": 2,
		"name": "Scrap Amalgam",
		"label": "Lv.2 Amalgam",
		"max_health": 240,
		"attack_damage": 22,
		"speed": 70.0,
		"attack_cooldown": 1.2,
		"attack_range": 38.0,
		"sprite_scale": Vector2(0.38, 0.38), # Logically scaled: ~20% larger than Sami (36.5px)
		"collision_radius": 9.0,
		"collision_height": 26.0,
		"tint": Color(1.0, 0.92, 0.78), # Bronze / hardened plating
		"scrap_drop": 35,
		"bar_color": Color(1.0, 0.75, 0.2),
		"bar_offset_y": -32.0,
		"label_offset_y": -46.0
	},
	3: {
		"tier": 3,
		"name": "Apex Behemoth",
		"label": "Lv.3 Behemoth",
		"max_health": 480,
		"attack_damage": 38,
		"speed": 55.0,
		"attack_cooldown": 1.5,
		"attack_range": 44.0,
		"sprite_scale": Vector2(0.45, 0.45), # Logically normalized: ~45% larger than Sami (43px), NOT giant
		"collision_radius": 11.0,
		"collision_height": 30.0,
		"tint": Color(1.0, 0.78, 0.78), # Corrupted crimson sheen
		"scrap_drop": 75,
		"bar_color": Color(0.95, 0.25, 0.25),
		"bar_offset_y": -38.0,
		"label_offset_y": -52.0
	}
}

var max_health: int = 100
var health: int = 100
var speed: float = 85.0
var attack_damage: int = 12
var attack_cooldown: float = 1.0
var attack_range: float = 32.0
var scrap_drop_amount: int = 15

var is_stunned: bool = false
var stun_timer: float = 0.0
var attack_timer: float = 0.0
var is_attacking: bool = false

var target_position: Vector2 = Vector2(1024, 768) # Default: Telecom Tower Core
var current_target_node: Node2D = null

@onready var anim_sprite: AnimatedSprite2D = $AnimatedSprite2D
@onready var collision_shape: CollisionShape2D = $CollisionShape2D
@onready var tier_label: Label = $TierLabel
@onready var health_bar: ProgressBar = $HealthBar
@onready var sfx_hit: AudioStreamPlayer2D = $AudioHit
@onready var sfx_attack: AudioStreamPlayer2D = $AudioAttack

var scrap_pile_scene = preload("res://scenes/entities/ScrapPile.tscn")

func _ready() -> void:
	add_to_group("Enemies")
	if anim_sprite:
		anim_sprite.animation_finished.connect(_on_animation_finished)
	
	set_tier(monster_tier)

func set_tier(tier: int) -> void:
	monster_tier = clamp(tier, 1, 3)
	var data = TIER_DATA[monster_tier]
	
	max_health = data["max_health"]
	health = max_health
	speed = data["speed"]
	attack_damage = data["attack_damage"]
	attack_cooldown = data["attack_cooldown"]
	attack_range = data["attack_range"]
	scrap_drop_amount = data["scrap_drop"]
	
	if anim_sprite:
		anim_sprite.scale = data["sprite_scale"]
		anim_sprite.self_modulate = data["tint"]
		if anim_sprite.animation != "attack":
			anim_sprite.play("walk")
			
	if collision_shape:
		var new_shape = CapsuleShape2D.new()
		new_shape.radius = data["collision_radius"]
		new_shape.height = data["collision_height"]
		collision_shape.shape = new_shape
		
	if tier_label:
		tier_label.text = data["label"]
		tier_label.position.y = data["label_offset_y"]
		tier_label.modulate = data["bar_color"]
		
	if health_bar:
		health_bar.max_value = max_health
		health_bar.value = health
		health_bar.position.y = data["bar_offset_y"]
		health_bar.modulate = data["bar_color"]

func _physics_process(delta: float) -> void:
	# 1. Handle EM Stun
	if is_stunned:
		stun_timer -= delta
		velocity = Vector2.ZERO
		move_and_slide()
		anim_sprite.modulate = Color(0.4, 0.8, 1.0).lerp(Color.WHITE, sin(Time.get_ticks_msec() * 0.03) * 0.5 + 0.5)
		if stun_timer <= 0.0:
			is_stunned = false
			anim_sprite.modulate = Color.WHITE
			anim_sprite.play("walk")
		return
		
	# 2. While actively in attack swing, do not slide or move
	if is_attacking:
		velocity = Vector2.ZERO
		move_and_slide()
		return
		
	attack_timer -= delta
	
	# 3. Determine target: Scrap Pile, Sami, or Core
	_update_target()
	
	var dir = (target_position - global_position)
	var dist = dir.length()
	
	# Hysteresis: only stop if within attack_range; only walk if > attack_range
	if dist > attack_range:
		velocity = dir.normalized() * speed
		if anim_sprite.animation != "walk" and anim_sprite.animation != "hit":
			anim_sprite.play("walk")
		anim_sprite.flip_h = velocity.x < 0
	else:
		velocity = Vector2.ZERO
		# Face target even when standing still
		anim_sprite.flip_h = dir.x < 0
		if attack_timer <= 0.0:
			_start_attack()
		elif anim_sprite.animation != "idle" and anim_sprite.animation != "attack" and anim_sprite.animation != "hit":
			anim_sprite.play("idle")
			
	move_and_slide()

func _update_target() -> void:
	# Priority 1: At night, devour unpurified scrap piles to mutate!
	if GameManager.is_night_phase():
		var piles = get_tree().get_nodes_in_group("ScrapPiles")
		var nearest_pile: Node2D = null
		var min_pile_dist = 260.0
		for p in piles:
			if is_instance_valid(p):
				var d = global_position.distance_to(p.global_position)
				if d < min_pile_dist:
					min_pile_dist = d
					nearest_pile = p
		if nearest_pile:
			target_position = nearest_pile.global_position
			current_target_node = nearest_pile
			return

	# Priority 2: Hunt Sami if within aggro radius
	var player = get_tree().get_first_node_in_group("Player")
	if player and is_instance_valid(player):
		var p_dist = global_position.distance_to(player.global_position)
		if p_dist < 260.0:
			target_position = player.global_position
			current_target_node = player
			return
			
	# Priority 3: Default target Telecom Tower Core
	target_position = Vector2(1024, 768)
	current_target_node = null

func _start_attack() -> void:
	is_attacking = true
	velocity = Vector2.ZERO
	
	# Face the target
	if target_position.x < global_position.x:
		anim_sprite.flip_h = true
	else:
		anim_sprite.flip_h = false
		
	anim_sprite.play("attack")
	
	# Damage lands midway through the strike for clean, responsive combat feedback
	var strike_timer = get_tree().create_timer(0.24)
	strike_timer.timeout.connect(_deliver_attack_damage)

func _deliver_attack_damage() -> void:
	if not is_instance_valid(self) or is_stunned:
		return
		
	if sfx_attack:
		sfx_attack.pitch_scale = randf_range(0.9, 1.1)
		sfx_attack.play()
		
	# Check target validity and distance at moment of strike (allows dodging!)
	if current_target_node and is_instance_valid(current_target_node):
		var d = global_position.distance_to(current_target_node.global_position)
		# Generous grace distance to avoid false whiffs while still allowing genuine dodges
		if d <= attack_range + 24.0:
			if current_target_node.has_method("take_damage"):
				current_target_node.take_damage(attack_damage, global_position)
	else:
		# Attack core directly
		var core_dist = global_position.distance_to(Vector2(1024, 768))
		if core_dist <= 75.0:
			GameManager.damage_core(attack_damage)

func _on_animation_finished() -> void:
	if anim_sprite.animation == "attack":
		is_attacking = false
		attack_timer = attack_cooldown
		
		# Return smoothly to idle or walk depending on current distance
		if current_target_node and is_instance_valid(current_target_node):
			var d = global_position.distance_to(current_target_node.global_position)
			if d <= attack_range:
				anim_sprite.play("idle")
			else:
				anim_sprite.play("walk")
		else:
			anim_sprite.play("walk")
			
	elif anim_sprite.animation == "hit":
		if not is_stunned and health > 0:
			if is_attacking:
				is_attacking = false
			anim_sprite.play("walk")

func take_damage(amount: int, _from_pos: Vector2 = Vector2.ZERO) -> void:
	health -= amount
	if health_bar:
		health_bar.value = health
	
	if sfx_hit:
		sfx_hit.pitch_scale = randf_range(0.95, 1.05)
		sfx_hit.play()
		
	# Brief hit flash without breaking attack logic
	if not is_attacking:
		anim_sprite.play("hit")
	else:
		anim_sprite.modulate = Color(1.8, 0.4, 0.4)
		var t = get_tree().create_timer(0.1)
		t.timeout.connect(func(): if is_instance_valid(self): anim_sprite.modulate = Color.WHITE)
	
	if health <= 0:
		die()

func apply_em_stun(duration: float) -> void:
	is_stunned = true
	is_attacking = false
	stun_timer = max(stun_timer, duration)

func devour_scrap(_scrap_pile: Node2D) -> void:
	# Lore mechanic: Devouring unpurified scrap at night mutates the enemy to the next tier!
	if monster_tier < 3:
		set_tier(monster_tier + 1)
	else:
		health = max_health
		speed *= 1.1
		attack_damage += 5
		if health_bar:
			health_bar.value = health

func die() -> void:
	EventBus.enemy_died.emit(self, global_position)
	
	# Drop Inert Scrap Pile so the recycle cycle continues!
	var pile = scrap_pile_scene.instantiate()
	pile.global_position = global_position
	if pile.has_method("set_scrap_amount"):
		pile.set_scrap_amount(scrap_drop_amount)
	get_parent().call_deferred("add_child", pile)
	
	queue_free()
