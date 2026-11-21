extends Node

# Game Manager for FACTORY RESET
enum Phase { DAY, DUSK, NIGHT }

var current_phase: Phase = Phase.DAY
var current_day: int = 1
var max_days: int = 5

var phase_timer: float = 60.0
const DAY_DURATION: float = 60.0
const DUSK_DURATION: float = 10.0
const NIGHT_DURATION: float = 90.0

var core_health: int = 1000
var max_core_health: int = 1000
var jamming_signal_strength: float = 1.0 # 100% in day, drops at dusk

func _ready() -> void:
	start_day_phase()

func _process(delta: float) -> void:
	phase_timer -= delta
	
	if current_phase == Phase.DAY:
		jamming_signal_strength = 1.0
		if phase_timer <= 0:
			start_dusk_phase()
	elif current_phase == Phase.DUSK:
		# Gradually attenuate jamming signal
		jamming_signal_strength = max(0.2, phase_timer / DUSK_DURATION)
		EventBus.tower_signal_changed.emit(jamming_signal_strength)
		if phase_timer <= 0:
			EventBus.dusk_frequency_dropped.emit()
			start_night_phase()
	elif current_phase == Phase.NIGHT:
		jamming_signal_strength = 0.25
		if phase_timer <= 0:
			current_day += 1
			start_day_phase()

func start_day_phase() -> void:
	current_phase = Phase.DAY
	phase_timer = DAY_DURATION
	jamming_signal_strength = 1.0
	EventBus.day_phase_started.emit()
	EventBus.tower_signal_changed.emit(jamming_signal_strength)

func start_dusk_phase() -> void:
	current_phase = Phase.DUSK
	phase_timer = DUSK_DURATION
	EventBus.dusk_warning_started.emit(DUSK_DURATION)

func start_night_phase() -> void:
	current_phase = Phase.NIGHT
	phase_timer = NIGHT_DURATION
	EventBus.night_phase_started.emit(current_day)

func is_night_phase() -> bool:
	return current_phase == Phase.NIGHT

func damage_core(amount: int) -> void:
	core_health = max(0, core_health - amount)
	EventBus.core_health_changed.emit(core_health, max_core_health)
