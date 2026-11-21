extends Node

# Central EventBus for FACTORY RESET
signal day_phase_started()
signal dusk_warning_started(duration: float)
signal dusk_frequency_dropped()
signal night_phase_started(wave_number: int)

signal scrap_purified(global_pos: Vector2)
signal shockwave_triggered(global_pos: Vector2, radius: float, damage: int)
signal monster_reformed(global_pos: Vector2)
signal scrap_devoured(enemy: Node2D)
signal enemy_died(enemy: Node2D, global_pos: Vector2)

signal inventory_updated()
signal core_health_changed(current: int, max_hp: int)
signal player_health_changed(current: int, max_hp: int)
signal tower_signal_changed(percentage: float)
signal dialogue_requested(speaker: String, text: String, portrait: Texture2D)
signal turret_placed(turret_type: String, global_pos: Vector2)
