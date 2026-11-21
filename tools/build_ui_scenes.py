import os

def create_aegis_modal_scene():
    content = """[gd_scene load_steps=5 format=3 uid="uid://aegis_modal001"]

[ext_resource type="Script" path="res://scripts/ui/AegisBarterModal.gd" id="1_scr"]
[ext_resource type="Texture2D" path="res://assets/sprites/ui/portrait_aegis.png" id="2_portrait"]
[ext_resource type="AudioStream" path="res://assets/audio/sfx/ui_buy.wav" id="3_buy_sfx"]

[sub_resource type="StyleBoxFlat" id="StyleBoxFlat_panel"]
bg_color = Color(0.08, 0.1, 0.14, 0.95)
border_width_left = 2
border_width_top = 2
border_width_right = 2
border_width_bottom = 2
border_color = Color(0.2, 0.8, 1, 0.8)
corner_radius_top_left = 6
corner_radius_top_right = 6
corner_radius_bottom_right = 6
corner_radius_bottom_left = 6

[node name="AegisBarterModal" type="Control"]
layout_mode = 3
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
grow_horizontal = 2
grow_vertical = 2
script = ExtResource("1_scr")

[node name="Panel" type="Panel" parent="."]
layout_mode = 1
anchors_preset = 8
anchor_left = 0.5
anchor_top = 0.5
anchor_right = 0.5
anchor_bottom = 0.5
offset_left = -240.0
offset_top = -140.0
offset_right = 240.0
offset_bottom = 140.0
grow_horizontal = 2
grow_vertical = 2
theme_override_styles/panel = SubResource("StyleBoxFlat_panel")

[node name="VBox" type="VBoxContainer" parent="Panel"]
layout_mode = 1
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
offset_left = 14.0
offset_top = 10.0
offset_right = -14.0
offset_bottom = -10.0
grow_horizontal = 2
grow_vertical = 2

[node name="HeaderHBox" type="HBoxContainer" parent="Panel/VBox"]
layout_mode = 2

[node name="Portrait" type="TextureRect" parent="Panel/VBox/HeaderHBox"]
custom_minimum_size = Vector2(40, 40)
layout_mode = 2
texture = ExtResource("2_portrait")
expand_mode = 1
stretch_mode = 5

[node name="TitleLabel" type="Label" parent="Panel/VBox/HeaderHBox"]
unique_name_in_owner = true
layout_mode = 2
size_flags_horizontal = 3
theme_override_colors/font_color = Color(0.2, 0.85, 1, 1)
text = "SYNTHOBIOME CORP - PROTOCOL A.E.G.I.S"

[node name="BtnClose" type="Button" parent="Panel/VBox/HeaderHBox"]
unique_name_in_owner = true
layout_mode = 2
text = " [X] CLOSE "

[node name="HSeparator" type="HSeparator" parent="Panel/VBox"]
layout_mode = 2

[node name="LogLabel" type="Label" parent="Panel/VBox"]
unique_name_in_owner = true
custom_minimum_size = Vector2(0, 45)
layout_mode = 2
theme_override_colors/font_color = Color(0.7, 0.85, 0.95, 1)
theme_override_font_sizes/font_size = 11
text = "Autonomous Reclamation Node. Trade Pure Alloys for High-Density Batteries."
autowrap_mode = 2

[node name="Grid" type="GridContainer" parent="Panel/VBox"]
layout_mode = 2
size_flags_vertical = 3
columns = 2

[node name="BtnBuyBattery" type="Button" parent="Panel/VBox/Grid"]
unique_name_in_owner = true
layout_mode = 2
size_flags_horizontal = 3
size_flags_vertical = 3
text = "1x Lithium Battery
(Cost: 1 Pure Alloy)"

[node name="BtnBuySentry" type="Button" parent="Panel/VBox/Grid"]
unique_name_in_owner = true
layout_mode = 2
size_flags_horizontal = 3
size_flags_vertical = 3
text = "1x Scrap Sentry Kit
(Cost: 3 Alloys + 40 Scrap)"

[node name="BtnBuyEmp" type="Button" parent="Panel/VBox/Grid"]
unique_name_in_owner = true
layout_mode = 2
size_flags_horizontal = 3
size_flags_vertical = 3
text = "1x EMP Pulsar Core
(Cost: 4 Alloys + 1 Battery)"

[node name="BtnRepairCore" type="Button" parent="Panel/VBox/Grid"]
unique_name_in_owner = true
layout_mode = 2
size_flags_horizontal = 3
size_flags_vertical = 3
text = "Tower Core Emergency Aid (+250 HP)
(Cost: 1 Alloy + 20 Scrap)"

[node name="AudioBuy" type="AudioStreamPlayer" parent="."]
stream = ExtResource("3_buy_sfx")
"""
    with open(r"FACTORY_RESET-main\scenes\ui\AegisBarterModal.tscn", "w", encoding="utf-8") as f:
        f.write(content)
    print("Created AegisBarterModal.tscn")

