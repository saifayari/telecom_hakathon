extends Node

signal player_connected(peer_id: int)
signal player_disconnected(peer_id: int)
signal connection_succeeded()
signal connection_failed()
signal server_disconnected()
signal game_started()
signal host_discovered(ip: String, port: int)

const DEFAULT_PORT: int = 7777
const DISCOVERY_PORT: int = 7788
const MAX_PLAYERS: int = 2

var peer: ENetMultiplayerPeer = null
var is_host: bool = false
var local_peer_id: int = 1
var players: Dictionary = {} # peer_id -> {"name": String, "player_id": int}

# LAN Discovery via UDP broadcast
var udp_broadcaster: PacketPeerUDP = null
var udp_listener: PacketPeerUDP = null
var broadcast_timer: float = 0.0
var broadcast_port_to_announce: int = DEFAULT_PORT

func _ready() -> void:
	multiplayer.peer_connected.connect(_on_peer_connected)
	multiplayer.peer_disconnected.connect(_on_peer_disconnected)
	multiplayer.connected_to_server.connect(_on_connected_to_server)
	multiplayer.connection_failed.connect(_on_connection_failed)
	multiplayer.server_disconnected.connect(_on_server_disconnected)

func _process(delta: float) -> void:
	# Host: Broadcast presence to LAN every 1 second
	if udp_broadcaster and is_host:
		broadcast_timer -= delta
		if broadcast_timer <= 0.0:
			broadcast_timer = 1.0
			var msg = ("SCRAPBOUND_HOST:%d" % broadcast_port_to_announce).to_utf8_buffer()
			udp_broadcaster.put_packet(msg)
			
	# Client: Listen for host announcements
	if udp_listener:
		while udp_listener.get_available_packet_count() > 0:
			var pkt = udp_listener.get_packet().get_string_from_utf8()
			var sender_ip = udp_listener.get_packet_ip()
			if pkt.begins_with("SCRAPBOUND_HOST:"):
				var parts = pkt.split(":")
				var p = int(parts[1]) if parts.size() > 1 else DEFAULT_PORT
				host_discovered.emit(sender_ip, p)

func start_lan_broadcasting(port: int) -> void:
	stop_lan_discovery()
	broadcast_port_to_announce = port
	udp_broadcaster = PacketPeerUDP.new()
	udp_broadcaster.set_broadcast_enabled(true)
	udp_broadcaster.set_dest_address("255.255.255.255", DISCOVERY_PORT)
	broadcast_timer = 0.0
	print("[NETWORK] LAN Broadcaster started on port %d" % DISCOVERY_PORT)

func start_lan_listener() -> void:
	stop_lan_discovery()
	udp_listener = PacketPeerUDP.new()
	var err = udp_listener.bind(DISCOVERY_PORT, "*")
	if err != OK:
		print("[NETWORK] Could not bind LAN discovery listener: %s" % err)
		udp_listener = null
	else:
		print("[NETWORK] LAN Listener active on port %d" % DISCOVERY_PORT)

func stop_lan_discovery() -> void:
	if udp_broadcaster:
		udp_broadcaster.close()
		udp_broadcaster = null
	if udp_listener:
		udp_listener.close()
		udp_listener = null

static func get_lan_ip() -> String:
	var addresses = IP.get_local_addresses()
	var fallback_ip = ""
	for ip in addresses:
		if not ":" in ip: # Only IPv4
			if ip.begins_with("127.") or ip.begins_with("169.254."):
				continue
			# Priority 1: standard local network (excluding virbr0 / 192.168.122.x)
			if ip.begins_with("192.168."):
				if not ip.begins_with("192.168.122."):
					return ip
				elif fallback_ip == "":
					fallback_ip = ip
			# Priority 2: 10.x.x.x
			elif ip.begins_with("10."):
				return ip
			# Priority 3: 172.x.x.x (used only if no other IP is available)
			elif ip.begins_with("172.") and fallback_ip == "":
				fallback_ip = ip
	return fallback_ip if fallback_ip != "" else "127.0.0.1"

func host_game(port: int = DEFAULT_PORT) -> Error:
	stop_lan_discovery()
	peer = ENetMultiplayerPeer.new()
	var error = peer.create_server(port, MAX_PLAYERS)
	if error != OK:
		print("[NETWORK] Failed to create server on port %d: %s" % [port, error])
		return error
		
	multiplayer.multiplayer_peer = peer
	is_host = true
	local_peer_id = 1
	
	players.clear()
	players[1] = {"name": "Player 1 (Host)", "player_id": 1}
	
	print("[NETWORK] Host server running on port %d" % port)
	start_lan_broadcasting(port)
	return OK

func join_game(address: String = "127.0.0.1", port: int = DEFAULT_PORT) -> Error:
	stop_lan_discovery()
	peer = ENetMultiplayerPeer.new()
	var error = peer.create_client(address, port)
	if error != OK:
		print("[NETWORK] Failed to create client to %s:%d: %s" % [address, port, error])
		return error
		
	multiplayer.multiplayer_peer = peer
	is_host = false
	
	print("[NETWORK] Connecting to %s:%d..." % [address, port])
	return OK

func disconnect_game() -> void:
	stop_lan_discovery()
	if peer:
		peer.close()
		peer = null
	multiplayer.multiplayer_peer = null
	is_host = false
	players.clear()
	print("[NETWORK] Disconnected from session.")

func _on_peer_connected(id: int) -> void:
	print("[NETWORK] Peer connected: %d" % id)
	if is_host:
		# Second player is Player 2
		players[id] = {"name": "Player 2 (Client)", "player_id": 2}
		# Broadcast updated player list to client
		_sync_players.rpc(players)
		
	player_connected.emit(id)

func _on_peer_disconnected(id: int) -> void:
	print("[NETWORK] Peer disconnected: %d" % id)
	players.erase(id)
	player_disconnected.emit(id)

func _on_connected_to_server() -> void:
	local_peer_id = multiplayer.get_unique_id()
	print("[NETWORK] Connected to host! My Peer ID is: %d" % local_peer_id)
	stop_lan_discovery()
	connection_succeeded.emit()

func _on_connection_failed() -> void:
	print("[NETWORK] Connection to host failed.")
	disconnect_game()
	connection_failed.emit()

func _on_server_disconnected() -> void:
	print("[NETWORK] Host disconnected.")
	disconnect_game()
	server_disconnected.emit()

@rpc("any_peer", "call_local", "reliable")
func _sync_players(updated_players: Dictionary) -> void:
	players = updated_players

func start_match() -> void:
	if not is_host:
		return
	print("[NETWORK] Host starting match across all peers!")
	stop_lan_discovery()
	_change_scene_to_game.rpc()

@rpc("any_peer", "call_local", "reliable")
func _change_scene_to_game() -> void:
	stop_lan_discovery()
	game_started.emit()
	get_tree().change_scene_to_file("res://scenes/scrapbound/ScrapboundMain.tscn")

func get_my_player_id() -> int:
	var my_id = multiplayer.get_unique_id()
	if my_id in players:
		return players[my_id]["player_id"]
	return 1 if is_host else 2
