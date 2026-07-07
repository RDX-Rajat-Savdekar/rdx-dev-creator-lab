import React, { useRef, useState } from 'react';
import { useFrame } from '@react-three/fiber';
import { Group, Mesh, Vector3 } from 'three';

interface LoadBalancerProps {
  onInteraction?: (clicked: boolean, hovered: boolean) => void;
}

export const Stage2_LoadBalancer: React.FC<LoadBalancerProps> = ({ onInteraction }) => {
  const groupRef = useRef<Group>(null);
  const coreRef = useRef<Mesh>(null);
  const ring1Ref = useRef<Mesh>(null);
  const ring2Ref = useRef<Mesh>(null);

  const [hovered, setHovered] = useState(false);
  const [clicked, setClicked] = useState(false);

  // Animating rotation and interpolating scale
  useFrame((state, delta) => {
    // 1. Slow rotation
    if (coreRef.current) {
      coreRef.current.rotation.y += delta * 0.4;
      coreRef.current.rotation.x += delta * 0.2;
    }
    if (ring1Ref.current) {
      ring1Ref.current.rotation.x += delta * 0.8;
      ring1Ref.current.rotation.y += delta * 0.4;
    }
    if (ring2Ref.current) {
      ring2Ref.current.rotation.y -= delta * 0.6;
      ring2Ref.current.rotation.z += delta * 0.9;
    }

    // 2. Smooth scale lerp (physic-like spring transition)
    if (groupRef.current) {
      const targetScale = clicked ? 1.3 : 1.0;
      const currentScale = groupRef.current.scale.x;
      const lerpedScale = currentScale + (targetScale - currentScale) * 0.15;
      groupRef.current.scale.set(lerpedScale, lerpedScale, lerpedScale);
    }
  });

  const handlePointerOver = () => {
    setHovered(true);
    if (onInteraction) onInteraction(clicked, true);
  };

  const handlePointerOut = () => {
    setHovered(false);
    if (onInteraction) onInteraction(clicked, false);
  };

  const handleClick = () => {
    const nextClicked = !clicked;
    setClicked(nextClicked);
    if (onInteraction) onInteraction(nextClicked, hovered);
  };

  return (
    <group ref={groupRef}>
      <ambientLight intensity={0.3} />
      <directionalLight position={[5, 10, 5]} intensity={1.0} color="#00e5ff" />

      {/* Outer Glow Point Light */}
      <pointLight 
        position={[0, 0, 0]} 
        intensity={hovered ? 2.5 : 1.2} 
        color={hovered ? '#ff0077' : '#00e5ff'} 
        distance={4}
      />

      {/* Main Core Node Sphere */}
      <mesh
        ref={coreRef}
        onPointerOver={handlePointerOver}
        onPointerOut={handlePointerOut}
        onClick={handleClick}
        style={{ cursor: 'pointer' }}
      >
        <sphereGeometry args={[0.9, 32, 32]} />
        <meshStandardMaterial
          color={hovered ? '#ff0077' : '#00e5ff'}
          roughness={0.1}
          metalness={0.9}
          emissive={hovered ? '#550022' : '#003344'}
        />
      </mesh>

      {/* Orbital Ring 1 */}
      <mesh ref={ring1Ref}>
        <torusGeometry args={[1.4, 0.04, 16, 100]} />
        <meshStandardMaterial 
          color={clicked ? '#bd00ff' : '#00ff66'} 
          metalness={0.8}
          roughness={0.2}
        />
      </mesh>

      {/* Orbital Ring 2 */}
      <mesh ref={ring2Ref}>
        <torusGeometry args={[1.65, 0.02, 12, 100]} />
        <meshStandardMaterial 
          color="#ffffff" 
          metalness={0.9}
          roughness={0.1}
          transparent
          opacity={0.6}
        />
      </mesh>
    </group>
  );
};
