import React, { useRef, useState } from 'react';
import { useFrame } from '@react-three/fiber';
import { Group, Mesh } from 'three';

interface DatabaseNodeProps {
  position: [number, number, number];
  isPrimary: boolean;
  name: string;
}

const DatabaseNode: React.FC<DatabaseNodeProps> = ({ position, isPrimary, name }) => {
  const meshRef = useRef<Mesh>(null);
  const [hovered, setHovered] = useState(false);

  // Smooth hover bounce effect
  useFrame((state) => {
    if (meshRef.current) {
      const targetY = hovered ? 0.3 : 0;
      meshRef.current.position.y = meshRef.current.position.y + (targetY - meshRef.current.position.y) * 0.2;

      // Gentle spin
      meshRef.current.rotation.y += 0.01;
    }
  });

  const nodeColor = isPrimary ? '#00ff66' : '#bd00ff';

  return (
    <group position={position}>
      {/* Database Cylinder Stack */}
      <mesh
        ref={meshRef}
        onPointerOver={() => setHovered(true)}
        onPointerOut={() => setHovered(false)}
      >
        <cylinderGeometry args={[0.45, 0.45, 1.2, 32]} />
        <meshStandardMaterial
          color={hovered ? '#ffffff' : nodeColor}
          metalness={0.8}
          roughness={0.2}
          emissive={hovered ? nodeColor : '#000000'}
          emissiveIntensity={hovered ? 0.8 : 0}
        />
      </mesh>

      {/* Segment lines indicating DB disk platters */}
      <mesh position={[0, 0.2, 0]}>
        <cylinderGeometry args={[0.46, 0.46, 0.04, 32]} />
        <meshBasicMaterial color="#07070d" />
      </mesh>
      <mesh position={[0, -0.2, 0]}>
        <cylinderGeometry args={[0.46, 0.46, 0.04, 32]} />
        <meshBasicMaterial color="#07070d" />
      </mesh>

      {/* Ring base glow */}
      <mesh position={[0, -0.62, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <torusGeometry args={[0.55, 0.03, 16, 64]} />
        <meshBasicMaterial color={nodeColor} transparent opacity={hovered ? 1.0 : 0.4} />
      </mesh>
      <pointLight
        position={[0, -0.5, 0]}
        intensity={hovered ? 1.5 : 0.4}
        color={nodeColor}
        distance={1.5}
      />
    </group>
  );
};

export const Stage3_DatabaseRing: React.FC = () => {
  const clusterRef = useRef<Group>(null);
  const radius = 2.8;
  const dbNodes = [
    { name: 'PRIMARY-01', isPrimary: true },
    { name: 'REPLICA-01', isPrimary: false },
    { name: 'REPLICA-02', isPrimary: false },
    { name: 'REPLICA-03', isPrimary: false },
    { name: 'REPLICA-04', isPrimary: false },
  ];

  // Rotate the entire cluster slowly
  useFrame((state, delta) => {
    if (clusterRef.current) {
      clusterRef.current.rotation.y += delta * 0.4;
    }
  });

  return (
    <group ref={clusterRef}>
      <ambientLight intensity={0.3} />
      <directionalLight position={[10, 10, 5]} intensity={0.7} color="#ffffff" />

      {/* Large central connecting loop ring */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.6, 0]}>
        <torusGeometry args={[radius, 0.015, 8, 100]} />
        <meshBasicMaterial color="rgba(255, 255, 255, 0.08)" />
      </mesh>

      {/* Project nodes in a circle */}
      {dbNodes.map((node, index) => {
        const angle = (index * 2 * Math.PI) / dbNodes.length;
        const x = Math.cos(angle) * radius;
        const z = Math.sin(angle) * radius;
        return (
          <DatabaseNode
            key={index}
            position={[x, 0.1, z]}
            isPrimary={node.isPrimary}
            name={node.name}
          />
        );
      })}
    </group>
  );
};
