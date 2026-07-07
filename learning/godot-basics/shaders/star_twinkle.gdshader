shader_type spatial;
render_mode unshaded, blend_add, depth_draw_never;

uniform float twinkle_speed = 3.0;
uniform float twinkle_intensity = 0.4;

varying vec3 v_pos;

void vertex() {
    v_pos = VERTEX;
    
    // Twinkle scale animation
    // Use vertex position coordinates to offset phase so they don't twinkle in sync
    float phase = dot(VERTEX, vec3(12.9898, 78.233, 45.164));
    float twinkle = sin(TIME * twinkle_speed + phase) * twinkle_intensity;
    
    // Scale the vertex slightly to create standard blinking size changes
    VERTEX *= (1.0 + twinkle);
}

void fragment() {
    // Read the vertex color (computed in script from B-V index)
    vec3 star_color = COLOR.rgb;
    
    // Smooth circle shape for the star billboard/quad
    vec2 center_uv = UV - vec2(0.5);
    float dist = length(center_uv);
    if (dist > 0.5) {
        discard;
    }
    
    // Glow effect towards the center
    float alpha = smoothstep(0.5, 0.0, dist);
    
    // Apply dynamic fade
    float phase = dot(v_pos, vec3(12.9898, 78.233, 45.164));
    float fade = 0.7 + 0.3 * cos(TIME * twinkle_speed * 1.5 + phase);
    
    ALBEDO = star_color;
    ALPHA = alpha * fade * COLOR.a;
}
