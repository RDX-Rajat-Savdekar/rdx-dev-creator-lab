extends Node3D

@export var star_count: int = 600
@export var sphere_radius: float = 10.0
@export var cube_size: float = 11.54 # 2 * R / sqrt(3)
@export var transition_speed: float = 4.0

# Active layout type: 0 = Sphere, 1 = Flat Net, 2 = Folded Cube
var layout_type: int = 0

# Cutoffs for interactive filtering
var magnitude_cutoff: float = 6.0
var min_bv_cutoff: float = -0.5
var max_bv_cutoff: float = 2.0

# Star data array
var stars: Array = []

# References to nodes
var multimesh_instance: MultiMeshInstance3D
var sphere_grid_instance: MeshInstance3D
var cube_grid_instance: MeshInstance3D
var flat_grid_instance: MeshInstance3D

# Alphas for wireframes
var sphere_grid_alpha: float = 1.0
var cube_grid_alpha: float = 0.0
var flat_grid_alpha: float = 0.0

func _ready():
    # 1. Setup MultiMeshInstance3D
    multimesh_instance = MultiMeshInstance3D.new()
    add_child(multimesh_instance)
    
    var mm = MultiMesh.new()
    mm.transform_format = MultiMesh.TRANSFORM_3D
    mm.use_colors = true
    mm.instance_count = star_count
    
    # Simple quad mesh facing the camera (billboard)
    var quad = QuadMesh.new()
    quad.size = Vector2(0.15, 0.15)
    mm.mesh = quad
    
    multimesh_instance.multimesh = mm
    
    # Assign custom twinkle shader material
    var material = ShaderMaterial.new()
    material.shader = load("res://shaders/star_twinkle.gdshader")
    multimesh_instance.material_override = material
    
    # 2. Generate Star Data
    _generate_star_database()
    
    # 3. Create Wireframes
    _create_sphere_grid()
    _create_cube_grid()
    _create_flat_grid()

func _generate_star_database():
    # Seed generator for consistent layout
    seed(42)
    stars.clear()
    
    for i in range(star_count):
        # Generate random astronomical coordinates
        # RA: 0 to 24 hours
        var ra = randf() * 24.0
        # Dec: -90 to +90 degrees (using sine distribution for uniform spherical coverage)
        var dec = rad_to_deg(asin(randf() * 2.0 - 1.0))
        # Magnitude: 1.0 (bright) to 7.0 (dim)
        var magnitude = randf_range(1.0, 7.0)
        # B-V color index: -0.4 (blue/hot) to 2.0 (red/cool)
        var bv = randf_range(-0.4, 2.0)
        
        # Calculate Sphere Position
        var theta = ra * (PI / 12.0) # RA to radians
        var phi = deg_to_rad(dec)    # Dec to radians
        var s_pos = Vector3(
            sphere_radius * cos(phi) * cos(theta),
            sphere_radius * sin(phi),
            sphere_radius * cos(phi) * sin(theta)
        )
        
        # Calculate Cube & Flat Net Positions
        var proj = _project_to_cube(s_pos, cube_size / 2.0)
        var c_pos = proj.position
        var f_pos = _flatten_cube_face(proj.face, c_pos, cube_size / 2.0)
        
        var star_color = _bv_to_color(bv)
        
        stars.append({
            "ra": ra,
            "dec": dec,
            "magnitude": magnitude,
            "bv": bv,
            "color": star_color,
            "sphere_pos": s_pos,
            "cube_pos": c_pos,
            "flat_pos": f_pos,
            "current_pos": s_pos
        })

func _project_to_cube(pos: Vector3, H: float) -> Dictionary:
    var u = pos.normalized()
    var abs_x = abs(u.x)
    var abs_y = abs(u.y)
    var abs_z = abs(u.z)
    var max_val = max(abs_x, max(abs_y, abs_z))
    
    var face_idx = 0
    var c_pos = Vector3.ZERO
    
    if max_val == abs_y:
        if u.y > 0:
            face_idx = 0 # Top (+Y)
            c_pos = Vector3(u.x / u.y * H, H, u.z / u.y * H)
        else:
            face_idx = 1 # Bottom (-Y)
            c_pos = Vector3(-u.x / abs_y * H, -H, -u.z / abs_y * H)
    elif max_val == abs_z:
        if u.z > 0:
            face_idx = 2 # Front (+Z)
            c_pos = Vector3(u.x / u.z * H, u.y / u.z * H, H)
        else:
            face_idx = 3 # Back (-Z)
            c_pos = Vector3(-u.x / abs_z * H, u.y / abs_z * H, -H)
    else:
        if u.x > 0:
            face_idx = 4 # Right (+X)
            c_pos = Vector3(H, u.y / u.x * H, -u.z / u.x * H)
        else:
            face_idx = 5 # Left (-X)
            c_pos = Vector3(-H, u.y / abs_x * H, u.z / abs_x * H)
            
    return {"face": face_idx, "position": c_pos}

