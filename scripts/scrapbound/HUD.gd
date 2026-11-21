extends Control
class_name ScrapboundHUD

signal rematch_requested()

@onready var timer_label: Label = %TimerLabel

@onready var my_title_label: Label = %MyTitleLabel
@onready var my_score_label: Label = %MyScoreLabel
@onready var my_health_bar: ProgressBar = %MyHealthBar
@onready var my_health_val: Label = %MyHealthVal
@onready var my_tower_bar: ProgressBar = %MyTowerBar
@onready var my_tower_val: Label = %MyTowerVal
@onready var my_weapon_label: Label = %MyWeaponLabel
@onready var my_scrap_label: Label = %MyScrapLabel
@onready var my_mats_label: Label = %MyMatsLabel

@onready var opp_title_label: Label = %OppTitleLabel
@onready var opp_score_label: Label = %OppScoreLabel
@onready var opp_tower_bar: ProgressBar = %OppTowerBar
@onready var opp_tower_val: Label = %OppTowerVal

@onready var results_panel: Panel = %ResultsPanel
@onready var winner_label: Label = %WinnerLabel
@onready var results_detail: Label = %ResultsDetail
@onready var btn_rematch: Button = %BtnRematch

var local_player_id: int = 1

func _ready() -> void:
	if results_panel:
		results_panel.visible = false
	if btn_rematch:
		btn_rematch.pressed.connect(_on_rematch_pressed)

func set_local_player(p_id: int) -> void:
	local_player_id = p_id
	if p_id == 1:
		my_title_label.text = "YOU (PLAYER 1 - BLUE)"
		my_title_label.modulate = Color(0.2, 0.85, 1.0)
		opp_title_label.text = "OPPONENT (PLAYER 2 - ORANGE)"
		opp_title_label.modulate = Color(1.0, 0.6, 0.2)
	else:
		my_title_label.text = "YOU (PLAYER 2 - ORANGE)"
		my_title_label.modulate = Color(1.0, 0.6, 0.2)
		opp_title_label.text = "OPPONENT (PLAYER 1 - BLUE)"
		opp_title_label.modulate = Color(0.2, 0.85, 1.0)

func update_timer(time_left: float) -> void:
	var t = max(0.0, time_left)
	if timer_label:
		timer_label.text = "%02d:%02d" % [int(t) / 60, int(t) % 60]
		timer_label.modulate = Color(1.0, 0.25, 0.25) if t <= 10.0 else Color.WHITE

func update_player_ui(
	p1_hp: int, p1_score: int, p1_kills: int, p1_tower: int, p1_wpn: String, p1_inv: Dictionary,
	p2_hp: int, p2_score: int, p2_kills: int, p2_tower: int, p2_wpn: String, p2_inv: Dictionary
) -> void:
	var my_hp = p1_hp if local_player_id == 1 else p2_hp
	var my_score = p1_score if local_player_id == 1 else p2_score
	var my_kills = p1_kills if local_player_id == 1 else p2_kills
	var my_tower = p1_tower if local_player_id == 1 else p2_tower
	var my_wpn = p1_wpn if local_player_id == 1 else p2_wpn
	var my_inv = p1_inv if local_player_id == 1 else p2_inv
	
	var opp_score = p2_score if local_player_id == 1 else p1_score
	var opp_tower = p2_tower if local_player_id == 1 else p1_tower
	
	# Update MY UI
	if my_score_label:
		my_score_label.text = "SCORE: %d (Kills: %d)" % [my_score, my_kills]
	if my_health_bar:
		my_health_bar.value = my_hp
	if my_health_val:
		my_health_val.text = "%d HP" % my_hp
	if my_tower_bar:
		my_tower_bar.value = my_tower
	if my_tower_val:
		my_tower_val.text = "%d / 1000" % my_tower
	if my_weapon_label:
		my_weapon_label.text = "WEAPON: " + my_wpn
	if my_scrap_label:
		my_scrap_label.text = "SCRAP: %d  |  BATTERY: %d" % [my_inv.get("scrap", 0), my_inv.get("battery", 0)]
	if my_mats_label:
		my_mats_label.text = "CRAFT: [A:%d B:%d C:%d D:%d]   BUILD: [Wood:%d Plas:%d Iron:%d]" % [
			my_inv.get("material_a", 0), my_inv.get("material_b", 0),
			my_inv.get("material_c", 0), my_inv.get("material_d", 0),
			my_inv.get("wood", 0), my_inv.get("plastic", 0), my_inv.get("iron", 0)
		]
		
	# Update OPPONENT UI
	if opp_score_label:
		opp_score_label.text = "SCORE: %d" % opp_score
	if opp_tower_bar:
		opp_tower_bar.value = opp_tower
	if opp_tower_val:
		opp_tower_val.text = "%d / 1000" % opp_tower

func show_results(p1_kills: int, p1_score: int, p1_tower_hp: int, p2_kills: int, p2_score: int, p2_tower_hp: int) -> void:
	if not results_panel:
		return
		
	var p1_total = p1_score + p1_tower_hp * 2
	var p2_total = p2_score + p2_tower_hp * 2
	
	results_panel.visible = true
	
	var is_p1 = (local_player_id == 1)
	var my_win = false
	var opp_win = false
	
	if p1_tower_hp <= 0 and p2_tower_hp > 0:
		if is_p1: opp_win = true
		else: my_win = true
	elif p2_tower_hp <= 0 and p1_tower_hp > 0:
		if is_p1: my_win = true
		else: opp_win = true
	elif p1_total > p2_total:
		if is_p1: my_win = true
		else: opp_win = true
	elif p2_total > p1_total:
		if is_p1: opp_win = true
		else: my_win = true
		
	if my_win:
		winner_label.text = "VICTORY! YOU WIN! 🏆"
		winner_label.modulate = Color(0.2, 0.9, 0.4)
	elif opp_win:
		winner_label.text = "DEFEAT! OPPONENT WON! 💀"
		winner_label.modulate = Color(1.0, 0.3, 0.3)
	else:
		winner_label.text = "DRAW MATCH! 🤝"
		winner_label.modulate = Color(1.0, 1.0, 1.0)
		
	if results_detail:
		results_detail.text = (
			"=== FINAL MATCH REPORT ===\n\n" +
			"PLAYER 1 (Blue):\n" +
			"  Kills: %d (%d pts) | Tower HP: %d (+%d bonus) | TOTAL: %d\n\n" % [p1_kills, p1_score, p1_tower_hp, p1_tower_hp * 2, p1_total] +
			"PLAYER 2 (Orange):\n" +
			"  Kills: %d (%d pts) | Tower HP: %d (+%d bonus) | TOTAL: %d" % [p2_kills, p2_score, p2_tower_hp, p2_tower_hp * 2, p2_total]
		)

func _on_rematch_pressed() -> void:
	rematch_requested.emit()
