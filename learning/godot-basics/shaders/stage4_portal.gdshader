shader_type spatial;
render_mode unshaded, blend_add, cull_disabled, depth_draw_never;

uniform vec4 portal_color : source_color = vec4(0.0, 0.8, 1.0, 1.0);
uniform float ripple_speed = 4.0;
uniform float ripple_frequency = 5.0;
uniform float ripple_amplitude = 0.15;
uniform float swirl_speed = 2.0;

varying vec3 v_vertex;
varying vec2 v_uv;

// Simple procedural noise helper
float hash(vec2 p) {
    return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453123);
}

float noise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    f = f * f * (3.0 - 2.0 * f);
    return mix(mix(hash(i + vec2(0.0,0.0)), hash(i + vec2(1.0,0.0)), f.x),
               mix(hash(i + vec2(0.0,1.0)), hash(i + vec2(1.0,1.0)), f.x), f.y);
}

void vertex() {
    v_vertex = VERTEX;
    v_uv = UV;
    
    // Deform vertices along normal using sine waves
    // Creating ruffling waves around the ring
    float angle = atan2(VERTEX.x, VERTEX.z);
    float wave = sin(angle * ripple_frequency + TIME * ripple_speed) * ripple_amplitude;
    VERTEX += NORMAL * wave;
}

void fragment() {
    // 1. Swirling pattern inside UV coordinates
    // Convert UV to polar coordinates from center
    vec2 uv_center = v_uv - vec2(0.5);
    float dist = length(uv_center);
    float angle = atan2(uv_center.y, uv_center.x);
    
    // Create bands of energy swirling around the center
    float radial_pattern = sin(angle * 6.0 - dist * 15.0 + TIME * swirl_speed);
    
    // Ring falloff: only visible within a band
    // Outer edge is dist=0.5, inner edge is dist=0.2
    float ring = smoothstep(0.5, 0.45, dist) * smoothstep(0.2, 0.3, dist);
    
    // Procedural turbulence noise
    float n = noise(vec2(angle * 3.0, dist * 20.0 - TIME * ripple_speed * 0.5));
    
    // Combine patterns
    float energy = (radial_pattern * 0.4 + n * 0.6) * ring;
    
    // Fresnel Rim Glow
    // Facing direction: dot product between VIEW and NORMAL
    // Cull disabled means we see both sides
    float fresnel = pow(1.0 - abs(dot(NORMAL, VIEW)), 2.5);
    
    vec3 final_color = portal_color.rgb * (energy * 1.5 + fresnel * 0.8);
    float final_alpha = (energy * 0.8 + fresnel * 0.5) * portal_color.a;
    
    ALBEDO = final_color;
    ALPHA = clamp(final_alpha, 0.0, 1.0);
}
