import os

def create_bullet_scene():
    content = """[gd_scene load_steps=4 format=3 uid="uid://bullet001"]

[ext_resource type="Script" path="res://scripts/entities/Bullet.gd" id="1_scr"]
[ext_resource type="Texture2D" path="res://assets/sprites/weapons/muzzle_flash.png" id="2_tex"]

[sub_resource type="CircleShape2D" id="CircleShape2D_1"]
radius = 4.0

[node name="Bullet" type="Area2D"]
collision_layer = 32
collision_mask = 5
script = ExtResource("1_scr")

[node name="Sprite2D" type="Sprite2D" parent="."]
modulate = Color(1, 0.9, 0.4, 1)
scale = Vector2(0.3, 0.3)
texture = ExtResource("2_tex")

[node name="CollisionShape2D" type="CollisionShape2D" parent="."]
shape = SubResource("CircleShape2D_1")
"""
    with open(r"FACTORY_RESET-main\scenes\entities\Bullet.tscn", "w", encoding="utf-8") as f:
        f.write(content)
    print("Created Bullet.tscn")

def create_shockwave_scene():
    content = """[gd_scene load_steps=5 format=3 uid="uid://shockwave001"]

[ext_resource type="Script" path="res://scripts/entities/Shockwave.gd" id="1_scr"]
[ext_resource type="Texture2D" path="res://assets/sprites/weapons/shockwave_ring.png" id="2_ring"]
[ext_resource type="AudioStream" path="res://assets/audio/sfx/shockwave_burst.wav" id="3_sfx"]

[sub_resource type="CircleShape2D" id="CircleShape2D_1"]
radius = 150.0

[node name="Shockwave" type="Area2D"]
collision_layer = 64
collision_mask = 4
script = ExtResource("1_scr")

[node name="Sprite2D" type="Sprite2D" parent="."]
modulate = Color(0.2, 0.8, 1, 0.9)
scale = Vector2(2.3, 2.3)
texture = ExtResource("2_ring")

[node name="CollisionShape2D" type="CollisionShape2D" parent="."]
shape = SubResource("CircleShape2D_1")

[node name="AudioStreamPlayer2D" type="AudioStreamPlayer2D" parent="."]
stream = ExtResource("3_sfx")
volume_db = 2.0
"""
    with open(r"FACTORY_RESET-main\scenes\entities\Shockwave.tscn", "w", encoding="utf-8") as f:
        f.write(content)
    print("Created Shockwave.tscn")

def create_scrappile_scene():
    content = """[gd_scene load_steps=6 format=3 uid="uid://scrappile001"]

[ext_resource type="Script" path="res://scripts/entities/ScrapPile.gd" id="1_scr"]
[ext_resource type="Texture2D" path="res://assets/sprites/environment/scrap_pile/scrap_pile_inert.png" id="2_inert"]
[ext_resource type="AudioStream" path="res://assets/audio/sfx/scrap_pickup.wav" id="3_pickup"]
[ext_resource type="AudioStream" path="res://assets/audio/sfx/alloy_crafted.wav" id="4_purify"]

[sub_resource type="CircleShape2D" id="CircleShape2D_1"]
radius = 28.0

[node name="ScrapPile" type="Area2D" groups=["ScrapPiles"]]
collision_layer = 8
collision_mask = 6
script = ExtResource("1_scr")

[node name="Sprite2D" type="Sprite2D" parent="."]
scale = Vector2(0.65, 0.65)
texture = ExtResource("2_inert")

[node name="CollisionShape2D" type="CollisionShape2D" parent="."]
shape = SubResource("CircleShape2D_1")

[node name="ProgressBar" type="TextureProgressBar" parent="."]
offset_left = -20.0
offset_top = -28.0
offset_right = 20.0
offset_bottom = -22.0
max_value = 0.8
step = 0.01

[node name="AudioPickup" type="AudioStreamPlayer2D" parent="."]
stream = ExtResource("3_pickup")

[node name="AudioPurify" type="AudioStreamPlayer2D" parent="."]
stream = ExtResource("4_purify")
"""
    with open(r"FACTORY_RESET-main\scenes\entities\ScrapPile.tscn", "w", encoding="utf-8") as f:
        f.write(content)
    print("Created ScrapPile.tscn")

