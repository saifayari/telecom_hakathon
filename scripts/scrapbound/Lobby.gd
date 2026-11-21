extends Control

@onready var ip_edit: LineEdit = %IPEdit
@onready var port_edit: LineEdit = %PortEdit
@onready var btn_host: Button = %BtnHost
@onready var btn_join: Button = %BtnJoin
@onready var btn_start: Button = %BtnStart
@onready var btn_disconnect: Button = %BtnDisconnect
@onready var status_label: Label = %StatusLabel
@onready var player_list_label: Label = %PlayerListLabel

func _ready() -> void:
	NetworkManager.player_connected.connect(_on_network_player_connected)
	NetworkManager.player_disconnected.connect(_on_network_player_disconnected)
	NetworkManager.connection_succeeded.connect(_on_connection_succeeded)
	NetworkManager.connection_failed.connect(_on_connection_failed)
	NetworkManager.server_disconnected.connect(_on_server_disconnected)
	
	btn_host.pressed.connect(_on_host_pressed)
	btn_join.pressed.connect(_on_join_pressed)
	btn_start.pressed.connect(_on_start_pressed)
	btn_disconnect.pressed.connect(_on_disconnect_pressed)
	
	_reset_ui()

func _reset_ui() -> void:
	btn_host.disabled = false
	btn_join.disabled = false
	btn_start.visible = false
	btn_start.disabled = true
	btn_disconnect.visible = false
	ip_edit.editable = true
	port_edit.editable = true
	status_label.text = "Select HOST or JOIN to start online match."
	status_label.modulate = Color(0.8, 0.8, 0.8)
	player_list_label.text = "Players: 0 / 2"

func _on_host_pressed() -> void:
	var port = int(port_edit.text) if port_edit.text != "" else 7777
	var err = NetworkManager.host_game(port)
	if err == OK:
		btn_host.disabled = true
		btn_join.disabled = true
		btn_disconnect.visible = true
		btn_start.visible = true
		btn_start.disabled = true
		ip_edit.editable = false
		port_edit.editable = false
		status_label.text = "Hosting on port %d! Waiting for Player 2 to join..." % port
		status_label.modulate = Color(0.2, 0.85, 1.0)
		_update_player_list()
	else:
		status_label.text = "Failed to host: %s" % err
		status_label.modulate = Color(1.0, 0.3, 0.3)

func _on_join_pressed() -> void:
	var ip = ip_edit.text.strip_edges()
	if ip == "": ip = "127.0.0.1"
	var port = int(port_edit.text) if port_edit.text != "" else 7777
	
	var err = NetworkManager.join_game(ip, port)
	if err == OK:
		btn_host.disabled = true
		btn_join.disabled = true
		btn_disconnect.visible = true
		ip_edit.editable = false
		port_edit.editable = false
		status_label.text = "Connecting to %s:%d..." % [ip, port]
		status_label.modulate = Color(1.0, 0.7, 0.2)
	else:
		status_label.text = "Failed to initiate connection: %s" % err
		status_label.modulate = Color(1.0, 0.3, 0.3)

func _on_connection_succeeded() -> void:
	status_label.text = "Connected as Player 2! Waiting for Host to start match..."
	status_label.modulate = Color(0.2, 0.9, 0.4)
	_update_player_list()

func _on_connection_failed() -> void:
	status_label.text = "Connection failed! Check IP/Port and make sure Host is running."
	status_label.modulate = Color(1.0, 0.3, 0.3)
	_reset_ui()

func _on_server_disconnected() -> void:
	status_label.text = "Host disconnected or connection lost."
	status_label.modulate = Color(1.0, 0.3, 0.3)
	_reset_ui()

func _on_network_player_connected(_id: int) -> void:
	_update_player_list()
	if NetworkManager.is_host:
		var count = NetworkManager.players.size()
		if count >= 2:
			status_label.text = "Player 2 joined! Ready to launch match."
			status_label.modulate = Color(0.2, 0.9, 0.4)
			btn_start.disabled = false
		else:
			status_label.text = "Waiting for Player 2 to join..."
			btn_start.disabled = true

func _on_network_player_disconnected(_id: int) -> void:
	_update_player_list()
	if NetworkManager.is_host:
		status_label.text = "Player 2 disconnected. Waiting for connection..."
		status_label.modulate = Color(1.0, 0.6, 0.2)
		btn_start.disabled = true

func _update_player_list() -> void:
	var count = NetworkManager.players.size()
	player_list_label.text = "Connected Players: %d / 2\n" % count
	for pid in NetworkManager.players:
		var pinfo = NetworkManager.players[pid]
		player_list_label.text += "• %s (Peer %d)\n" % [pinfo["name"], pid]

func _on_start_pressed() -> void:
	if NetworkManager.is_host:
		NetworkManager.start_match()

func _on_disconnect_pressed() -> void:
	NetworkManager.disconnect_game()
	_reset_ui()
