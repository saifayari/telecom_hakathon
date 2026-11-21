extends CharacterBody2D
class_name ScrapboundMonster

signal monster_killed(monster: Node2D, killer_player_id: int)

@export var max_health: int = 80
@export var speed: float = 72.0
@export var attack_damage: int = 15
@export var attack_cooldown: float = 1.0
@export var attack_range: float = 34.0

var health: int = 80
var is_attacking: bool = false
var attack_timer: float = 0.0

var target_node: Node2D = null
var target_position: Vector2 = Vector2.ZERO
var last_hit_by_player: int = 1

var remote_pos: Vector2 = Vector2.ZERO

@onready var anim_sprite: AnimatedSprite2D = $AnimatedSprite2D
@onready var health_bar: ProgressBar = $HealthBar
@onready var audio_attack: AudioStreamPlayer2D = $AudioAttack
@onready var audio_hit: AudioStreamPlayer2D = $AudioHit

func _ready() -> void:
	add_to_group("Enemies")
	health = max_health
	remote_pos = global_position
	
	if health_bar:
		health_bar.max_value = max_health
		health_bar.value = health
		
	if anim_sprite:
		anim_sprite.play("walk")
		anim_sprite.animation_finished.connect(_on_animation_finished)

func _physics_process(delta: float) -> void:
	if multiplayer.is_server():
		_physics_process_server(delta)
	else:
		_physics_process_client(delta)

func _physics_process_server(delta: float) -> void:
	if is_attacking:
		velocity = Vector2.ZERO
		move_and_slide()
		return
		
	attack_timer -= delta
	_update_ai_target()
	
	var dir = (target_position - global_position)
	var dist = dir.length()
	
	if dist > attack_range:
		velocity = dir.normalized() * speed
		if anim_sprite and anim_sprite.animation != "walk":
			anim_sprite.play("walk")
		if anim_sprite:
			anim_sprite.flip_h = velocity.x < 0
	else:
		velocity = Vector2.ZERO
		if anim_sprite:
			anim_sprite.flip_h = dir.x < 0
		if attack_timer <= 0.0:
			_start_attack_server()
		elif anim_sprite and anim_sprite.animation != "idle" and anim_sprite.animation != "attack":
			anim_sprite.play("idle")
			
	move_and_slide()
	
	# Broadcast position and animation to clients
	var anim_name = anim_sprite.animation if anim_sprite else "walk"
	var flip = anim_sprite.flip_h if anim_sprite else false
	sync_monster_state.rpc(global_position, anim_name, flip)

func _physics_process_client(delta: float) -> void:
	if global_position.distance_to(remote_pos) > 1.0:
		global_position = global_position.lerp(remote_pos, delta * 15.0)

@rpc("any_peer", "unreliable_ordered")
func sync_monster_state(pos: Vector2, anim: String, flip: bool) -> void:
	if multiplayer.is_server():
		return
	remote_pos = pos
	if anim_sprite:
		if anim_sprite.animation != anim:
			anim_sprite.play(anim)
		anim_sprite.flip_h = flip

func _update_ai_target() -> void:
	var candidates: Array = []
	var towers = get_tree().get_nodes_in_group("Towers")
	for t in towers:
		if is_instance_valid(t) and t.health > 0:
			candidates.append(t)
			
	var players = get_tree().get_nodes_in_group("Players")
	for p in players:
		if is_instance_valid(p) and not p.is_dead:
			candidates.append(p)
			
	var barriers = get_tree().get_nodes_in_group("Barriers")
	for b in barriers:
		if is_instance_valid(b) and b.health > 0:
			if global_position.distance_to(b.global_position) < 48.0:
				candidates.append(b)
				
	var nearest: Node2D = null
	var min_dist = 99999.0
	for c in candidates:
		var d = global_position.distance_to(c.global_position)
		if d < min_dist:
			min_dist = d
			nearest = c
			
	if nearest:
		target_node = nearest
		target_position = nearest.global_position
	else:
		target_position = Vector2(540, 300)

func _start_attack_server() -> void:
	is_attacking = true
	velocity = Vector2.ZERO
	play_attack_net.rpc()
	
	var strike_timer = get_tree().create_timer(0.22)
	strike_timer.timeout.connect(_deliver_attack_server)

@rpc("any_peer", "call_local", "reliable")
func play_attack_net() -> void:
	if anim_sprite:
		anim_sprite.play("attack")
	if audio_attack:
		audio_attack.pitch_scale = randf_range(0.9, 1.1)
		audio_attack.play()

func _deliver_attack_server() -> void:
	if not is_instance_valid(self):
		return
	if target_node and is_instance_valid(target_node):
		var d = global_position.distance_to(target_node.global_position)
		if d <= attack_range + 24.0:
			if target_node is ScrapboundPlayer:
				target_node.take_damage_server(attack_damage)
			elif target_node is ScrapboundTower:
				target_node.take_damage_server(attack_damage)
			elif target_node is ScrapboundBarrier:
				target_node.take_damage_server(attack_damage)

func _on_animation_finished() -> void:
	if anim_sprite and anim_sprite.animation == "attack":
		is_attacking = false
		attack_timer = attack_cooldown
		anim_sprite.play("walk")

func take_damage(amount: int, player_id: int = 1) -> void:
	if not multiplayer.is_server():
		return
	last_hit_by_player = player_id
	health -= amount
	sync_monster_hit_net.rpc(health)
	
	if health <= 0:
		die_server()

@rpc("any_peer", "call_local", "reliable")
func sync_monster_hit_net(new_hp: int) -> void:
	health = new_hp
	if health_bar:
		health_bar.value = health
	if audio_hit:
		audio_hit.pitch_scale = randf_range(0.95, 1.05)
		audio_hit.play()
	if anim_sprite:
		anim_sprite.modulate = Color(2.0, 0.4, 0.4)
		var t = get_tree().create_timer(0.1)
		t.timeout.connect(func(): if is_instance_valid(self) and anim_sprite: anim_sprite.modulate = Color.WHITE)

func die_server() -> void:
	monster_killed.emit(self, last_hit_by_player)
	var main = get_parent() as ScrapboundMain
	if main:
		main.on_monster_destroyed_server(self, last_hit_by_player, global_position)
	remove_monster_net.rpc()

@rpc("any_peer", "call_local", "reliable")
func remove_monster_net() -> void:
	queue_free()
