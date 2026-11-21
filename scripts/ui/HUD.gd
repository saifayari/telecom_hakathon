extends Control
class_name GameHUD

@onready var phase_label: Label = %PhaseLabel
@onready var timer_label: Label = %TimerLabel
@onready var signal_bar: ProgressBar = %SignalBar
@onready var core_bar: ProgressBar = %CoreBar
@onready var scrap_val: Label = %ScrapVal
@onready var alloy_val: Label = %AlloyVal
@onready var battery_val: Label = %BatteryVal
@onready var core_val: Label = %CoreVal

@onready var dialogue_box: Control = %DialogueBox
@onready var speaker_label: Label = %SpeakerLabel
@onready var dialogue_text: Label = %DialogueText
@onready var portrait_rect: TextureRect = %PortraitRect

@onready var crafting_modal: CraftingModal = %CraftingModal
@onready var aegis_modal: AegisBarterModal = %AegisModal

var dialogue_hide_timer: float = 0.0

func _ready() -> void:
	add_to_group("HUD")
	EventBus.day_phase_started.connect(_on_day_started)
	EventBus.dusk_warning_started.connect(_on_dusk_warning)
	EventBus.night_phase_started.connect(_on_night_started)
	EventBus.tower_signal_changed.connect(_on_signal_changed)
	EventBus.core_health_changed.connect(_on_core_health_changed)
	EventBus.inventory_updated.connect(_update_inventory)
	EventBus.dialogue_requested.connect(show_dialogue)
	
	if dialogue_box:
		dialogue_box.visible = false
		
	_update_inventory()
	_update_phase_display()

func _process(delta: float) -> void:
	# Update Phase Timer
	var t = max(0.0, GameManager.phase_timer)
	if timer_label:
		timer_label.text = "%02d:%02d" % [int(t) / 60, int(t) % 60]
		
	# Dialogue box auto hide
	if dialogue_hide_timer > 0.0:
		dialogue_hide_timer -= delta
		if dialogue_hide_timer <= 0.0 and dialogue_box:
			dialogue_box.visible = false
			
	# Key input for Crafting (TAB)
	if Input.is_action_just_pressed("open_crafting"):
		if crafting_modal:
			if crafting_modal.visible:
				crafting_modal.close_modal()
			else:
				crafting_modal.open_modal()

func _update_phase_display() -> void:
	match GameManager.current_phase:
		GameManager.Phase.DAY:
			if phase_label:
				phase_label.text = "DAY %d - PURIFY SCRAP & PREPARE" % GameManager.current_day
				phase_label.modulate = Color(1.0, 0.85, 0.2)
		GameManager.Phase.DUSK:
			if phase_label:
				phase_label.text = "DUSK WARNING - FREQUENCY ATTENUATING!"
				phase_label.modulate = Color(1.0, 0.45, 0.1)
		GameManager.Phase.NIGHT:
			if phase_label:
				phase_label.text = "NIGHT %d - SURVIVE THE ASSAULT" % GameManager.current_day
				phase_label.modulate = Color(0.2, 0.85, 1.0)

func _on_day_started() -> void:
	_update_phase_display()

func _on_dusk_warning(_dur: float) -> void:
	_update_phase_display()
	show_dialogue("TOWER_OS", "WARNING: Solar irradiance dropped below threshold. Shifting primary reactor to core shields. Platform RF jamming field decaying!", preload("res://assets/sprites/ui/portrait_tower_os.png"))

func _on_night_started(wave: int) -> void:
	_update_phase_display()
	show_dialogue("SAMI", "Night %d... Here they come. Don't let them eat the unpurified scrap or we're dead!" % wave, preload("res://assets/sprites/ui/portrait_sami.png"))

func _on_signal_changed(percentage: float) -> void:
	if signal_bar:
		signal_bar.value = percentage * 100.0

func _on_core_health_changed(current: int, max_hp: int) -> void:
	if core_bar:
		core_bar.max_value = max_hp
		core_bar.value = current

func _update_inventory() -> void:
	if scrap_val:
		scrap_val.text = str(InventoryManager.raw_scrap)
	if alloy_val:
		alloy_val.text = str(InventoryManager.pure_alloys)
	if battery_val:
		battery_val.text = str(InventoryManager.lithium_batteries)
	if core_val:
		core_val.text = str(InventoryManager.charged_nano_cores)

func show_dialogue(speaker: String, text: String, portrait: Texture2D) -> void:
	if not dialogue_box:
		return
	dialogue_box.visible = true
	speaker_label.text = speaker
	dialogue_text.text = text
	if portrait and portrait_rect:
		portrait_rect.texture = portrait
	dialogue_hide_timer = 5.0

func open_aegis_barter() -> void:
	if aegis_modal:
		aegis_modal.open_terminal()
