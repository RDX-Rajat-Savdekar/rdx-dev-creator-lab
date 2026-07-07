import React, { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { Group } from 'three';

export const Stage1_ServerRack: React.FC = () => {
  const groupRef = useRef<Group>(null);

  // Slow floating rotation
  useFrame((state) => {
    if (groupRef.current) {
      groupRef.current.rotation.y = Math.sin(state.clock.getElapsedTime() * 0.4) * 0.2;
      groupRef.current.position.y = Math.sin(state.clock.getElapsedTime() * 0.8) * 0.1;
    }
  });

  return (
    <group ref={groupRef} position={[0, 0, 0]}>
      {/* Ambient and local lights for realistic metallic shadowing */}
      <ambientLight intensity={0.4} />
      <pointLight position={[5, 5, 5]} intensity={1.5} color="#00e5ff" />
      <pointLight position={[-5, -5, -5]} intensity={0.5} color="#ff0077" />

      {/* Main Server Cabinet / Frame */}
      <mesh position={[0, 0, 0]}>
        <boxGeometry args={[2.2, 3.4, 1.8]} />
        <meshStandardMaterial 
          color="#0d0d18" 
          metalness={0.9} 
          roughness={0.15} 
          transparent
          opacity={0.95}
        />
      </mesh>

      {/* Outer Cabinet Frame Wireframe Highlight */}
      <mesh position={[0, 0, 0]}>
        <boxGeometry args={[2.22, 3.42, 1.82]} />
        <meshBasicMaterial 
          color="#00e5ff" 
          wireframe 
          transparent
          opacity={0.15}
        />
      </mesh>

      {/* Rack Blades (Units) */}
      {[0, 1, 2, 3, 4].map((index) => {
        const yOffset = -1.2 + index * 0.6;
        // Introduce a simulated active / faulty state
        const isFaulty = index === 1;
        const ledColor = isFaulty ? '#ff0055' : '#00ff66';

        return (
          <group key={index} position={[0, yOffset, 0]}>
            {/* Blade Faceplate */}
            <mesh position={[0, 0, 0.05]}>
              <boxGeometry args={[1.98, 0.45, 1.7]} />
              <meshStandardMaterial 
                color="#06060a" 
                metalness={0.95} 
                roughness={0.3} 
              />
            </mesh>

            {/* Glowing Status LED */}
            <mesh position={[-0.8, 0, 0.92]}>
              <sphereGeometry args={[0.04, 16, 16]} />
              <meshBasicMaterial color={ledColor} />
            </mesh>
            <pointLight 
              position={[-0.8, 0, 0.95]} 
              intensity={1.2} 
              distance={0.6} 
              color={ledColor} 
            />

            {/* Simulated Server Disk LED Array */}
            {[-0.5, -0.3, -0.1, 0.1, 0.3, 0.5].map((xOffset, i) => (
              <mesh key={i} position={[xOffset, 0, 0.92]}>
                <boxGeometry args={[0.08, 0.08, 0.02]} />
                <meshBasicMaterial 
                  color={Math.random() > 0.3 ? '#00e5ff' : '#042230'} 
                />
              </mesh>
            ))}
          </group>
        );
      })}
    </group>
  );
};
