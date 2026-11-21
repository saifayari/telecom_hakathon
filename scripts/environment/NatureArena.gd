extends Node2D
class_name NatureArena

signal day_night_toggled(is_night: bool)

@onready var tilemap_layer: TileMapLayer = $TileMapLayer
@onready var trees_container: Node2D = $TreesContainer

var is_night: bool = false

# Preload Day and Night tileset textures
var tex_tileset_day: Texture2D = preload("res://assets/sprites/environment/metalslug_tileset_day.png")
var tex_tileset_night: Texture2D = preload("res://assets/sprites/environment/metalslug_tileset_night.png")

# Preload Day and Night tree prop textures
var tex_oak_lg_day: Texture2D = preload("res://assets/sprites/environment/tree_oak_large_day.png")
var tex_oak_lg_night: Texture2D = preload("res://assets/sprites/environment/tree_oak_large_night.png")

var tex_oak_md_day: Texture2D = preload("res://assets/sprites/environment/tree_oak_med_day.png")
var tex_oak_md_night: Texture2D = preload("res://assets/sprites/environment/tree_oak_med_night.png")

var tex_pine_day: Texture2D = preload("res://assets/sprites/environment/tree_pine_day.png")
var tex_pine_night: Texture2D = preload("res://assets/sprites/environment/tree_pine_night.png")

var tex_dead_day: Texture2D = preload("res://assets/sprites/environment/tree_dead_day.png")
var tex_dead_night: Texture2D = preload("res://assets/sprites/environment/tree_dead_night.png")

var tex_stump_day: Texture2D = preload("res://assets/sprites/environment/tree_stump_day.png")
var tex_stump_night: Texture2D = preload("res://assets/sprites/environment/tree_stump_night.png")

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
	
	# Swap TileMapLayer Atlas texture for all ground tiles instantaneously
	if tilemap_layer and tilemap_layer.tile_set:
		var source = tilemap_layer.tile_set.get_source(0) as TileSetAtlasSource
		if source:
			source.texture = tex_tileset_night if is_night else tex_tileset_day
			tilemap_layer.notify_runtime_tile_data_update()
			tilemap_layer.queue_redraw()
	
	# Swap all perimeter trees and nature props
	if trees_container:
		for tree_node in trees_container.get_children():
			var spr: Sprite2D = tree_node.get_node_or_null("Sprite2D")
			if not spr:
				continue
			var t_type: String = tree_node.get_meta("tree_type", "")
			match t_type:
				"oak_lg":
					spr.texture = tex_oak_lg_night if is_night else tex_oak_lg_day
				"oak_md":
					spr.texture = tex_oak_md_night if is_night else tex_oak_md_day
				"pine":
					spr.texture = tex_pine_night if is_night else tex_pine_day
				"dead":
					spr.texture = tex_dead_night if is_night else tex_dead_day
				"stump":
					spr.texture = tex_stump_night if is_night else tex_stump_day
				_:
					spr.texture = tex_oak_md_night if is_night else tex_oak_md_day
					
	day_night_toggled.emit(is_night)