func _flatten_cube_face(face: int, c_pos: Vector3, H: float) -> Vector3:
    # Arrange faces in a 2D cross layout centered on Z=0
    # Face 2 (Front) is at (0,0)
    match face:
        2: # Front
            return Vector3(c_pos.x, c_pos.y, 0)
        4: # Right
            return Vector3(2.0 * H - c_pos.z, c_pos.y, 0)
        5: # Left
            return Vector3(-2.0 * H + c_pos.z, c_pos.y, 0)
        3: # Back
            return Vector3(4.0 * H - c_pos.x, c_pos.y, 0)
        0: # Top
            return Vector3(c_pos.x, 2.0 * H + c_pos.z, 0)
        1: # Bottom
            return Vector3(c_pos.x, -2.0 * H - c_pos.z, 0)
    return Vector3.ZERO

func _bv_to_color(bv: float) -> Color:
    if bv < 0.0:
        return Color("#9bb2ff").lerp(Color("#cbd9ff"), (bv + 0.4) / 0.4)
    elif bv < 0.4:
        return Color("#cbd9ff").lerp(Color("#fff4ea"), bv / 0.4)
    elif bv < 0.8:
        return Color("#fff4ea").lerp(Color("#fff2a3"), (bv - 0.4) / 0.4)
    elif bv < 1.4:
        return Color("#fff2a3").lerp(Color("#ffd2a1"), (bv - 0.8) / 0.6)
    else:
        return Color("#ffd2a1").lerp(Color("#ff9e85"), clamp((bv - 1.4) / 0.6, 0.0, 1.0))

func _process(delta):
    # 1. Animate Alphas of wireframes based on active mode
    sphere_grid_alpha = move_toward(sphere_grid_alpha, 1.0 if layout_type == 0 else 0.0, delta * transition_speed)
    flat_grid_alpha = move_toward(flat_grid_alpha, 1.0 if layout_type == 1 else 0.0, delta * transition_speed)
    cube_grid_alpha = move_toward(cube_grid_alpha, 1.0 if layout_type == 2 else 0.0, delta * transition_speed)
    
    _update_wireframe_materials()
    
    # 2. Update star positions & multimesh instances
    var mm = multimesh_instance.multimesh
    
    for i in range(star_count):
        var star = stars[i]
        
        # Decide target position
        var target_pos = star.sphere_pos
        if layout_type == 1:
            target_pos = star.flat_pos
        elif layout_type == 2:
            target_pos = star.cube_pos
            
        # Lerp position
        star.current_pos = star.current_pos.lerp(target_pos, delta * transition_speed)
        
        # Apply interactive filtering
        var is_visible = star.magnitude <= magnitude_cutoff and star.bv >= min_bv_cutoff and star.bv <= max_bv_cutoff
        
        # Build transform
        var t = Transform3D()
        if is_visible:
            # Base scale on magnitude (bright stars are larger)
            var size_factor = clamp(1.8 - (star.magnitude * 0.2), 0.3, 1.8)
            t = t.scaled(Vector3.ONE * size_factor)
            t.origin = star.current_pos
        else:
            # Hiding the instance by placing it at origin with 0 scale
            t = t.scaled(Vector3.ZERO)
            t.origin = Vector3.ZERO
            
        mm.set_instance_transform(i, t)
        mm.set_instance_color(i, star.color)

func _update_wireframe_materials():
    if sphere_grid_instance and sphere_grid_instance.material_override:
        sphere_grid_instance.material_override.albedo_color.a = sphere_grid_alpha * 0.3
    if cube_grid_instance and cube_grid_instance.material_override:
        cube_grid_instance.material_override.albedo_color.a = cube_grid_alpha * 0.3
    if flat_grid_instance and flat_grid_instance.material_override:
        flat_grid_instance.material_override.albedo_color.a = flat_grid_alpha * 0.3

# =====================================================================
# WIREFRAME GENERATORS
# =====================================================================