def create_amalgam_scene():
    content = """[gd_scene load_steps=18 format=3 uid="uid://amalgam001"]

[ext_resource type="Script" path="res://scripts/entities/EnemyAmalgam.gd" id="1_scr"]
[ext_resource type="Texture2D" path="res://assets/sprites/monsters/amalgam/amalgam_idle.png" id="2_idle"]
[ext_resource type="Texture2D" path="res://assets/sprites/monsters/amalgam/amalgam_attack_0.png" id="3_atk0"]
[ext_resource type="Texture2D" path="res://assets/sprites/monsters/amalgam/amalgam_attack_1.png" id="4_atk1"]
[ext_resource type="Texture2D" path="res://assets/sprites/monsters/amalgam/amalgam_attack_2.png" id="5_atk2"]
[ext_resource type="Texture2D" path="res://assets/sprites/monsters/amalgam/amalgam_attack_3.png" id="6_atk3"]
[ext_resource type="Texture2D" path="res://assets/sprites/monsters/amalgam/amalgam_hit.png" id="7_hit"]
[ext_resource type="Texture2D" path="res://assets/sprites/monsters/amalgam/amalgam_walk_0.png" id="8_w0"]
[ext_resource type="Texture2D" path="res://assets/sprites/monsters/amalgam/amalgam_walk_1.png" id="9_w1"]
[ext_resource type="Texture2D" path="res://assets/sprites/monsters/amalgam/amalgam_walk_2.png" id="10_w2"]
[ext_resource type="Texture2D" path="res://assets/sprites/monsters/amalgam/amalgam_walk_3.png" id="11_w3"]
[ext_resource type="Texture2D" path="res://assets/sprites/monsters/amalgam/amalgam_walk_4.png" id="12_w4"]
[ext_resource type="Texture2D" path="res://assets/sprites/monsters/amalgam/amalgam_walk_5.png" id="13_w5"]
[ext_resource type="AudioStream" path="res://assets/audio/sfx/amalgam_smash.wav" id="14_smash"]
[ext_resource type="AudioStream" path="res://assets/audio/sfx/crawler_bite.wav" id="15_bite"]

[sub_resource type="SpriteFrames" id="SpriteFrames_1"]
animations = [{
"frames": [{
"duration": 1.0,
"texture": ExtResource("3_atk0")
}, {
"duration": 1.0,
"texture": ExtResource("4_atk1")
}, {
"duration": 1.0,
"texture": ExtResource("5_atk2")
}, {
"duration": 1.0,
"texture": ExtResource("6_atk3")
}],
"loop": false,
"name": &"attack",
"speed": 8.0
}, {
"frames": [{
"duration": 1.0,
"texture": ExtResource("7_hit")
}],
"loop": false,
"name": &"hit",
"speed": 5.0
}, {
"frames": [{
"duration": 1.0,
"texture": ExtResource("2_idle")
}],
"loop": true,
"name": &"idle",
"speed": 5.0
}, {
"frames": [{
"duration": 1.0,
"texture": ExtResource("8_w0")
}, {
"duration": 1.0,
"texture": ExtResource("9_w1")
}, {
"duration": 1.0,
"texture": ExtResource("10_w2")
}, {
"duration": 1.0,
"texture": ExtResource("11_w3")
}, {
"duration": 1.0,
"texture": ExtResource("12_w4")
}, {
"duration": 1.0,
"texture": ExtResource("13_w5")
}],
"loop": true,
"name": &"walk",
"speed": 8.0
}]

[sub_resource type="CapsuleShape2D" id="CapsuleShape2D_1"]
radius = 16.0
height = 38.0

[node name="EnemyAmalgam" type="CharacterBody2D" groups=["Enemies"]]
collision_layer = 4
collision_mask = 19
script = ExtResource("1_scr")

[node name="AnimatedSprite2D" type="AnimatedSprite2D" parent="."]
scale = Vector2(0.4, 0.4)
sprite_frames = SubResource("SpriteFrames_1")
animation = &"walk"

[node name="CollisionShape2D" type="CollisionShape2D" parent="."]
position = Vector2(0, 4)
shape = SubResource("CapsuleShape2D_1")

[node name="HealthBar" type="ProgressBar" parent="."]
offset_left = -18.0
offset_top = -28.0
offset_right = 18.0
offset_bottom = -23.0
max_value = 350.0
value = 350.0
show_percentage = false

[node name="AudioHit" type="AudioStreamPlayer2D" parent="."]
stream = ExtResource("15_bite")

[node name="AudioAttack" type="AudioStreamPlayer2D" parent="."]
stream = ExtResource("14_smash")
"""
    with open(r"FACTORY_RESET-main\scenes\entities\EnemyAmalgam.tscn", "w", encoding="utf-8") as f:
        f.write(content)
    print("Created EnemyAmalgam.tscn")

