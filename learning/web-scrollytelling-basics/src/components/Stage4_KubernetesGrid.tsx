import React, { useRef, useState } from 'react';
import { useFrame } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import { Group, Mesh, Vector3 } from 'three';
import * as THREE from 'three';

interface Pod {
  id: string;
  r: number;
  c: number;
  ip: string;
  cpu: string;
  status: string;
}

interface KubernetesGridProps {
  onPodSelect?: (pod: Pod | null) => void;
}

export const Stage4_KubernetesGrid: React.FC<KubernetesGridProps> = ({ onPodSelect }) => {
  const gridRef = useRef<Group>(null);
  const controlsRef = useRef<any>(null);

  const [selectedPod, setSelectedPod] = useState<Pod | null>(null);

  const pods: Pod[] = [];
  for (let r = -1; r <= 1; r++) {
    for (let c = -1; c <= 1; c++) {
      const idx = (r + 1) * 3 + (c + 2);
      pods.push({
        id: `pod-0${idx}`,
        r,
        c,
        ip: `10.244.1.${12 + idx}`,
        cpu: `${Math.floor(10 + Math.random() * 30)}%`,
        status: idx === 5 ? 'TERMINATING' : 'RUNNING',
      });
    }
  }

  // Camera targets for smooth lerping
  const targetCamPos = useRef(new Vector3(0, 0, 7.5));
  const targetLookAt = useRef(new Vector3(0, 0, 0));

  useFrame((state) => {
    // Smoothly interpolate camera position
    state.camera.position.lerp(targetCamPos.current, 0.08);

    // Smoothly interpolate OrbitControls target
    if (controlsRef.current) {
      controlsRef.current.target.lerp(targetLookAt.current, 0.08);
      controlsRef.current.update();
    }
  });

  const handlePodClick = (pod: Pod) => {
    if (selectedPod?.id === pod.id) {
      // Deselect -> Reset Camera to center view
      setSelectedPod(null);
      targetCamPos.current.set(0, 0, 7.5);
      targetLookAt.current.set(0, 0, 0);
      if (onPodSelect) onPodSelect(null);
    } else {
      // Select Pod -> Move camera closer and shift controls target to pod position
      setSelectedPod(pod);
      targetCamPos.current.set(pod.c * 2.2, pod.r * 2.2, 3.5);
      targetLookAt.current.set(pod.c * 2.2, pod.r * 2.2, 0);
      if (onPodSelect) onPodSelect(pod);
    }
  };

  return (
    <group ref={gridRef}>
      {/* OrbitControls to allow manual panning, but programmatically driven on click */}
      <OrbitControls 
        ref={controlsRef} 
        enableDamping 
        dampingFactor={0.05}
        maxPolarAngle={Math.PI / 2 + 0.1}
        minDistance={2}
        maxDistance={12}
      />

      <ambientLight intensity={0.65} />
      <directionalLight position={[0, 0, 10]} intensity={1.5} color="#ffffff" />
      <pointLight position={[-5, -5, 5]} intensity={0.8} color="#bd00ff" />

      {/* Grid Floor Mesh */}
      <gridHelper args={[15, 15, '#3f3f5c', '#1c1c2e']} position={[0, -2.5, 0]} />

      {/* Render 3x3 array of pods */}
      {pods.map((pod) => {
        const isSelected = selectedPod?.id === pod.id;
        const x = pod.c * 2.2;
        const y = pod.r * 2.2;

        return (
          <PodItem
            key={pod.id}
            pod={pod}
            x={x}
            y={y}
            isSelected={isSelected}
            onClick={() => handlePodClick(pod)}
          />
        );
      })}
    </group>
  );
};

interface PodItemProps {
  pod: Pod;
  x: number;
  y: number;
  isSelected: boolean;
  onClick: () => void;
}

const PodItem: React.FC<PodItemProps> = ({ pod, x, y, isSelected, onClick }) => {
  const meshRef = useRef<Mesh>(null);
  const [hovered, setHovered] = useState(false);

  // Status-driven color scheme
  let activeColor = '#00e5ff'; // cyan
  if (pod.status === 'TERMINATING') {
    activeColor = '#ffea00'; // yellow
  } else if (isSelected) {
    activeColor = '#00ff66'; // neon green
  }

  // Float up and down inside useFrame
  useFrame((state) => {
    if (meshRef.current) {
      const floatVal = Math.sin(state.clock.getElapsedTime() * 2 + (pod.r + pod.c)) * 0.05;
      meshRef.current.position.y = y + floatVal;
      
      // Rotate selected pod
      if (isSelected) {
        meshRef.current.rotation.y += 0.02;
        meshRef.current.rotation.x += 0.01;
      } else {
        // Return to flat rotation
        meshRef.current.rotation.y += (0 - meshRef.current.rotation.y) * 0.1;
        meshRef.current.rotation.x += (0 - meshRef.current.rotation.x) * 0.1;
      }
    }
  });

  return (
    <group position={[x, y, 0]}>
      {/* Main Cube Pod */}
      <mesh
        ref={meshRef}
        onPointerOver={() => {
          document.body.style.cursor = 'pointer';
          setHovered(true);
        }}
        onPointerOut={() => {
          document.body.style.cursor = 'auto';
          setHovered(false);
        }}
        onClick={onClick}
      >
        <boxGeometry args={[0.8, 0.8, 0.8]} />
        <meshStandardMaterial
          color={isSelected ? '#00ff66' : hovered ? '#00e5ff' : '#616a94'}
          metalness={0.15}
          roughness={0.4}
          emissive={isSelected ? '#002208' : hovered ? '#002230' : '#1c1f30'}
        />
      </mesh>

      {/* Wireframe outer container highlighting bounds */}
      <mesh position={[0, 0, 0]}>
        <boxGeometry args={[0.9, 0.9, 0.9]} />
        <meshBasicMaterial 
          color={activeColor} 
          wireframe 
          transparent
          opacity={isSelected || hovered ? 0.8 : 0.3}
        />
      </mesh>

      {/* Glowing point light inside selected/hovered nodes */}
      {(isSelected || hovered) && (
        <pointLight 
          position={[0, 0, 0]} 
          intensity={1.2} 
          distance={1.5} 
          color={activeColor} 
        />
      )}
    </group>
  );
};