def create_crafting_modal_scene():
    content = """[gd_scene load_steps=4 format=3 uid="uid://crafting_modal001"]

[ext_resource type="Script" path="res://scripts/ui/CraftingModal.gd" id="1_scr"]
[ext_resource type="AudioStream" path="res://assets/audio/sfx/ui_click.wav" id="2_click_sfx"]

[sub_resource type="StyleBoxFlat" id="StyleBoxFlat_craft"]
bg_color = Color(0.1, 0.1, 0.08, 0.95)
border_width_left = 2
border_width_top = 2
border_width_right = 2
border_width_bottom = 2
border_color = Color(0.9, 0.75, 0.2, 0.8)
corner_radius_top_left = 6
corner_radius_top_right = 6
corner_radius_bottom_right = 6
corner_radius_bottom_left = 6

[node name="CraftingModal" type="Control"]
layout_mode = 3
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
grow_horizontal = 2
grow_vertical = 2
script = ExtResource("1_scr")

[node name="Panel" type="Panel" parent="."]
layout_mode = 1
anchors_preset = 8
anchor_left = 0.5
anchor_top = 0.5
anchor_right = 0.5
anchor_bottom = 0.5
offset_left = -220.0
offset_top = -130.0
offset_right = 220.0
offset_bottom = 130.0
grow_horizontal = 2
grow_vertical = 2
theme_override_styles/panel = SubResource("StyleBoxFlat_craft")

[node name="VBox" type="VBoxContainer" parent="Panel"]
layout_mode = 1
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
offset_left = 12.0
offset_top = 10.0
offset_right = -12.0
offset_bottom = -10.0
grow_horizontal = 2
grow_vertical = 2

[node name="HeaderHBox" type="HBoxContainer" parent="Panel/VBox"]
layout_mode = 2

[node name="TitleLabel" type="Label" parent="Panel/VBox/HeaderHBox"]
layout_mode = 2
size_flags_horizontal = 3
theme_override_colors/font_color = Color(1, 0.85, 0.2, 1)
text = "FIELD WORKBENCH - SCHEMATICS [TAB]"

[node name="BtnClose" type="Button" parent="Panel/VBox/HeaderHBox"]
unique_name_in_owner = true
layout_mode = 2
text = " [X] CLOSE "

[node name="HSeparator" type="HSeparator" parent="Panel/VBox"]
layout_mode = 2

[node name="LogLabel" type="Label" parent="Panel/VBox"]
unique_name_in_owner = true
layout_mode = 2
theme_override_colors/font_color = Color(0.85, 0.85, 0.8, 1)
theme_override_font_sizes/font_size = 11
text = "Select a defensive module or component to fabricate."

[node name="Grid" type="GridContainer" parent="Panel/VBox"]
layout_mode = 2
size_flags_vertical = 3
columns = 2

[node name="BtnCraftSentry" type="Button" parent="Panel/VBox/Grid"]
unique_name_in_owner = true
layout_mode = 2
size_flags_horizontal = 3
size_flags_vertical = 3
text = "Scrap Sentry Turret
(Cost: 50 Scrap + 1 Alloy)"

[node name="BtnCraftBarricade" type="Button" parent="Panel/VBox/Grid"]
unique_name_in_owner = true
layout_mode = 2
size_flags_horizontal = 3
size_flags_vertical = 3
text = "Spiked Scrap Barricade
(Cost: 30 Scrap)"

[node name="BtnCraftRepair" type="Button" parent="Panel/VBox/Grid"]
unique_name_in_owner = true
layout_mode = 2
size_flags_horizontal = 3
size_flags_vertical = 3
text = "Repair Hazmat Suit (+40 HP)
(Cost: 15 Scrap)"

[node name="BtnCraftCoil" type="Button" parent="Panel/VBox/Grid"]
unique_name_in_owner = true
layout_mode = 2
size_flags_horizontal = 3
size_flags_vertical = 3
text = "Induction Coil Module
(Cost: 40 Scrap)"

[node name="AudioClick" type="AudioStreamPlayer" parent="."]
stream = ExtResource("2_click_sfx")
"""
    with open(r"FACTORY_RESET-main\scenes\ui\CraftingModal.tscn", "w", encoding="utf-8") as f:
        f.write(content)
    print("Created CraftingModal.tscn")

