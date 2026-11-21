extends StaticBody2D
class_name TelecomTowerCore

@onready var tower_sprite: Sprite2D = $TowerSprite
@onready var frequency_ring: Sprite2D = $FrequencyRing
@onready var beacon_light: PointLight2D = $BeaconLight
@onready var sfx_alarm: AudioStreamPlayer2D = $AudioAlarm

var tex_tower_day = preload("res://assets/sprites/environment/telecom_tower_day.png")
var tex_tower_night = preload("res://assets/sprites/environment/telecom_tower_night.png")

var is_night: bool = false

func _ready() -> void:
	add_to_group("CoreTower")
	EventBus.day_phase_started.connect(_on_day_started)
	EventBus.dusk_warning_started.connect(_on_dusk_warning)
	EventBus.night_phase_started.connect(_on_night_started)
	EventBus.tower_signal_changed.connect(_on_signal_changed)
	
	_apply_mode(false)

func _process(delta: float) -> void:
	# Frequency shield cyan pulse
	if frequency_ring:
		var pulse = sin(Time.get_ticks_msec() * 0.005) * 0.15 + 0.85
		var sig = GameManager.jamming_signal_strength
		frequency_ring.scale = Vector2(pulse, pulse) * (0.8 + sig * 0.4)
		frequency_ring.modulate.a = 0.3 + sig * 0.5

func _apply_mode(night: bool) -> void:
	is_night = night
	if tower_sprite:
		tower_sprite.texture = tex_tower_night if is_night else tex_tower_day
	if beacon_light:
		beacon_light.enabled = is_night

func _on_day_started() -> void:
	_apply_mode(false)

func _on_dusk_warning(_duration: float) -> void:
	if sfx_alarm:
		sfx_alarm.play()

func _on_night_started(_wave: int) -> void:
	_apply_mode(true)

func _on_signal_changed(percentage: float) -> void:
	if frequency_ring:
		if percentage < 0.3:
			frequency_ring.modulate = Color(1.0, 0.4, 0.2, 0.4) # Warning red/orange
		else:
			frequency_ring.modulate = Color(0.1, 0.8, 1.0, 0.7) # Healthy cyan