func _create_sphere_grid():
    sphere_grid_instance = MeshInstance3D.new()
    add_child(sphere_grid_instance)
    
    var imm = ImmediateMesh.new()
    sphere_grid_instance.mesh = imm
    
    var mat = StandardMaterial3D.new()
    mat.shading_mode = StandardMaterial3D.SHADING_MODE_UNSHADED
    mat.transparency = StandardMaterial3D.TRANSPARENCY_ALPHA
    mat.albedo_color = Color("#34CF00", 0.0) # Fade controlled by alpha
    mat.use_point_size = false
    sphere_grid_instance.material_override = mat
    
    imm.clear_surfaces()
    imm.surface_begin(Mesh.PRIMITIVE_LINES)
    
    var steps = 36
    # Latitude lines (Declination equivalent)
    for dec_deg in [-60, -30, 0, 30, 60]:
        var phi = deg_to_rad(dec_deg)
        var r = sphere_radius * cos(phi)
        var y = sphere_radius * sin(phi)
        for j in range(steps):
            var t1 = j * (2.0 * PI / steps)
            var t2 = (j + 1) * (2.0 * PI / steps)
            imm.surface_add_vertex(Vector3(r * cos(t1), y, r * sin(t1)))
            imm.surface_add_vertex(Vector3(r * cos(t2), y, r * sin(t2)))
            
    # Longitude lines (Right Ascension equivalent)
    for ra_hour in range(12):
        var theta = ra_hour * (2.0 * PI / 12.0)
        for j in range(steps):
            var p1 = -PI/2 + j * (PI / steps)
            var p2 = -PI/2 + (j + 1) * (PI / steps)
            imm.surface_add_vertex(Vector3(sphere_radius * cos(p1) * cos(theta), sphere_radius * sin(p1), sphere_radius * cos(p1) * sin(theta)))
            imm.surface_add_vertex(Vector3(sphere_radius * cos(p2) * cos(theta), sphere_radius * sin(p2), sphere_radius * cos(p2) * sin(theta)))
            
    imm.surface_end()

func _create_cube_grid():
    cube_grid_instance = MeshInstance3D.new()
    add_child(cube_grid_instance)
    
    var imm = ImmediateMesh.new()
    cube_grid_instance.mesh = imm
    
    var mat = StandardMaterial3D.new()
    mat.shading_mode = StandardMaterial3D.SHADING_MODE_UNSHADED
    mat.transparency = StandardMaterial3D.TRANSPARENCY_ALPHA
    mat.albedo_color = Color("#4FC3F7", 0.0)
    cube_grid_instance.material_override = mat
    
    var H = cube_size / 2.0
    
    imm.clear_surfaces()
    imm.surface_begin(Mesh.PRIMITIVE_LINES)
    
    # 12 edges of the 3D cube
    var vertices = [
        Vector3(-H, -H, -H), Vector3(H, -H, -H),
        Vector3(H, -H, -H), Vector3(H, H, -H),
        Vector3(H, H, -H), Vector3(-H, H, -H),
        Vector3(-H, H, -H), Vector3(-H, -H, -H),
        
        Vector3(-H, -H, H), Vector3(H, -H, H),
        Vector3(H, -H, H), Vector3(H, H, H),
        Vector3(H, H, H), Vector3(-H, H, H),
        Vector3(-H, H, H), Vector3(-H, -H, H),
        
        Vector3(-H, -H, -H), Vector3(-H, -H, H),
        Vector3(H, -H, -H), Vector3(H, -H, H),
        Vector3(H, H, -H), Vector3(H, H, H),
        Vector3(-H, H, -H), Vector3(-H, H, H)
    ]
    
    for v in vertices:
        imm.surface_add_vertex(v)
        
    imm.surface_end()

func _create_flat_grid():
    flat_grid_instance = MeshInstance3D.new()
    add_child(flat_grid_instance)
    
    var imm = ImmediateMesh.new()
    flat_grid_instance.mesh = imm
    
    var mat = StandardMaterial3D.new()
    mat.shading_mode = StandardMaterial3D.SHADING_MODE_UNSHADED
    mat.transparency = StandardMaterial3D.TRANSPARENCY_ALPHA
    mat.albedo_color = Color("#4FC3F7", 0.0)
    flat_grid_instance.material_override = mat
    
    var H = cube_size / 2.0
    
    imm.clear_surfaces()
    imm.surface_begin(Mesh.PRIMITIVE_LINES)
    
    # Flat 6-panel cross net outline on Z=0
    # Helper to draw a square on Z=0
    var draw_face_outline = func(center_x: float, center_y: float):
        imm.surface_add_vertex(Vector3(center_x - H, center_y - H, 0))
        imm.surface_add_vertex(Vector3(center_x + H, center_y - H, 0))
        
        imm.surface_add_vertex(Vector3(center_x + H, center_y - H, 0))
        imm.surface_add_vertex(Vector3(center_x + H, center_y + H, 0))
        
        imm.surface_add_vertex(Vector3(center_x + H, center_y + H, 0))
        imm.surface_add_vertex(Vector3(center_x - H, center_y + H, 0))
        
        imm.surface_add_vertex(Vector3(center_x - H, center_y + H, 0))
        imm.surface_add_vertex(Vector3(center_x - H, center_y - H, 0))
        
    # Draw the 6 faces in cross positions
    draw_face_outline.call(0.0, 0.0)         # Face 2: Front
    draw_face_outline.call(2.0 * H, 0.0)     # Face 4: Right
    draw_face_outline.call(-2.0 * H, 0.0)    # Face 5: Left
    draw_face_outline.call(4.0 * H, 0.0)     # Face 3: Back
    draw_face_outline.call(0.0, 2.0 * H)     # Face 0: Top
    draw_face_outline.call(0.0, -2.0 * H)    # Face 1: Bottom
    
    imm.surface_end()
