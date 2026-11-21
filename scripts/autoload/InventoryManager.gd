extends Node

# Inventory & Crafting Manager for FACTORY RESET
var raw_scrap: int = 50
var pure_alloys: int = 0
var lithium_batteries: int = 1
var charged_nano_cores: int = 0

# Intermediate Crafted Modules
var induction_coils: int = 0
var composite_armor: int = 0
var nano_rf_capacitors: int = 0
var scrubber_filters: int = 0
var purified_silicon: int = 0
var neutralized_acid: int = 0

func add_raw_scrap(amount: int) -> void:
	raw_scrap += amount
	EventBus.inventory_updated.emit()

func add_pure_alloys(amount: int) -> void:
	pure_alloys += amount
	EventBus.inventory_updated.emit()

func add_lithium_batteries(amount: int) -> void:
	lithium_batteries += amount
	EventBus.inventory_updated.emit()

func add_charged_nano_cores(amount: int) -> void:
	charged_nano_cores += amount
	EventBus.inventory_updated.emit()

# Check affordability for recipes
func can_craft_sentry() -> bool:
	return raw_scrap >= 50 and pure_alloys >= 1

func craft_sentry() -> bool:
	if can_craft_sentry():
		raw_scrap -= 50
		pure_alloys -= 1
		EventBus.inventory_updated.emit()
		return true
	return false

func can_craft_emp_pulsar() -> bool:
	return raw_scrap >= 80 and lithium_batteries >= 1 and pure_alloys >= 3

func craft_emp_pulsar() -> bool:
	if can_craft_emp_pulsar():
		raw_scrap -= 80
		lithium_batteries -= 1
		pure_alloys -= 3
		EventBus.inventory_updated.emit()
		return true
	return false

func can_craft_resonance_turret() -> bool:
	return raw_scrap >= 120 and pure_alloys >= 5

func craft_resonance_turret() -> bool:
	if can_craft_resonance_turret():
		raw_scrap -= 120
		pure_alloys -= 5
		EventBus.inventory_updated.emit()
		return true
	return false

# AEGIS Barter: Selling crafted modules for 3x - 5x Lithium batteries
func barter_module_to_aegis(module_name: String) -> bool:
	match module_name:
		"induction_coil":
			if induction_coils >= 1:
				induction_coils -= 1
				add_lithium_batteries(1)
				add_raw_scrap(40)
				return true
		"composite_armor":
			if composite_armor >= 1:
				composite_armor -= 1
				add_lithium_batteries(1)
				return true
		"nano_rf_capacitor":
			if nano_rf_capacitors >= 1:
				nano_rf_capacitors -= 1
				add_lithium_batteries(2)
				return true
		"scrubber_filter":
			if scrubber_filters >= 1:
				scrubber_filters -= 1
				add_lithium_batteries(1)
				add_pure_alloys(3)
				return true
	return false
