extends Control

@onready var ip_edit: LineEdit = %IPEdit
@onready var port_edit: LineEdit = %PortEdit
@onready var btn_host: Button = %BtnHost
@onready var btn_join: Button = %BtnJoin
@onready var btn_start: Button = %BtnStart
@onready var btn_disconnect: Button = %BtnDisconnect
@onready var status_label: Label = %StatusLabel
@onready var player_list_label: Label = %PlayerListLabel

var local_lan_ip: String = "127.0.0.1"

func _ready() -> void:
	NetworkManager.player_connected.connect(_on_network_player_connected)
	NetworkManager.player_disconnected.connect(_on_network_player_disconnected)
	NetworkManager.connection_succeeded.connect(_on_connection_succeeded)
	NetworkManager.connection_failed.connect(_on_connection_failed)
	NetworkManager.server_disconnected.connect(_on_server_disconnected)
	NetworkManager.host_discovered.connect(_on_host_discovered)
	
	btn_host.pressed.connect(_on_host_pressed)
	btn_join.pressed.connect(_on_join_pressed)
	btn_start.pressed.connect(_on_start_pressed)
	btn_disconnect.pressed.connect(_on_disconnect_pressed)
	
	local_lan_ip = NetworkManager.get_lan_ip()
	_reset_ui()
	
	var all_args = OS.get_cmdline_args() + OS.get_cmdline_user_args()
	for a in all_args:
		if a == "--host" or a == "host":
			DisplayServer.window_set_title("SCRAPBOUND - PLAYER 1 [HOST]")
			DisplayServer.window_set_size(Vector2i(630, 520))
			DisplayServer.window_set_position(Vector2i(20, 60))
			get_tree().create_timer(0.4).timeout.connect(_on_host_pressed)
			break
		elif a == "--join" or a == "join":
			DisplayServer.window_set_title("SCRAPBOUND - PLAYER 2 [CLIENT]")
			DisplayServer.window_set_size(Vector2i(630, 520))
			DisplayServer.window_set_position(Vector2i(665, 60))
			get_tree().create_timer(0.9).timeout.connect(_on_join_pressed)
			break

func _reset_ui() -> void:
	btn_host.disabled = false
	btn_join.disabled = false
	btn_start.visible = false
	btn_start.disabled = true
	btn_disconnect.visible = false
	ip_edit.editable = true
	port_edit.editable = true
	
	local_lan_ip = NetworkManager.get_lan_ip()
	status_label.text = "Your LAN IP: %s\nSelect HOST (P1) or JOIN (P2) to begin." % local_lan_ip
	status_label.modulate = Color(0.85, 0.9, 1.0)
	player_list_label.text = "Connected Players: 0 / 2"
	
	# Start listening for any host on the LAN
	NetworkManager.start_lan_listener()

func _on_host_discovered(discovered_ip: String, discovered_port: int) -> void:
	if not NetworkManager.is_host and not multiplayer.multiplayer_peer:
		ip_edit.text = discovered_ip
		port_edit.text = str(discovered_port)
		status_label.text = "✨ LAN Host detected at %s:%d!\nClick JOIN GAME (P2) to connect." % [discovered_ip, discovered_port]
		status_label.modulate = Color(0.25, 0.95, 0.45)

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
		status_label.text = "Hosting on Port %d | LAN IP: %s\nTell Player 2 to join %s (or Auto-Discovery)." % [port, local_lan_ip, local_lan_ip]
		status_label.modulate = Color(0.2, 0.85, 1.0)
		_update_player_list()
	else:
		status_label.text = "Failed to host: %s\n(Check if port %d is already in use)" % [err, port]
		status_label.modulate = Color(1.0, 0.3, 0.3)

func _on_join_pressed() -> void:
	var raw_ip = ip_edit.text.strip_edges()
	var port = int(port_edit.text) if port_edit.text != "" else 7777
	
	# Handle pasted IP:PORT (e.g. 192.168.1.50:7777)
	if ":" in raw_ip and not "[" in raw_ip:
		var parts = raw_ip.split(":")
		raw_ip = parts[0].strip_edges()
		if parts.size() > 1 and parts[1].strip_edges().is_valid_int():
			port = int(parts[1].strip_edges())
			port_edit.text = str(port)
			
	if raw_ip == "":
		raw_ip = "127.0.0.1"
		
	ip_edit.text = raw_ip
	
	var err = NetworkManager.join_game(raw_ip, port)
	if err == OK:
		btn_host.disabled = true
		btn_join.disabled = true
		btn_disconnect.visible = true
		ip_edit.editable = false
		port_edit.editable = false
		if raw_ip == "127.0.0.1":
			status_label.text = "Connecting to 127.0.0.1 (Localhost)...\n(For LAN, enter Player 1's LAN IP)"
		else:
			status_label.text = "Connecting to %s:%d...\n(Make sure Host has clicked HOST GAME)" % [raw_ip, port]
		status_label.modulate = Color(1.0, 0.75, 0.2)
	else:
		status_label.text = "Failed to initiate connection: %s" % err
		status_label.modulate = Color(1.0, 0.3, 0.3)

func _on_connection_succeeded() -> void:
	status_label.text = "Connected as Player 2! Waiting for Host to start match..."
	status_label.modulate = Color(0.2, 0.9, 0.4)
	_update_player_list()

func _on_connection_failed() -> void:
	status_label.text = "Connection failed!\nCheck Host IP & Port, and ensure Firewall allows UDP 7777."
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
