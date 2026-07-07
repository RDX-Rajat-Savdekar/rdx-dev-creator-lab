extends Node3D

@onready var marbles_container = $Marbles
@onready var void_area = $VoidArea
@onready var label_counts = $ControlUI/Panel/MarginContainer/VBoxContainer/LabelCounts
@onready var btn_menu = $ControlUI/BtnMenu
@onready var camera = $Camera3D

# Counting states
var spawned_count: int = 0
var escaped_count: int = 0

func _ready():
	# Connect void sensor
	void_area.body_entered.connect(_on_void_body_entered)
	btn_menu.pressed.connect(func(): get_tree().change_scene_to_file("res://scenes/main_menu.tscn"))
	_update_ui()

func _input(event):
	# 1. Spawn marble when pressing SPACE
	if event.is_action_pressed("ui_accept") and not event.is_echo(): # Spacebar
		_spawn_marble()

	# 2. Click to trigger raycast explosion
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
		_trigger_raycast_explosion(event.position)

func _spawn_marble():
	var marble = RigidBody3D.new()
	marbles_container.add_child(marble)
	
	# Position slightly offset to drop on the tray
	marble.global_position = Vector3(randf_range(-1.5, 1.5), 5.0, randf_range(-1.5, 1.5))
	
	# Physics parameters
	marble.mass = 1.0
	
	# Physics Material: bouncy!
	var phys_mat = PhysicsMaterial.new()
	phys_mat.bounce = 0.65
	phys_mat.friction = 0.1
	marble.physics_material_override = phys_mat
	
	# Collision shape: Sphere
	var col_shape = CollisionShape3D.new()
	var sphere_shape = SphereShape3D.new()
	sphere_shape.radius = 0.25
	col_shape.shape = sphere_shape
	marble.add_child(col_shape)
	
	# MeshInstance for rendering
	var mesh_inst = MeshInstance3D.new()
	var sphere_mesh = SphereMesh.new()
	sphere_mesh.radius = 0.25
	sphere_mesh.height = 0.5
	mesh_inst.mesh = sphere_mesh
	marble.add_child(mesh_inst)
	
	# Metallic glowing material
	var mat = StandardMaterial3D.new()
	mat.albedo_color = Color.from_hsv(randf(), 0.9, 0.9)
	mat.roughness = 0.1
	mat.metallic = 0.8
	mat.emission_enabled = true
	mat.emission = mat.albedo_color * 0.4
	mesh_inst.material_override = mat
	
	spawned_count += 1
	_update_ui()

func _trigger_raycast_explosion(mouse_pos: Vector2):
	# Perform screen-to-world raycast
	var from = camera.project_ray_origin(mouse_pos)
	var to = from + camera.project_ray_normal(mouse_pos) * 100.0
	
	var space_state = get_world_3d().direct_space_state
	var query = PhysicsRayQueryParameters3D.create(from, to)
	var result = space_state.intersect_ray(query)
	
	if result:
		# We hit a surface! Let's get the 3D position
		var hit_point = result.position
		
		# Trigger visual push to all nearby marbles
		var explosion_radius = 5.0
		var push_force = 12.0
		
		for marble in marbles_container.get_children():
			if marble is RigidBody3D:
				var offset = marble.global_position - hit_point
				var dist = offset.length()
				if dist < explosion_radius:
					var dir = offset.normalized()
					# Closer marbles get pushed stronger
					var force = (1.0 - (dist / explosion_radius)) * push_force
					marble.apply_central_impulse(dir * force)
					
		# Visual effect: Spawn a temporary glowing ring at hit spot
		_spawn_explosion_ring(hit_point)

func _spawn_explosion_ring(pos: Vector3):
	var ring = MeshInstance3D.new()
	add_child(ring)
	ring.global_position = pos
	
	var torus = TorusMesh.new()
	torus.inner_radius = 0.05
	torus.outer_radius = 0.1
	torus.rings = 32
	torus.ring_segments = 16
	ring.mesh = torus
	
	var mat = StandardMaterial3D.new()
	mat.shading_mode = StandardMaterial3D.SHADING_MODE_UNSHADED
	mat.albedo_color = Color("#ff6600")
	ring.material_override = mat
	
	# Animate expansion and fade out using a Tween
	var tween = create_tween().set_parallel(true)
	tween.tween_property(ring, "scale", Vector3.ONE * 5.0, 0.4)
	tween.tween_property(mat, "albedo_color:a", 0.0, 0.4)
	tween.chain().kill()
	
	# Delete mesh when done
	get_tree().create_timer(0.4).timeout.connect(func(): ring.queue_free())

func _on_void_body_entered(body: Node):
	# If a marble falls into the void, remove it and increment count
	# RigidBody nodes spawn directly as children of the marbles container
	if body.get_parent() == marbles_container:
		body.queue_free()
		escaped_count += 1
		# Need to call deferred or wait a frame to let count reduce
		get_tree().create_timer(0.05).timeout.connect(_update_ui)

func _update_ui():
	label_counts.text = (
		"Active Marbles: %d\n" % marbles_container.get_child_count() +
		"Spawned Total: %d\n" % spawned_count +
		"Escaped/Void: %d" % escaped_count
	)
