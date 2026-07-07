extends Control

# Nodes
@onready var line_edit_name = $PanelContainer/MarginContainer/VBoxContainer/HBoxInput/LineEditName
@onready var label_greeting = $PanelContainer/MarginContainer/VBoxContainer/LabelGreeting

@onready var slider_throttle = $PanelContainer/MarginContainer/VBoxContainer/VBoxThrottle/SliderThrottle
@onready var label_throttle_val = $PanelContainer/MarginContainer/VBoxContainer/VBoxThrottle/HBoxThrottle/LabelThrottleVal
@onready var progress_throttle = $PanelContainer/MarginContainer/VBoxContainer/VBoxThrottle/ProgressThrottle

@onready var progress_fuel = $PanelContainer/MarginContainer/VBoxContainer/VBoxFuel/ProgressFuel
@onready var btn_refuel = $PanelContainer/MarginContainer/VBoxContainer/VBoxFuel/HBoxFuel/BtnRefuel
@onready var label_status = $PanelContainer/MarginContainer/VBoxContainer/LabelStatus

@onready var btn_menu = $PanelContainer/MarginContainer/VBoxContainer/BtnMenu

# Fuel variables
var fuel_level: float = 100.0
var burn_rate: float = 1.5 # Per tick base

func _ready():
    # 1. Text Mirroring setup
    line_edit_name.text_changed.connect(_on_line_edit_text_changed)
    _on_line_edit_text_changed(line_edit_name.text)
    
    # 2. Throttle setup
    slider_throttle.value_changed.connect(_on_slider_throttle_value_changed)
    _on_slider_throttle_value_changed(slider_throttle.value)
    
    # 3. Fuel setup
    btn_refuel.pressed.connect(_on_btn_refuel_pressed)
    
    # 4. Timer setup: create a timer programmatically to burn fuel
    var timer = Timer.new()
    timer.wait_time = 0.1
    timer.autostart = true
    add_child(timer)
    timer.timeout.connect(_on_fuel_timer_tick)
    
    # 5. Menu transition
    btn_menu.pressed.connect(func(): get_tree().change_scene_to_file("res://scenes/main_menu.tscn"))

func _on_line_edit_text_changed(new_text: String):
    if new_text.strip_edges() == "":
        label_greeting.text = "Hello, Pilot! Enter your name above."
    else:
        label_greeting.text = "Welcome aboard, Commander " + new_text + "!"

func _on_slider_throttle_value_changed(value: float):
    label_throttle_val.text = "%d%%" % value
    progress_throttle.value = value
    
    # Dynamically color-modulate progress bar: Green -> Yellow -> Red
    if value < 50.0:
        progress_throttle.modulate = Color.GREEN.lerp(Color.YELLOW, value / 50.0)
    else:
        progress_throttle.modulate = Color.YELLOW.lerp(Color.RED, (value - 50.0) / 50.0)

func _on_btn_refuel_pressed():
    fuel_level = 100.0
    progress_fuel.value = 100.0
    label_status.text = "Systems fully operational."
    label_status.add_theme_color_override("font_color", Color.GREEN_YELLOW)

func _on_fuel_timer_tick():
    # Fuel burn rate is directly proportional to the engine throttle!
    var throttle_pct = slider_throttle.value
    var current_burn = burn_rate * (1.0 + (throttle_pct / 20.0)) * 0.1
    
    if fuel_level > 0.0:
        fuel_level = max(fuel_level - current_burn, 0.0)
        progress_fuel.value = fuel_level
        
        if fuel_level == 0.0:
            label_status.text = "EMERGENCY: Fuel Depleted. Engine offline."
            label_status.add_theme_color_override("font_color", Color.RED)
            slider_throttle.value = 0.0 # Force throttle cutoff
            _on_slider_throttle_value_changed(0.0)
    else:
        # If fuel is empty, keep throttle forced at 0
        slider_throttle.value = 0.0