def create_aegis_scene():
    content = """[gd_scene load_steps=12 format=3 uid="uid://aegis001"]

[ext_resource type="Script" path="res://scripts/entities/AegisDrone.gd" id="1_scr"]
[ext_resource type="Texture2D" path="res://assets/sprites/characters/drone/drone_idle_0.png" id="2_id0"]
[ext_resource type="Texture2D" path="res://assets/sprites/characters/drone/drone_idle_1.png" id="3_id1"]
[ext_resource type="Texture2D" path="res://assets/sprites/characters/drone/drone_idle_2.png" id="4_id2"]
[ext_resource type="Texture2D" path="res://assets/sprites/characters/drone/drone_idle_3.png" id="5_id3"]
[ext_resource type="Texture2D" path="res://assets/sprites/characters/drone/drone_scan_0.png" id="6_sc0"]
[ext_resource type="Texture2D" path="res://assets/sprites/characters/drone/drone_scan_1.png" id="7_sc1"]
[ext_resource type="Texture2D" path="res://assets/sprites/characters/drone/drone_scan_2.png" id="8_sc2"]
[ext_resource type="Texture2D" path="res://assets/sprites/characters/drone/drone_scan_3.png" id="9_sc3"]

[sub_resource type="SpriteFrames" id="SpriteFrames_1"]
animations = [{
"frames": [{
"duration": 1.0,
"texture": ExtResource("2_id0")
}, {
"duration": 1.0,
"texture": ExtResource("3_id1")
}, {
"duration": 1.0,
"texture": ExtResource("4_id2")
}, {
"duration": 1.0,
"texture": ExtResource("5_id3")
}],
"loop": true,
"name": &"idle",
"speed": 6.0
}, {
"frames": [{
"duration": 1.0,
"texture": ExtResource("6_sc0")
}, {
"duration": 1.0,
"texture": ExtResource("7_sc1")
}, {
"duration": 1.0,
"texture": ExtResource("8_sc2")
}, {
"duration": 1.0,
"texture": ExtResource("9_sc3")
}],
"loop": true,
"name": &"scan",
"speed": 6.0
}]

[sub_resource type="CircleShape2D" id="CircleShape2D_1"]
radius = 48.0

[node name="AegisDrone" type="Node2D" groups=["AEGIS"]]
script = ExtResource("1_scr")

[node name="AnimatedSprite2D" type="AnimatedSprite2D" parent="."]
scale = Vector2(0.55, 0.55)
sprite_frames = SubResource("SpriteFrames_1")
animation = &"idle"

[node name="InteractionArea" type="Area2D" parent="."]
collision_layer = 0
collision_mask = 2

[node name="CollisionShape2D" type="CollisionShape2D" parent="InteractionArea"]
shape = SubResource("CircleShape2D_1")

[node name="PromptLabel" type="Label" parent="."]
offset_left = -90.0
offset_top = -42.0
offset_right = 90.0
offset_bottom = -22.0
text = "[F] TRADE WITH PROTOCOL AEGIS"
horizontal_alignment = 1

[node name="ScanLight" type="PointLight2D" parent="."]
color = Color(0.2, 0.8, 1, 0.8)
energy = 1.2
"""
    with open(r"FACTORY_RESET-main\scenes\entities\AegisDrone.tscn", "w", encoding="utf-8") as f:
        f.write(content)
    print("Created AegisDrone.tscn")

def create_sentry_scene():
    content = """[gd_scene load_steps=5 format=3 uid="uid://sentry001"]

[ext_resource type="Script" path="res://scripts/entities/ScrapSentry.gd" id="1_scr"]
[ext_resource type="Texture2D" path="res://assets/sprites/turrets/scrap_sentry.png" id="2_tex"]
[ext_resource type="AudioStream" path="res://assets/audio/sfx/sentry_shoot.wav" id="3_sfx"]

[sub_resource type="CircleShape2D" id="CircleShape2D_1"]
radius = 14.0

[node name="ScrapSentry" type="StaticBody2D" groups=["Turrets"]]
collision_layer = 16
collision_mask = 4
script = ExtResource("1_scr")

[node name="Sprite2D" type="Sprite2D" parent="."]
scale = Vector2(0.8, 0.8)
texture = ExtResource("2_tex")

[node name="CollisionShape2D" type="CollisionShape2D" parent="."]
shape = SubResource("CircleShape2D_1")

[node name="BarrelPivot" type="Node2D" parent="."]

[node name="AudioShoot" type="AudioStreamPlayer2D" parent="."]
stream = ExtResource("3_sfx")
volume_db = -4.0
"""
    with open(r"FACTORY_RESET-main\scenes\entities\ScrapSentry.tscn", "w", encoding="utf-8") as f:
        f.write(content)
    print("Created ScrapSentry.tscn")

