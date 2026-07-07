extends Control

@onready var btn_stage_1 = $MarginContainer/VBoxContainer/GridContainer/BtnStage1
@onready var btn_stage_3 = $MarginContainer/VBoxContainer/GridContainer/BtnStage3
@onready var btn_stage_4 = $MarginContainer/VBoxContainer/GridContainer/BtnStage4
@onready var btn_stage_5 = $MarginContainer/VBoxContainer/GridContainer/BtnStage5
@onready var btn_exit = $MarginContainer/VBoxContainer/BtnExit

func _ready():
    btn_stage_1.pressed.connect(func(): get_tree().change_scene_to_file("res://scenes/main_presentation.tscn"))
    btn_stage_3.pressed.connect(func(): get_tree().change_scene_to_file("res://scenes/stage3_ui_dashboard.tscn"))
    btn_stage_4.pressed.connect(func(): get_tree().change_scene_to_file("res://scenes/stage4_portal_shader.tscn"))
    btn_stage_5.pressed.connect(func(): get_tree().change_scene_to_file("res://scenes/stage5_physics_sandbox.tscn"))
    btn_exit.pressed.connect(func(): get_tree().quit())