def create_hud_scene():
    content = """[gd_scene load_steps=10 format=3 uid="uid://hud001"]

[ext_resource type="Script" path="res://scripts/ui/HUD.gd" id="1_scr"]
[ext_resource type="PackedScene" path="res://scenes/ui/CraftingModal.tscn" id="2_craft"]
[ext_resource type="PackedScene" path="res://scenes/ui/AegisBarterModal.tscn" id="3_aegis"]
[ext_resource type="Texture2D" path="res://assets/sprites/icons/icon_scrap.png" id="4_scrap"]
[ext_resource type="Texture2D" path="res://assets/sprites/icons/icon_pure_alloy.png" id="5_alloy"]
[ext_resource type="Texture2D" path="res://assets/sprites/icons/icon_lithium_battery.png" id="6_bat"]
[ext_resource type="Texture2D" path="res://assets/sprites/icons/icon_nano_core.png" id="7_core"]
[ext_resource type="Texture2D" path="res://assets/sprites/ui/portrait_sami.png" id="8_portrait"]

[sub_resource type="StyleBoxFlat" id="StyleBoxFlat_top"]
bg_color = Color(0.06, 0.07, 0.09, 0.88)
border_width_bottom = 2
border_color = Color(0.2, 0.25, 0.3, 1)

[sub_resource type="StyleBoxFlat" id="StyleBoxFlat_dialogue"]
bg_color = Color(0.05, 0.08, 0.12, 0.92)
border_width_left = 2
border_width_top = 2
border_width_right = 2
border_width_bottom = 2
border_color = Color(0.2, 0.7, 0.9, 0.8)
corner_radius_top_left = 4
corner_radius_top_right = 4
corner_radius_bottom_right = 4
corner_radius_bottom_left = 4

[node name="HUD" type="Control"]
layout_mode = 3
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
grow_horizontal = 2
grow_vertical = 2
mouse_filter = 2
script = ExtResource("1_scr")

[node name="TopBar" type="Panel" parent="."]
layout_mode = 1
anchors_preset = 10
anchor_right = 1.0
offset_bottom = 36.0
grow_horizontal = 2
theme_override_styles/panel = SubResource("StyleBoxFlat_top")

[node name="HBox" type="HBoxContainer" parent="TopBar"]
layout_mode = 1
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
offset_left = 8.0
offset_right = -8.0
grow_horizontal = 2
grow_vertical = 2
theme_override_constants/separation = 12

[node name="PhaseLabel" type="Label" parent="TopBar/HBox"]
unique_name_in_owner = true
layout_mode = 2
theme_override_colors/font_color = Color(1, 0.85, 0.2, 1)
text = "DAY 1 - PURIFY SCRAP"

[node name="TimerLabel" type="Label" parent="TopBar/HBox"]
unique_name_in_owner = true
layout_mode = 2
theme_override_colors/font_color = Color(0.9, 0.9, 0.9, 1)
text = "01:00"

[node name="VSeparator1" type="VSeparator" parent="TopBar/HBox"]
layout_mode = 2

[node name="SignalLabel" type="Label" parent="TopBar/HBox"]
layout_mode = 2
theme_override_font_sizes/font_size = 11
text = "SIGNAL:"

[node name="SignalBar" type="ProgressBar" parent="TopBar/HBox"]
unique_name_in_owner = true
custom_minimum_size = Vector2(60, 14)
layout_mode = 2
size_flags_vertical = 4
value = 100.0
show_percentage = false

[node name="CoreLabel" type="Label" parent="TopBar/HBox"]
layout_mode = 2
theme_override_font_sizes/font_size = 11
text = "CORE:"

[node name="CoreBar" type="ProgressBar" parent="TopBar/HBox"]
unique_name_in_owner = true
custom_minimum_size = Vector2(60, 14)
layout_mode = 2
size_flags_vertical = 4
max_value = 1000.0
value = 1000.0
show_percentage = false

[node name="VSeparator2" type="VSeparator" parent="TopBar/HBox"]
layout_mode = 2

[node name="ResourcesHBox" type="HBoxContainer" parent="TopBar/HBox"]
layout_mode = 2
size_flags_horizontal = 3
alignment = 2

[node name="IconScrap" type="TextureRect" parent="TopBar/HBox/ResourcesHBox"]
custom_minimum_size = Vector2(18, 18)
layout_mode = 2
texture = ExtResource("4_scrap")
expand_mode = 1
stretch_mode = 5

[node name="ScrapVal" type="Label" parent="TopBar/HBox/ResourcesHBox"]
unique_name_in_owner = true
layout_mode = 2
text = "50"

[node name="Spacer1" type="Control" parent="TopBar/HBox/ResourcesHBox"]
custom_minimum_size = Vector2(8, 0)
layout_mode = 2

[node name="IconAlloy" type="TextureRect" parent="TopBar/HBox/ResourcesHBox"]
custom_minimum_size = Vector2(18, 18)
layout_mode = 2
texture = ExtResource("5_alloy")
expand_mode = 1
stretch_mode = 5

[node name="AlloyVal" type="Label" parent="TopBar/HBox/ResourcesHBox"]
unique_name_in_owner = true
layout_mode = 2
text = "0"

[node name="Spacer2" type="Control" parent="TopBar/HBox/ResourcesHBox"]
custom_minimum_size = Vector2(8, 0)
layout_mode = 2

[node name="IconBattery" type="TextureRect" parent="TopBar/HBox/ResourcesHBox"]
custom_minimum_size = Vector2(18, 18)
layout_mode = 2
texture = ExtResource("6_bat")
expand_mode = 1
stretch_mode = 5

[node name="BatteryVal" type="Label" parent="TopBar/HBox/ResourcesHBox"]
unique_name_in_owner = true
layout_mode = 2
text = "1"

[node name="Spacer3" type="Control" parent="TopBar/HBox/ResourcesHBox"]
custom_minimum_size = Vector2(8, 0)
layout_mode = 2

[node name="IconCore" type="TextureRect" parent="TopBar/HBox/ResourcesHBox"]
custom_minimum_size = Vector2(18, 18)
layout_mode = 2
texture = ExtResource("7_core")
expand_mode = 1
stretch_mode = 5

[node name="CoreVal" type="Label" parent="TopBar/HBox/ResourcesHBox"]
unique_name_in_owner = true
layout_mode = 2
text = "0"

[node name="BottomHints" type="Label" parent="."]
layout_mode = 1
anchors_preset = 12
anchor_top = 1.0
anchor_right = 1.0
anchor_bottom = 1.0
offset_top = -22.0
offset_left = 12.0
grow_horizontal = 2
grow_vertical = 0
theme_override_colors/font_color = Color(0.65, 0.7, 0.75, 0.8)
theme_override_font_sizes/font_size = 11
text = "[WASD] Move | [Click] Shoot | [Hold E] Purify Scrap | [F] AEGIS Barter | [TAB] Crafting | [N] Day/Night"

[node name="DialogueBox" type="Panel" parent="."]
unique_name_in_owner = true
layout_mode = 1
anchors_preset = 7
anchor_left = 0.5
anchor_top = 1.0
anchor_right = 0.5
anchor_bottom = 1.0
offset_left = -220.0
offset_top = -92.0
offset_right = 220.0
offset_bottom = -28.0
grow_horizontal = 2
grow_vertical = 0
theme_override_styles/panel = SubResource("StyleBoxFlat_dialogue")

[node name="HBox" type="HBoxContainer" parent="DialogueBox"]
layout_mode = 1
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
offset_left = 8.0
offset_top = 6.0
offset_right = -8.0
offset_bottom = -6.0
grow_horizontal = 2
grow_vertical = 2

[node name="PortraitRect" type="TextureRect" parent="DialogueBox/HBox"]
unique_name_in_owner = true
custom_minimum_size = Vector2(48, 48)
layout_mode = 2
texture = ExtResource("8_portrait")
expand_mode = 1
stretch_mode = 5

[node name="VBox" type="VBoxContainer" parent="DialogueBox/HBox"]
layout_mode = 2
size_flags_horizontal = 3

[node name="SpeakerLabel" type="Label" parent="DialogueBox/HBox/VBox"]
unique_name_in_owner = true
layout_mode = 2
theme_override_colors/font_color = Color(0.2, 0.85, 1, 1)
theme_override_font_sizes/font_size = 11
text = "SPEAKER"

[node name="DialogueText" type="Label" parent="DialogueBox/HBox/VBox"]
unique_name_in_owner = true
layout_mode = 2
theme_override_font_sizes/font_size = 11
text = "Transmission incoming..."
autowrap_mode = 2

[node name="CraftingModal" parent="." instance=ExtResource("2_craft")]
unique_name_in_owner = true
visible = false
layout_mode = 1

[node name="AegisModal" parent="." instance=ExtResource("3_aegis")]
unique_name_in_owner = true
visible = false
layout_mode = 1
"""
    with open(r"FACTORY_RESET-main\scenes\ui\HUD.tscn", "w", encoding="utf-8") as f:
        f.write(content)
    print("Created HUD.tscn")

os.makedirs(r"FACTORY_RESET-main\scenes\ui", exist_ok=True)
create_aegis_modal_scene()
create_crafting_modal_scene()
create_hud_scene()
print("All UI scenes created successfully!")
