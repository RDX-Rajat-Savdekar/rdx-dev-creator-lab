extends Node3D

@onready var star_field = $StarField
@onready var orbit_camera = $OrbitCamera

# UI references
@onready var btn_sphere = $ControlUI/Panel/MarginContainer/VBoxContainer/HBoxButtons/BtnSphere
@onready var btn_flat = $ControlUI/Panel/MarginContainer/VBoxContainer/HBoxButtons/BtnFlat
@onready var btn_cube = $ControlUI/Panel/MarginContainer/VBoxContainer/HBoxButtons/BtnCube

@onready var slider_mag = $ControlUI/Panel/MarginContainer/VBoxContainer/SliderMag
@onready var label_mag_val = $ControlUI/Panel/MarginContainer/VBoxContainer/HBoxMag/LabelMagVal

@onready var slider_twinkle = $ControlUI/Panel/MarginContainer/VBoxContainer/SliderTwinkle
@onready var label_twinkle_val = $ControlUI/Panel/MarginContainer/VBoxContainer/HBoxTwinkle/LabelTwinkleVal

func _ready():
    # Connect signals
    btn_sphere.pressed.connect(_on_btn_sphere_pressed)
    btn_flat.pressed.connect(_on_btn_flat_pressed)
    btn_cube.pressed.connect(_on_btn_cube_pressed)
    
    slider_mag.value_changed.connect(_on_slider_mag_value_changed)
    slider_twinkle.value_changed.connect(_on_slider_twinkle_value_changed)
    
    # Initialize values
    _on_slider_mag_value_changed(slider_mag.value)
    _on_slider_twinkle_value_changed(slider_twinkle.value)
    
    # Set default layout style (Sphere active)
    _update_button_states(0)

func _on_btn_sphere_pressed():
    star_field.layout_type = 0
    _update_button_states(0)
    # Reset camera target back to origin when viewing sphere
    orbit_camera.target = Vector3.ZERO
    _animate_camera_to(12.0)

func _on_btn_flat_pressed():
    star_field.layout_type = 1
    _update_button_states(1)
    # Center camera on the 2D cross layout
    var H = star_field.cube_size / 2.0
    orbit_camera.target = Vector3(H, 0, 0)
    _animate_camera_to(25.0)

func _on_btn_cube_pressed():
    star_field.layout_type = 2
    _update_button_states(2)
    # Orbit the cube center
    orbit_camera.target = Vector3.ZERO
    _animate_camera_to(15.0)

func _update_button_states(active_type: int):
    # Stylize button focus to show active state
    btn_sphere.flat = (active_type != 0)
    btn_flat.flat = (active_type != 1)
    btn_cube.flat = (active_type != 2)

func _on_slider_mag_value_changed(value: float):
    star_field.magnitude_cutoff = value
    label_mag_val.text = "%.1f" % value

func _on_slider_twinkle_value_changed(value: float):
    # Set speed uniform in the shader material of starfield
    var mat = star_field.multimesh_instance.material_override
    if mat and mat is ShaderMaterial:
        mat.set_shader_parameter("twinkle_speed", value)
    label_twinkle_val.text = "%.1f" % value

func _animate_camera_to(target_distance: float):
    # Smoothly shift the orbit distance
    var tween = create_tween().set_parallel(true).set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_OUT)
    tween.tween_property(orbit_camera, "distance", target_distance, 1.5)
