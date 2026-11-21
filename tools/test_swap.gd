@tool
extends SceneTree

func _init():
    var tileset = load("res://scenes/environment/arena_tileset.tres") as TileSet
    var src = tileset.get_source(0) as TileSetAtlasSource
    print("Source 0 initial texture:", src.texture.resource_path)
    var night_tex = load("res://assets/sprites/environment/arena_tileset_night.png")
    src.texture = night_tex
    print("Source 0 new texture:", src.texture.resource_path)
    var day_tex = load("res://assets/sprites/environment/arena_tileset_day.png")
    src.texture = day_tex
    print("Reverted to day texture:", src.texture.resource_path)
    print("Texture swap works perfectly!")
    quit()
