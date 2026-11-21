extends Control
class_name CraftingModal

@onready var btn_craft_sentry: Button = %BtnCraftSentry
@onready var btn_craft_barricade: Button = %BtnCraftBarricade
@onready var btn_craft_repair: Button = %BtnCraftRepair
@onready var btn_craft_coil: Button = %BtnCraftCoil
@onready var btn_close: Button = %BtnClose
@onready var log_label: Label = %LogLabel
@onready var audio_click: AudioStreamPlayer = $AudioClick

func _ready() -> void:
	visible = false
	btn_craft_sentry.pressed.connect(_on_craft_sentry)
	btn_craft_barricade.pressed.connect(_on_craft_barricade)
	btn_craft_repair.pressed.connect(_on_craft_repair)
	btn_craft_coil.pressed.connect(_on_craft_coil)
	btn_close.pressed.connect(close_modal)
	
	EventBus.inventory_updated.connect(_update_ui)

func open_modal() -> void:
	visible = true
	_update_ui()
	if log_label:
		log_label.text = "FIELD WORKBENCH - SELECT SCHEMATIC TO FABRICATE"

func close_modal() -> void:
	visible = false

func _update_ui() -> void:
	if not visible:
		return
	btn_craft_sentry.disabled = not InventoryManager.can_craft_sentry()
	btn_craft_barricade.disabled = InventoryManager.raw_scrap < 30
	btn_craft_repair.disabled = InventoryManager.raw_scrap < 15
	btn_craft_coil.disabled = InventoryManager.raw_scrap < 40

func _on_craft_sentry() -> void:
	if InventoryManager.craft_sentry():
		var player = get_tree().get_first_node_in_group("Player")
		if player:
			var pos = player.global_position + Vector2(30, 0)
			EventBus.turret_placed.emit("ScrapSentry", pos)
		_log_craft("FABRICATED: Scrap Sentry Turret deployed!")

func _on_craft_barricade() -> void:
	if InventoryManager.raw_scrap >= 30:
		InventoryManager.raw_scrap -= 30
		EventBus.inventory_updated.emit()
		var player = get_tree().get_first_node_in_group("Player")
		if player:
			var pos = player.global_position + Vector2(25, 25)
			EventBus.turret_placed.emit("Barricade", pos)
		_log_craft("FABRICATED: Spiked Scrap Barricade placed!")

func _on_craft_repair() -> void:
	if InventoryManager.raw_scrap >= 15:
		InventoryManager.raw_scrap -= 15
		EventBus.inventory_updated.emit()
		var player = get_tree().get_first_node_in_group("Player")
		if player and player.has_method("take_damage"):
			player.health = min(player.max_health, player.health + 40)
		_log_craft("FIELD AID: Farady Hazmat suit repaired (+40 HP).")

func _on_craft_coil() -> void:
	if InventoryManager.raw_scrap >= 40:
		InventoryManager.raw_scrap -= 40
		InventoryManager.induction_coils += 1
		EventBus.inventory_updated.emit()
		_log_craft("FABRICATED: Induction Coil prepared for AEGIS Barter.")

func _log_craft(msg: String) -> void:
	if audio_click:
		audio_click.play()
	if log_label:
		log_label.text = msg
	_update_ui()
