@tool
extends SceneTree

func _init():
    print("Regenerating res://scenes/main/GameLevel.tscn for Nature Arena...")
    var root = Node2D.new()
    root.name = "GameLevel"
    root.set_script(load("res://scripts/main/GameLevel.gd"))
    
    # 1. Nature Arena Instance
    var arena_scene = load("res://scenes/environment/NatureArena.tscn")
    var arena = arena_scene.instantiate()
    arena.name = "Arena"
    root.add_child(arena)
    arena.owner = root
    
    # 2. Player (Sami) - spawned near central clearing
    var sami_scene = load("res://scenes/entities/SamiPlayer.tscn")
    var player = sami_scene.instantiate()
    player.name = "SamiPlayer"
    player.position = Vector2(768, 480)
    root.add_child(player)
    player.owner = root
    
    # 3. Camera2D - 1536 x 1152 boundaries
    var cam = Camera2D.new()
    cam.name = "Camera2D"
    cam.position = Vector2(768, 480)
    cam.limit_left = 0
    cam.limit_top = 0
    cam.limit_right = 1536
    cam.limit_bottom = 1152
    cam.position_smoothing_enabled = true
    cam.position_smoothing_speed = 8.0
    root.add_child(cam)
    cam.owner = root
    
    # 4. CanvasLayer HUD
    var cl = CanvasLayer.new()
    cl.name = "CanvasLayer"
    root.add_child(cl)
    cl.owner = root
    
    var hud_ctrl = Control.new()
    hud_ctrl.name = "ControlsHUD"
    hud_ctrl.set_anchors_preset(Control.PRESET_FULL_RECT)
    cl.add_child(hud_ctrl)
    hud_ctrl.owner = root
    
    var panel = PanelContainer.new()
    panel.name = "Panel"
    panel.position = Vector2(16, 16)
    hud_ctrl.add_child(panel)
    panel.owner = root
    
    var vbox = VBoxContainer.new()
    vbox.name = "VBoxContainer"
    panel.add_child(vbox)
    vbox.owner = root
    
    var title = Label.new()
    title.name = "TitleLabel"
    title.text = "🌲 FACTORY RESET - OUTDOOR FOREST ARENA"
    vbox.add_child(title)
    title.owner = root
    
    var status = Label.new()
    status.name = "StatusLabel"
    status.unique_name_in_owner = true
    status.text = "MODE: DAY | [N] or [TAB] TO TOGGLE"
    vbox.add_child(status)
    status.owner = root
    
    var hint = Label.new()
    hint.name = "HintLabel"
    hint.text = "WASD: Move Sami | Center: Empty Tower Clearing (1536x1152 Map)"
    vbox.add_child(hint)
    hint.owner = root
    
    # 5. Audio
    var audio = Node.new()
    audio.name = "Audio"
    root.add_child(audio)
    audio.owner = root
    
    var day_music = AudioStreamPlayer.new()
    day_music.name = "DayMusic"
    day_music.stream = load("res://assets/audio/music/ost_day_ambient.ogg")
    day_music.volume_db = -6.0
    audio.add_child(day_music)
    day_music.owner = root
    
    var night_music = AudioStreamPlayer.new()
    night_music.name = "NightMusic"
    night_music.stream = load("res://assets/audio/music/ost_night_battle.ogg")
    night_music.volume_db = -6.0
    audio.add_child(night_music)
    night_music.owner = root
    
    var scene = PackedScene.new()
    scene.pack(root)
    var err = ResourceSaver.save(scene, "res://scenes/main/GameLevel.tscn")
    if err == OK:
        print("Successfully generated res://scenes/main/GameLevel.tscn with Nature Arena!")
    else:
        printerr("Failed to save GameLevel.tscn: ", err)
    quit()
