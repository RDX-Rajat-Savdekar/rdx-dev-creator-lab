import React, { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { Text } from '@react-three/drei';
import { ShaderMaterial, Mesh } from 'three';

interface CreativeSandboxProps {
  waveSpeed?: number;
  colorSpeed?: number;
  isKnot?: boolean;
}

export const Stage6_CreativeSandbox: React.FC<CreativeSandboxProps> = ({
  waveSpeed = 1.0,
  colorSpeed = 1.0,
  isKnot = true,
}) => {
  const shaderRef = useRef<ShaderMaterial>(null);
  const meshRef = useRef<Mesh>(null);

  // 1. Define custom shaders to demonstrate vertex coordinate deformation
  // and procedural pixel fragment color shifting.
  const customShader = {
    uniforms: {
      uTime: { value: 0 },
      uWaveSpeed: { value: 1.0 },
      uColorSpeed: { value: 1.0 },
    },
    vertexShader: `
      uniform float uTime;
      uniform float uWaveSpeed;
      varying vec2 vUv;
      varying vec3 vNormal;
      varying vec3 vPosition;

      void main() {
        vUv = uv;
        vNormal = normal;
        vPosition = position;

        // Animate a vertex displacement wave using sine functions
        vec3 pos = position;
        float displacement = sin(pos.y * 4.0 + uTime * uWaveSpeed * 2.5) * 0.15;
        pos += normal * displacement;

        gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
      }
    `,
    fragmentShader: `
      uniform float uTime;
      uniform float uColorSpeed;
      varying vec2 vUv;
      varying vec3 vNormal;
      varying vec3 vPosition;

      void main() {
        // Procedurally morph RGB values over time and coordinates
        float r = 0.5 + 0.5 * sin(uTime * uColorSpeed * 1.2 + vUv.x * 6.0);
        float g = 0.5 + 0.5 * sin(uTime * uColorSpeed * 1.8 + vUv.y * 4.0);
        float b = 0.5 + 0.5 * cos(uTime * uColorSpeed * 0.8 + (vUv.x + vUv.y) * 5.0);

        vec3 baseColor = vec3(r, g, b);

        // Simple Fresnel Rim Light Glow effect
        // Dot product between view direction (approx 0,0,1) and face normal
        float intensity = pow(1.0 - max(dot(vNormal, vec3(0.0, 0.0, 1.0)), 0.0), 3.0);
        vec3 rimColor = vec3(0.0, 0.9, 1.0); // neon cyan glow
        
        vec3 finalColor = mix(baseColor, rimColor, intensity * 0.6);

        gl_FragColor = vec4(finalColor, 1.0);
      }
    `,
  };

  // 2. Continuous frame loop updating uniforms and rotating mesh
  useFrame((state) => {
    const elapsed = state.clock.getElapsedTime();

    // Update shader uniforms
    if (shaderRef.current) {
      shaderRef.current.uniforms.uTime.value = elapsed;
      shaderRef.current.uniforms.uWaveSpeed.value = waveSpeed;
      shaderRef.current.uniforms.uColorSpeed.value = colorSpeed;
    }

    // Slow rotation of central mesh
    if (meshRef.current) {
      meshRef.current.rotation.y = elapsed * 0.4;
      meshRef.current.rotation.x = elapsed * 0.2;
    }
  });

  return (
    <group>
      <ambientLight intensity={0.5} />

      {/* 3D MSDF Text Label floating above mesh */}
      <Text
        position={[0, 2.2, 0]}
        fontSize={0.35}
        anchorX="center"
        anchorY="middle"
        outlineWidth={0.02}
        outlineColor="#00e5ff"
      >
        CUSTOM SHADERS
        <meshBasicMaterial color="#ffffff" />
      </Text>

      {/* Main Complex Geometry (Torus Knot or Torus Sphere) */}
      <mesh ref={meshRef} position={[0, -0.2, 0]}>
        {isKnot ? (
          <torusKnotGeometry args={[1.0, 0.35, 120, 16]} />
        ) : (
          <sphereGeometry args={[1.2, 64, 64]} />
        )}

        {/* Custom Shader Material */}
        <shaderMaterial
          ref={shaderRef}
          vertexShader={customShader.vertexShader}
          fragmentShader={customShader.fragmentShader}
          uniforms={customShader.uniforms}
          wireframe={false}
        />
      </mesh>

      {/* Wireframe overlay to visualize vertex shifts */}
      <mesh position={[0, -0.2, 0]} rotation={meshRef.current?.rotation}>
        {isKnot ? (
          <torusKnotGeometry args={[1.002, 0.352, 120, 16]} />
        ) : (
          <sphereGeometry args={[1.202, 32, 32]} />
        )}
        <meshBasicMaterial
          color="#ffffff"
          wireframe
          transparent
          opacity={0.06}
        />
      </mesh>
    </group>
  );
};