def update_sami_player_scene():
    content = """[gd_scene load_steps=14 format=3 uid="uid://cx6i8v1sami"]

[ext_resource type="Script" path="res://scripts/entities/SamiPlayer.gd" id="1_sami"]
[ext_resource type="Texture2D" path="res://assets/sprites/characters/sami/sami_idle.png" id="2_idle"]
[ext_resource type="Texture2D" path="res://assets/sprites/characters/sami/sami_shoot.png" id="3_shoot"]
[ext_resource type="Texture2D" path="res://assets/sprites/characters/sami/sami_walk_0.png" id="4_w0"]
[ext_resource type="Texture2D" path="res://assets/sprites/characters/sami/sami_walk_1.png" id="5_w1"]
[ext_resource type="Texture2D" path="res://assets/sprites/characters/sami/sami_walk_2.png" id="6_w2"]
[ext_resource type="Texture2D" path="res://assets/sprites/characters/sami/sami_walk_3.png" id="7_w3"]
[ext_resource type="Texture2D" path="res://assets/sprites/characters/sami/sami_weld.png" id="8_weld"]
[ext_resource type="Texture2D" path="res://assets/sprites/weapons/gun_rifle.png" id="9_gun"]
[ext_resource type="Texture2D" path="res://assets/sprites/weapons/muzzle_flash.png" id="10_flash"]
[ext_resource type="AudioStream" path="res://assets/audio/sfx/weld_resonate.wav" id="11_weld_sfx"]
[ext_resource type="AudioStream" path="res://assets/audio/sfx/sentry_shoot.wav" id="12_shoot_sfx"]

[sub_resource type="SpriteFrames" id="SpriteFrames_sami"]
animations = [{
"frames": [{
"duration": 1.0,
"texture": ExtResource("2_idle")
}],
"loop": true,
"name": &"idle",
"speed": 5.0
}, {
"frames": [{
"duration": 1.0,
"texture": ExtResource("3_shoot")
}],
"loop": false,
"name": &"shoot",
"speed": 10.0
}, {
"frames": [{
"duration": 1.0,
"texture": ExtResource("4_w0")
}, {
"duration": 1.0,
"texture": ExtResource("5_w1")
}, {
"duration": 1.0,
"texture": ExtResource("6_w2")
}, {
"duration": 1.0,
"texture": ExtResource("7_w3")
}],
"loop": true,
"name": &"walk",
"speed": 8.0
}, {
"frames": [{
"duration": 1.0,
"texture": ExtResource("8_weld")
}],
"loop": true,
"name": &"weld",
"speed": 6.0
}]

[sub_resource type="CapsuleShape2D" id="CapsuleShape2D_body"]
radius = 8.0
height = 24.0

[sub_resource type="CircleShape2D" id="CircleShape2D_interact"]
radius = 36.0

[node name="SamiPlayer" type="CharacterBody2D" groups=["Player"]]
collision_layer = 2
collision_mask = 5
script = ExtResource("1_sami")

[node name="AnimatedSprite2D" type="AnimatedSprite2D" parent="."]
scale = Vector2(0.4, 0.4)
sprite_frames = SubResource("SpriteFrames_sami")
animation = &"idle"

[node name="WeaponPivot" type="Node2D" parent="."]
position = Vector2(0, 2)

[node name="GunSprite" type="Sprite2D" parent="WeaponPivot"]
position = Vector2(10, 0)
scale = Vector2(0.3, 0.3)
texture = ExtResource("9_gun")

[node name="MuzzleFlash" type="Sprite2D" parent="WeaponPivot"]
position = Vector2(24, 0)
scale = Vector2(0.35, 0.35)
texture = ExtResource("10_flash")

[node name="CollisionShape2D" type="CollisionShape2D" parent="."]
position = Vector2(0, 4)
shape = SubResource("CapsuleShape2D_body")

[node name="InteractionArea" type="Area2D" parent="."]
collision_layer = 0
collision_mask = 8

[node name="CollisionShape2D" type="CollisionShape2D" parent="InteractionArea"]
shape = SubResource("CircleShape2D_interact")

[node name="WeldAudio" type="AudioStreamPlayer2D" parent="."]
stream = ExtResource("11_weld_sfx")

[node name="ShootAudio" type="AudioStreamPlayer2D" parent="."]
stream = ExtResource("12_shoot_sfx")
volume_db = -2.0

[connection signal="area_entered" from="InteractionArea" to="." method="_on_interaction_area_entered"]
[connection signal="area_exited" from="InteractionArea" to="." method="_on_interaction_area_exited"]
"""
    with open(r"FACTORY_RESET-main\scenes\entities\SamiPlayer.tscn", "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated SamiPlayer.tscn")

