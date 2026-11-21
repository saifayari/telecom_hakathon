extends Node

signal player_connected(peer_id: int)
signal player_disconnected(peer_id: int)
signal connection_succeeded()
signal connection_failed()
signal server_disconnected()
signal game_started()

const DEFAULT_PORT: int = 7777
const MAX_PLAYERS: int = 2

var peer: ENetMultiplayerPeer = null
var is_host: bool = false
var local_peer_id: int = 1
var players: Dictionary = {} # peer_id -> {"name": String, "player_id": int}

func _ready() -> void:
	multiplayer.peer_connected.connect(_on_peer_connected)
	multiplayer.peer_disconnected.connect(_on_peer_disconnected)
	multiplayer.connected_to_server.connect(_on_connected_to_server)
	multiplayer.connection_failed.connect(_on_connection_failed)
	multiplayer.server_disconnected.connect(_on_server_disconnected)

func host_game(port: int = DEFAULT_PORT) -> Error:
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
	return OK

func join_game(address: String = "127.0.0.1", port: int = DEFAULT_PORT) -> Error:
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
	connection_succeeded.emit()

func _on_connection_failed() -> void:
	print("[NETWORK] Connection to host failed.")
	disconnect_game()
	connection_failed.emit()

func _on_server_disconnected() -> void:
	print("[NETWORK] Host disconnected.")
	disconnect_game()
	server_disconnected.emit()

@rpc("authority", "call_local", "reliable")
func _sync_players(updated_players: Dictionary) -> void:
	players = updated_players

func start_match() -> void:
	if not is_host:
		return
	print("[NETWORK] Host starting match across all peers!")
	_change_scene_to_game.rpc()

@rpc("authority", "call_local", "reliable")
func _change_scene_to_game() -> void:
	game_started.emit()
	get_tree().change_scene_to_file("res://scenes/scrapbound/ScrapboundMain.tscn")

func get_my_player_id() -> int:
	var my_id = multiplayer.get_unique_id()
	if my_id in players:
		return players[my_id]["player_id"]
	return 1 if is_host else 2
