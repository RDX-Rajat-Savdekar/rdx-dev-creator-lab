extends Camera3D

# Target position the camera is orbiting
@export var target: Vector3 = Vector3.ZERO

# Orbit parameters
@export var min_distance: float = 2.0
@export var max_distance: float = 50.0
@export var zoom_speed: float = 0.5
@export var rotate_speed: float = 0.005

var distance: float = 10.0
var yaw: float = 0.0 # Horizontal angle
var pitch: float = 0.0 # Vertical angle

var is_rotating: bool = false
var is_panning: bool = false

func _ready():
    # Initialize from current transform
    var offset = global_position - target
    distance = offset.length()
    if distance < min_distance:
        distance = 10.0
    
    # Calculate yaw and pitch from coordinates
    yaw = atan2(offset.x, offset.z)
    pitch = clamp(asin(offset.y / distance), -PI/2 + 0.01, PI/2 - 0.01)
    
    _update_camera_position()

func _unhandled_input(event: InputEvent):
    # Zoom control
    if event is InputEventMouseButton:
        if event.button_index == MOUSE_BUTTON_WHEEL_UP:
            distance = clamp(distance - zoom_speed * 2.0, min_distance, max_distance)
            _update_camera_position()
        elif event.button_index == MOUSE_BUTTON_WHEEL_DOWN:
            distance = clamp(distance + zoom_speed * 2.0, min_distance, max_distance)
            _update_camera_position()
        
        # Click to orbit
        if event.button_index == MOUSE_BUTTON_LEFT:
            is_rotating = event.pressed
        # Click to pan
        elif event.button_index == MOUSE_BUTTON_RIGHT:
            is_panning = event.pressed

    # Rotate / Pan mouse motion
    if event is InputEventMouseMotion:
        if is_rotating:
            yaw -= event.relative.x * rotate_speed
            pitch = clamp(pitch - event.relative.y * rotate_speed, -PI/2 + 0.05, PI/2 - 0.05)
            _update_camera_position()
        elif is_panning:
            # Panning shifts the look-at target horizontally/vertically relative to camera view
            var right = global_transform.basis.x
            var up = global_transform.basis.y
            var factor = distance * 0.002
            target -= right * event.relative.x * factor
            target += up * event.relative.y * factor
            _update_camera_position()

func _update_camera_position():
    # Calculate new position using spherical coordinates
    var offset = Vector3(
        distance * cos(pitch) * sin(yaw),
        distance * sin(pitch),
        distance * cos(pitch) * cos(yaw)
    )
    global_position = target + offset
    look_at(target, Vector3.UP)
