extends Node2D
class_name Arena

signal day_night_toggled(is_night: bool)

@onready var tilemap_layer: TileMapLayer = $TileMapLayer
@onready var sky_sprite: Sprite2D = $Background/SkySprite
@onready var central_tower_bay: Sprite2D = $CentralTowerBay
@onready var scrap_depot: Sprite2D = $ScrapDepot
@onready var aegis_pad: Sprite2D = $AegisPad
@onready var turret_pad_nw: Sprite2D = $TurretPadNW
@onready var turret_pad_ne: Sprite2D = $TurretPadNE
@onready var turret_pad_sw: Sprite2D = $TurretPadSW
@onready var turret_pad_se: Sprite2D = $TurretPadSE

var is_night: bool = false

# Preload Day and Night textures
var tex_tileset_day: Texture2D = preload("res://assets/sprites/environment/arena_tileset_day.png")
var tex_tileset_night: Texture2D = preload("res://assets/sprites/environment/arena_tileset_night.png")

var tex_sky_day: Texture2D = preload("res://assets/sprites/environment/bg_day_sky.png")
var tex_sky_night: Texture2D = preload("res://assets/sprites/environment/bg_night_sky.png")

var tex_tower_day: Texture2D = preload("res://assets/sprites/environment/central_tower_bay_day.png")
var tex_tower_night: Texture2D = preload("res://assets/sprites/environment/central_tower_bay_night.png")

var tex_turret_day: Texture2D = preload("res://assets/sprites/environment/turret_mount_pad_day.png")
var tex_turret_night: Texture2D = preload("res://assets/sprites/environment/turret_mount_pad_night.png")

var tex_aegis_day: Texture2D = preload("res://assets/sprites/environment/aegis_landing_pad_day.png")
var tex_aegis_night: Texture2D = preload("res://assets/sprites/environment/aegis_landing_pad_night.png")

var tex_scrap_day: Texture2D = preload("res://assets/sprites/environment/scrap_depot_zone_day.png")
var tex_scrap_night: Texture2D = preload("res://assets/sprites/environment/scrap_depot_zone_night.png")

func _ready() -> void:
	apply_night_mode(false)

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_N or event.keycode == KEY_TAB:
			toggle_day_night()

func toggle_day_night() -> void:
	apply_night_mode(not is_night)

func apply_night_mode(night: bool) -> void:
	is_night = night
	
	# Swap TileMapLayer texture in Atlas Source 0
	if tilemap_layer and tilemap_layer.tile_set:
		var source = tilemap_layer.tile_set.get_source(0) as TileSetAtlasSource
		if source:
			source.texture = tex_tileset_night if is_night else tex_tileset_day
			tilemap_layer.notify_runtime_tile_data_update()
			tilemap_layer.queue_redraw()
	
	# Swap Landmark Props & Background
	if sky_sprite:
		sky_sprite.texture = tex_sky_night if is_night else tex_sky_day
	if central_tower_bay:
		central_tower_bay.texture = tex_tower_night if is_night else tex_tower_day
	if scrap_depot:
		scrap_depot.texture = tex_scrap_night if is_night else tex_scrap_day
	if aegis_pad:
		aegis_pad.texture = tex_aegis_night if is_night else tex_aegis_day
		
	var turret_tex = tex_turret_night if is_night else tex_turret_day
	if turret_pad_nw: turret_pad_nw.texture = turret_tex
	if turret_pad_ne: turret_pad_ne.texture = turret_tex
	if turret_pad_sw: turret_pad_sw.texture = turret_tex
	if turret_pad_se: turret_pad_se.texture = turret_tex
	
	day_night_toggled.emit(is_night)