def create_telecom_core_scene():
    content = """[gd_scene load_steps=13 format=3 uid="uid://telecomcore001"]

[ext_resource type="Script" path="res://scripts/environment/TelecomTowerCore.gd" id="1_scr"]
[ext_resource type="Texture2D" path="res://assets/sprites/environment/telecom_tower_day.png" id="2_day"]
[ext_resource type="Texture2D" path="res://assets/sprites/weapons/shockwave_ring.png" id="3_ring"]
[ext_resource type="AudioStream" path="res://assets/audio/sfx/core_alarm.wav" id="4_alarm"]
[ext_resource type="Texture2D" path="res://assets/sprites/props/power_generator.png" id="5_gen"]
[ext_resource type="Texture2D" path="res://assets/sprites/props/workbench_electronics.png" id="6_elec"]
[ext_resource type="Texture2D" path="res://assets/sprites/props/workbench_mechanical.png" id="7_mech"]
[ext_resource type="Texture2D" path="res://assets/sprites/props/cable_spool.png" id="8_spool"]
[ext_resource type="Texture2D" path="res://assets/sprites/props/telecom_junction_box.png" id="9_box"]
[ext_resource type="Texture2D" path="res://assets/sprites/props/tower_terminal.png" id="10_term"]

[sub_resource type="RectangleShape2D" id="RectangleShape2D_base"]
size = Vector2(72, 40)

[sub_resource type="CircleShape2D" id="CircleShape2D_core"]
radius = 42.0

[node name="TelecomTowerCore" type="StaticBody2D" groups=["CoreTower"]]
collision_layer = 129
collision_mask = 6
script = ExtResource("1_scr")

[node name="FrequencyRing" type="Sprite2D" parent="."]
modulate = Color(0.1, 0.8, 1, 0.6)
scale = Vector2(1.8, 1.8)
texture = ExtResource("3_ring")

[node name="TowerSprite" type="Sprite2D" parent="."]
position = Vector2(0, -70)
scale = Vector2(0.7, 0.7)
texture = ExtResource("2_day")

[node name="CollisionShape2D" type="CollisionShape2D" parent="."]
position = Vector2(0, -6)
shape = SubResource("RectangleShape2D_base")

[node name="Props" type="Node2D" parent="."]

[node name="Generator" type="Sprite2D" parent="Props"]
position = Vector2(-75, 15)
scale = Vector2(0.55, 0.55)
texture = ExtResource("5_gen")

[node name="ElecBench" type="Sprite2D" parent="Props"]
position = Vector2(75, -20)
scale = Vector2(0.55, 0.55)
texture = ExtResource("6_elec")

[node name="MechBench" type="Sprite2D" parent="Props"]
position = Vector2(80, 25)
scale = Vector2(0.55, 0.55)
texture = ExtResource("7_mech")

[node name="Terminal" type="Sprite2D" parent="Props"]
position = Vector2(-55, -30)
scale = Vector2(0.5, 0.5)
texture = ExtResource("10_term")

[node name="CableSpool" type="Sprite2D" parent="Props"]
position = Vector2(-95, -15)
scale = Vector2(0.5, 0.5)
texture = ExtResource("8_spool")

[node name="JunctionBox" type="Sprite2D" parent="Props"]
position = Vector2(40, -45)
scale = Vector2(0.45, 0.45)
texture = ExtResource("9_box")

[node name="AudioAlarm" type="AudioStreamPlayer2D" parent="."]
stream = ExtResource("4_alarm")
volume_db = 4.0

[node name="BeaconLight" type="PointLight2D" parent="."]
position = Vector2(0, -145)
color = Color(1, 0.1, 0.1, 1)
energy = 1.8
"""
    with open(r"FACTORY_RESET-main\scenes\environment\TelecomTowerCore.tscn", "w", encoding="utf-8") as f:
        f.write(content)
    print("Created TelecomTowerCore.tscn")

create_bullet_scene()
create_shockwave_scene()
create_scrappile_scene()
create_amalgam_scene()
create_aegis_scene()
create_sentry_scene()
update_sami_player_scene()
create_telecom_core_scene()
print("All entity scenes created successfully!")
