extends Control
class_name AegisBarterModal

@onready var title_label: Label = %TitleLabel
@onready var log_label: Label = %LogLabel
@onready var btn_buy_battery: Button = %BtnBuyBattery
@onready var btn_buy_sentry: Button = %BtnBuySentry
@onready var btn_buy_emp: Button = %BtnBuyEmp
@onready var btn_repair_core: Button = %BtnRepairCore
@onready var btn_close: Button = %BtnClose
@onready var audio_buy: AudioStreamPlayer = $AudioBuy

func _ready() -> void:
	visible = false
	btn_buy_battery.pressed.connect(_on_buy_battery)
	btn_buy_sentry.pressed.connect(_on_buy_sentry)
	btn_buy_emp.pressed.connect(_on_buy_emp)
	btn_repair_core.pressed.connect(_on_repair_core)
	btn_close.pressed.connect(close_terminal)
	
	EventBus.inventory_updated.connect(_update_ui)

func open_terminal() -> void:
	visible = true
	_update_ui()
	if log_label:
		log_label.text = "SYNTHOBIOME PROTOCOL AEGIS - v4.2 ONLINE\nCONTRACTOR: SAMI | STATUS: ACTIVE\n'Bring Pure Alloys to exchange for Lithium Batteries and advanced grid components.'"

func close_terminal() -> void:
	visible = false

func _update_ui() -> void:
	if not visible:
		return
	btn_buy_battery.disabled = InventoryManager.pure_alloys < 1
	btn_buy_sentry.disabled = InventoryManager.pure_alloys < 3 or InventoryManager.raw_scrap < 40
	btn_buy_emp.disabled = InventoryManager.pure_alloys < 4 or InventoryManager.lithium_batteries < 1
	btn_repair_core.disabled = InventoryManager.pure_alloys < 1 or InventoryManager.raw_scrap < 20

func _on_buy_battery() -> void:
	if InventoryManager.pure_alloys >= 1:
		InventoryManager.pure_alloys -= 1
		InventoryManager.add_lithium_batteries(1)
		_play_buy("TRADE COMPLETE: +1 High-Density Lithium Battery acquired.")

func _on_buy_sentry() -> void:
	if InventoryManager.pure_alloys >= 3 and InventoryManager.raw_scrap >= 40:
		InventoryManager.pure_alloys -= 3
		InventoryManager.raw_scrap -= 40
		EventBus.inventory_updated.emit()
		_spawn_turret_near_player("ScrapSentry")
		_play_buy("DEFENSE AUTHORIZED: Scrap Sentry deployed near platform.")

func _on_buy_emp() -> void:
	if InventoryManager.pure_alloys >= 4 and InventoryManager.lithium_batteries >= 1:
		InventoryManager.pure_alloys -= 4
		InventoryManager.lithium_batteries -= 1
		EventBus.inventory_updated.emit()
		_spawn_turret_near_player("EMPPulsar")
		_play_buy("HIGH-VOLTAGE AUTHORIZED: EMP Pulsar deployed.")

func _on_repair_core() -> void:
	if InventoryManager.pure_alloys >= 1 and InventoryManager.raw_scrap >= 20:
		InventoryManager.pure_alloys -= 1
		InventoryManager.raw_scrap -= 20
		GameManager.core_health = min(GameManager.max_core_health, GameManager.core_health + 250)
		EventBus.core_health_changed.emit(GameManager.core_health, GameManager.max_core_health)
		InventoryManager.EventBus.inventory_updated.emit()
		_play_buy("GRID RESTORED: Telecom Tower Core repaired (+250 HP).")

func _spawn_turret_near_player(type: String) -> void:
	var player = get_tree().get_first_node_in_group("Player")
	if player:
		var pos = player.global_position + Vector2(randf_range(-40, 40), randf_range(-40, 40))
		EventBus.turret_placed.emit(type, pos)

func _play_buy(msg: String) -> void:
	if audio_buy:
		audio_buy.play()
	if log_label:
		log_label.text = msg
	_update_ui()
