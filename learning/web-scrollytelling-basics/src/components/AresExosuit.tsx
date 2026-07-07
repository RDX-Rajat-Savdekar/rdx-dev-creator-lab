import { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

interface AresExosuitProps {
  activeSection: number;
}

export function AresExosuit({ activeSection }: AresExosuitProps) {
  const suitGroup = useRef<THREE.Group>(null);
  const reactorRef = useRef<THREE.Mesh>(null);
  const leftRepulsorLight = useRef<THREE.PointLight>(null);
  const rightRepulsorLight = useRef<THREE.PointLight>(null);

  // Thruster particle data
  const particleCount = 40;
  const particles = useMemo(() => {
    const data = [];
    for (let i = 0; i < particleCount; i++) {
      data.push({
        yOffset: Math.random() * -1.5,
        speed: 1.5 + Math.random() * 2.0,
        xNoise: (Math.random() - 0.5) * 0.15,
        zNoise: (Math.random() - 0.5) * 0.15,
        scale: 0.05 + Math.random() * 0.06,
        isLeft: i < particleCount / 2,
      });
    }
    return data;
  }, []);

  const particleRefs = useRef<THREE.Mesh[]>([]);

  useFrame((state) => {
    const time = state.clock.getElapsedTime();

    // 1. Idle breathing rotation and subtle hover translation
    if (suitGroup.current) {
      suitGroup.current.rotation.y = Math.sin(time * 0.3) * 0.15;
      
      // Floating hover in propulsion stage (Stage 4 & 6)
      if (activeSection === 4 || activeSection === 6) {
        suitGroup.current.position.y = Math.sin(time * 2.0) * 0.12;
      } else {
        // Smoothly return to center
        suitGroup.current.position.y += (0 - suitGroup.current.position.y) * 0.05;
      }
    }

    // 2. Arc Reactor pulsing core
    if (reactorRef.current) {
      const pulse = 1.0 + Math.sin(time * 5.0) * 0.15;
      // In Section 2 (Core focus), make it pulse faster and brighter!
      const multiplier = activeSection === 2 ? 1.5 : 1.0;
      reactorRef.current.scale.set(pulse * multiplier, pulse * multiplier, 1);
    }

    // 3. Firing Hand Repulsors in propulsion stage
    const repulsorIntensity = activeSection === 4 ? 6.0 + Math.sin(time * 15.0) * 2.0 : 0.8;
    if (leftRepulsorLight.current) leftRepulsorLight.current.intensity = repulsorIntensity;
    if (rightRepulsorLight.current) rightRepulsorLight.current.intensity = repulsorIntensity;

    // 4. Animate Thruster Particles (Downwards flow)
    const isThrusterFiring = activeSection === 4 || activeSection === 6;
    particles.forEach((p, idx) => {
      const mesh = particleRefs.current[idx];
      if (!mesh) return;

      if (!isThrusterFiring) {
        mesh.visible = false;
        return;
      }

      mesh.visible = true;
      p.yOffset -= state.clock.getDelta() * p.speed;

      // Reset particle if it goes too low
      if (p.yOffset < -1.6) {
        p.yOffset = 0;
        p.xNoise = (Math.random() - 0.5) * 0.15;
        p.zNoise = (Math.random() - 0.5) * 0.15;
      }

      // Compute coordinate position based on boot nodes
      const bootX = p.isLeft ? -0.32 : 0.32;
      const bootY = -1.63;
      const bootZ = 0.18;

      mesh.position.set(
        bootX + p.xNoise,
        bootY + p.yOffset,
        bootZ + p.zNoise
      );

      // Fade out size as it flows down
      const scaleT = Math.max(0, 1 + p.yOffset / 1.6);
      mesh.scale.setScalar(p.scale * scaleT);
    });
  });

  // Materials system
  const paintMaterial = {
    color: '#a31010', // Dark Crimson
    metalness: 0.95,
    roughness: 0.12,
    clearcoat: 1.0,
    clearcoatRoughness: 0.1,
  };

  const goldMaterial = {
    color: '#d4982a', // Gold Alloy
    metalness: 0.90,
    roughness: 0.15,
  };

  const jointMaterial = {
    color: '#1e293b', // Gunmetal Grey
    metalness: 0.8,
    roughness: 0.4,
  };

  const glowMaterial = {
    color: '#00ffff',
    emissive: '#00e5ff',
    emissiveIntensity: 3.0,
  };

  const fireMaterial = {
    color: '#ff6600',
    emissive: '#ff3300',
    emissiveIntensity: 4.0,
  };

  return (
    <group ref={suitGroup}>
      {/* Ambient Lighting tailored for exosuite */}
      <ambientLight intensity={0.5} />
      <directionalLight position={[5, 5, 5]} intensity={5.0} color="#ffffff" />
      <directionalLight position={[-5, 5, -5]} intensity={2.0} color="#ff0044" />
      <pointLight position={[0, 0, 3]} intensity={1.5} color="#00ffff" distance={5} />

      {/* 🛡️ CHEST / TORSO */}
      <group position={[0, 0.4, 0]}>
        {/* Main Chest Plate */}
        <mesh>
          <boxGeometry args={[0.9, 1.1, 0.6]} />
          <meshPhysicalMaterial {...paintMaterial} />
        </mesh>
        {/* Collar Collar armor */}
        <mesh position={[0, 0.6, 0.05]}>
          <boxGeometry args={[0.7, 0.15, 0.55]} />
          <meshPhysicalMaterial {...paintMaterial} />
        </mesh>
        {/* Gold Chest highlights */}
        <mesh position={[-0.26, 0.2, 0.31]}>
          <boxGeometry args={[0.2, 0.5, 0.05]} />
          <meshPhysicalMaterial {...goldMaterial} />
        </mesh>
        <mesh position={[0.26, 0.2, 0.31]}>
          <boxGeometry args={[0.2, 0.5, 0.05]} />
          <meshPhysicalMaterial {...goldMaterial} />
        </mesh>

        {/* ⚛️ ARC REACTOR POWER CORE */}
        <group position={[0, 0.25, 0.31]}>
          {/* Reactor Inner Glow Core */}
          <mesh ref={reactorRef} rotation={[Math.PI / 2, 0, 0]}>
            <cylinderGeometry args={[0.18, 0.18, 0.04, 32]} />
            <meshStandardMaterial {...glowMaterial} />
          </mesh>
          {/* Reactor Outer Ring border */}
          <mesh position={[0, 0, -0.01]} rotation={[Math.PI / 2, 0, 0]}>
            <cylinderGeometry args={[0.22, 0.22, 0.03, 32]} />
            <meshStandardMaterial color="#020617" roughness={0.5} metalness={0.9} />
          </mesh>
          <pointLight position={[0, 0, 0.1]} intensity={3.5} color="#00ffff" distance={3} />
        </group>
      </group>

      {/* 🪖 HELMET / HEAD */}
      <group position={[0, 1.25, 0]}>
        {/* Helmet base */}
        <mesh>
          <sphereGeometry args={[0.34, 32, 32]} />
          <meshPhysicalMaterial {...paintMaterial} />
        </mesh>
        {/* Gold Faceplate */}
        <mesh position={[0, 0.04, 0.08]} scale={[1, 1.1, 1]}>
          <sphereGeometry args={[0.31, 32, 32]} />
          <meshPhysicalMaterial {...goldMaterial} />
        </mesh>
        {/* Red Helmet Crown detail */}
        <mesh position={[0, 0.2, 0.05]}>
          <boxGeometry args={[0.16, 0.12, 0.32]} />
          <meshPhysicalMaterial {...paintMaterial} />
        </mesh>

        {/* 👁️ VISOR SLIT HUD */}
        <mesh position={[0, 0.08, 0.29]}>
          <boxGeometry args={[0.26, 0.035, 0.08]} />
          <meshStandardMaterial
            color={activeSection === 3 ? '#ff003c' : '#00ffff'}
            emissive={activeSection === 3 ? '#ff0000' : '#00e5ff'}
            emissiveIntensity={4.0}
          />
        </mesh>
      </group>

      {/* 💪 UPPER LIMBS (SHOULDERS & ARMS) */}
      {/* Left Arm */}
      <group position={[-0.62, 0.75, 0]}>
        {/* Upper Arm shoulder */}
        <mesh>
          <sphereGeometry args={[0.22, 16, 16]} />
          <meshPhysicalMaterial {...paintMaterial} />
        </mesh>
        {/* Joint */}
        <mesh position={[0, -0.15, 0]}>
          <sphereGeometry args={[0.12, 16, 16]} />
          <meshStandardMaterial {...jointMaterial} />
        </mesh>
        {/* Bicep (Red Metallic) */}
        <mesh position={[-0.08, -0.38, 0.1]}>
          <cylinderGeometry args={[0.11, 0.09, 0.45, 16]} />
          <meshPhysicalMaterial {...paintMaterial} />
        </mesh>
        {/* Forearm (Raised defensive pose) */}
        <group position={[-0.08, -0.6, 0.1]}>
          <mesh position={[-0.05, 0.15, 0.28]} rotation={[Math.PI / 3, 0, 0]}>
            <cylinderGeometry args={[0.09, 0.07, 0.45, 16]} />
            <meshPhysicalMaterial {...paintMaterial} />
          </mesh>
          {/* Left Palm Repulsor Node */}
          <group position={[-0.05, 0.32, 0.45]}>
            <mesh>
              <sphereGeometry args={[0.08, 16, 16]} />
              <meshPhysicalMaterial {...goldMaterial} />
            </mesh>
            <mesh position={[0, 0, 0.04]} rotation={[Math.PI / 2, 0, 0]}>
              <cylinderGeometry args={[0.045, 0.045, 0.01, 16]} />
              <meshStandardMaterial color="#ffffff" emissive="#00ffff" emissiveIntensity={3.0} />
            </mesh>
            <pointLight ref={leftRepulsorLight} position={[0, 0, 0.15]} intensity={1} color="#00ffff" distance={2} />
          </group>
        </group>
      </group>

      {/* Right Arm */}
      <group position={[0.62, 0.75, 0]}>
        {/* Upper Arm shoulder */}
        <mesh>
          <sphereGeometry args={[0.22, 16, 16]} />
          <meshPhysicalMaterial {...paintMaterial} />
        </mesh>
        {/* Joint */}
        <mesh position={[0, -0.15, 0]}>
          <sphereGeometry args={[0.12, 16, 16]} />
          <meshStandardMaterial {...jointMaterial} />
        </mesh>
        {/* Bicep */}
        <mesh position={[0.08, -0.38, 0.1]}>
          <cylinderGeometry args={[0.11, 0.09, 0.45, 16]} />
          <meshPhysicalMaterial {...paintMaterial} />
        </mesh>
        {/* Forearm (Raised defensive pose) */}
        <group position={[0.08, -0.6, 0.1]}>
          <mesh position={[0.05, 0.15, 0.28]} rotation={[Math.PI / 3, 0, 0]}>
            <cylinderGeometry args={[0.09, 0.07, 0.45, 16]} />
            <meshPhysicalMaterial {...paintMaterial} />
          </mesh>
          {/* Right Palm Repulsor Node */}
          <group position={[0.05, 0.32, 0.45]}>
            <mesh>
              <sphereGeometry args={[0.08, 16, 16]} />
              <meshPhysicalMaterial {...goldMaterial} />
            </mesh>
            <mesh position={[0, 0, 0.04]} rotation={[Math.PI / 2, 0, 0]}>
              <cylinderGeometry args={[0.045, 0.045, 0.01, 16]} />
              <meshStandardMaterial color="#ffffff" emissive="#00ffff" emissiveIntensity={3.0} />
            </mesh>
            <pointLight ref={rightRepulsorLight} position={[0, 0, 0.15]} intensity={1} color="#00ffff" distance={2} />
          </group>
        </group>
      </group>

      {/* 🦵 LOWER LIMBS (LEGS & BOOTS) */}
      {/* Left Leg */}
      <group position={[-0.32, -0.3, 0]}>
        {/* Hip Joint */}
        <mesh>
          <sphereGeometry args={[0.14, 16, 16]} />
          <meshStandardMaterial {...jointMaterial} />
        </mesh>
        {/* Thigh */}
        <mesh position={[0, -0.45, 0]}>
          <cylinderGeometry args={[0.14, 0.11, 0.6, 16]} />
          <meshPhysicalMaterial {...paintMaterial} />
        </mesh>
        {/* Knee Guard */}
        <mesh position={[0, -0.78, 0.08]}>
          <sphereGeometry args={[0.1, 16, 16]} />
          <meshPhysicalMaterial {...goldMaterial} />
        </mesh>
        {/* Shin & Calf */}
        <mesh position={[0, -1.15, 0.05]}>
          <cylinderGeometry args={[0.11, 0.09, 0.7, 16]} />
          <meshPhysicalMaterial {...paintMaterial} />
        </mesh>
        {/* Boot foot */}
        <mesh position={[0, -1.56, 0.18]}>
          <boxGeometry args={[0.18, 0.13, 0.38]} />
          <meshPhysicalMaterial {...paintMaterial} />
        </mesh>
        {/* Boot Thruster Ring Base */}
        <mesh position={[0, -1.63, 0.12]} rotation={[Math.PI / 2, 0, 0]}>
          <torusGeometry args={[0.1, 0.02, 8, 32]} />
          <meshStandardMaterial color="#fca5a5" emissive="#ff3300" emissiveIntensity={1.5} />
        </mesh>
      </group>

      {/* Right Leg */}
      <group position={[0.32, -0.3, 0]}>
        {/* Hip Joint */}
        <mesh>
          <sphereGeometry args={[0.14, 16, 16]} />
          <meshStandardMaterial {...jointMaterial} />
        </mesh>
        {/* Thigh */}
        <mesh position={[0, -0.45, 0]}>
          <cylinderGeometry args={[0.14, 0.11, 0.6, 16]} />
          <meshPhysicalMaterial {...paintMaterial} />
        </mesh>
        {/* Knee Guard */}
        <mesh position={[0, -0.78, 0.08]}>
          <sphereGeometry args={[0.1, 16, 16]} />
          <meshPhysicalMaterial {...goldMaterial} />
        </mesh>
        {/* Shin & Calf */}
        <mesh position={[0, -1.15, 0.05]}>
          <cylinderGeometry args={[0.11, 0.09, 0.7, 16]} />
          <meshPhysicalMaterial {...paintMaterial} />
        </mesh>
        {/* Boot foot */}
        <mesh position={[0, -1.56, 0.18]}>
          <boxGeometry args={[0.18, 0.13, 0.38]} />
          <meshPhysicalMaterial {...paintMaterial} />
        </mesh>
        {/* Boot Thruster Ring Base */}
        <mesh position={[0, -1.63, 0.12]} rotation={[Math.PI / 2, 0, 0]}>
          <torusGeometry args={[0.1, 0.02, 8, 32]} />
          <meshStandardMaterial color="#fca5a5" emissive="#ff3300" emissiveIntensity={1.5} />
        </mesh>
      </group>

      {/* 🔥 FLIGHT THRUSTER DUST PARTICLES */}
      {particles.map((_, idx) => (
        <mesh
          key={idx}
          ref={(el) => {
            if (el) particleRefs.current[idx] = el;
          }}
        >
          <sphereGeometry args={[1, 8, 8]} />
          <meshBasicMaterial color="#ff5500" transparent opacity={0.6} />
        </mesh>
      ))}
    </group>
  );
}
