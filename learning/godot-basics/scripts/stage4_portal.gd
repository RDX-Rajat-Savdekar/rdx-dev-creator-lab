extends Node3D

@onready var portal_mesh = $PortalMesh
@onready var label_info = $ControlUI/Panel/MarginContainer/VBoxContainer/LabelInfo
@onready var btn_menu = $ControlUI/BtnMenu

# Shader variables we will modify dynamically
var amplitude: float = 0.15
var frequency: float = 5.0
var color_index: int = 0
var colors: Array[Color] = [
    Color(0.0, 0.8, 1.0, 1.0), # Neon Cyan
    Color(1.0, 0.0, 1.0, 1.0), # Magenta Pink
    Color(1.0, 0.8, 0.0, 1.0), # Golden Sun
    Color(0.0, 1.0, 0.4, 1.0)  # Emerald Green
]

func _ready():
    # Setup initial material overrides
    _update_shader_parameters()
    btn_menu.pressed.connect(func(): get_tree().change_scene_to_file("res://scenes/main_menu.tscn"))

func _process(delta):
    # Rotate the portal mesh to show off the shader
    portal_mesh.rotate_y(delta * 0.5)
    portal_mesh.rotation.z = sin(Time.get_ticks_msec() * 0.001) * 0.1
    
    # Check continuous keyboard inputs
    var changed = false
    
    if Input.is_action_pressed("ui_up"):
        amplitude = clamp(amplitude + delta * 0.2, 0.0, 0.5)
        changed = true
    elif Input.is_action_pressed("ui_down"):
        amplitude = clamp(amplitude - delta * 0.2, 0.0, 0.5)
        changed = true
        
    if changed:
        _update_shader_parameters()

func _input(event):
    if event is InputEventKey and event.pressed and not event.is_echo():
        var changed = false
        if event.keycode == KEY_SPACE or event.keycode == KEY_C:
            color_index = (color_index + 1) % colors.size()
            changed = true
        elif event.keycode == KEY_RIGHT:
            frequency = clamp(frequency + 1.0, 1.0, 16.0)
            changed = true
        elif event.keycode == KEY_LEFT:
            frequency = clamp(frequency - 1.0, 1.0, 16.0)
            changed = true
            
        if changed:
            _update_shader_parameters()

func _update_shader_parameters():
    var mat = portal_mesh.material_override
    if mat and mat is ShaderMaterial:
        mat.set_shader_parameter("ripple_amplitude", amplitude)
        mat.set_shader_parameter("ripple_frequency", frequency)
        mat.set_shader_parameter("portal_color", colors[color_index])
        
    # Update UI text
    label_info.text = (
        "Ripple Amplitude: %.2f (Up/Down Arrows)\n" % amplitude +
        "Ripple Frequency: %d (Left/Right Arrows)\n" % frequency +
        "Portal Color: %s (Space/C to Cycle)" % _get_color_name(color_index)
    )

func _get_color_name(idx: int) -> String:
    match idx:
        0: return "Neon Cyan"
        1: return "Magenta Pink"
        2: return "Golden Sun"
        3: return "Emerald Green"
    return "Unknown"
