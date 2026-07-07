import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import { Group, Vector3, Mesh } from 'three';

interface Packet {
  id: number;
  progress: number; // 0 to 3
  path: 0 | 1;      // Server A path or Server B path
  speed: number;
}

export const Stage5_TrafficFlow: React.FC = () => {
  const groupRef = useRef<Group>(null);
  
  // 1. Coordinates of structural network nodes
  const ingressPos = useMemo(() => new Vector3(-4, 1.8, 0), []);
  const lbPos = useMemo(() => new Vector3(-1, 0, 0), []);
  const serverAPos = useMemo(() => new Vector3(2, 1.3, 0), []);
  const serverBPos = useMemo(() => new Vector3(2, -1.3, 0), []);
  const dbPos = useMemo(() => new Vector3(5, 0, 0), []);

  // 2. Active packets running concurrently
  const packets = useRef<Packet[]>([
    { id: 1, progress: 0, path: 0, speed: 0.65 },
    { id: 2, progress: 1.0, path: 1, speed: 0.55 },
    { id: 3, progress: 2.0, path: 0, speed: 0.70 },
  ]);

  // Keep references to packet meshes to update coordinates directly in useFrame
  const packetMeshRefs = useRef<(Mesh | null)[]>([]);

  useFrame((state, delta) => {
    // Animate structural nodes (gentle float)
    if (groupRef.current) {
      groupRef.current.position.y = Math.sin(state.clock.getElapsedTime() * 0.5) * 0.05;
    }

    // Process and translate traffic packets along connection nodes
    packets.current.forEach((packet, index) => {
      packet.progress += delta * packet.speed;

      // Recycle packet if it reaches the database destination
      if (packet.progress >= 3.0) {
        packet.progress = 0;
        packet.path = Math.random() > 0.5 ? 0 : 1; // pick random worker route
      }

      const mesh = packetMeshRefs.current[index];
      if (!mesh) return;

      const p = packet.progress;
      const targetServer = packet.path === 0 ? serverAPos : serverBPos;

      if (p < 1.0) {
        // Segment 0: Ingress Gateway -> Load Balancer
        mesh.position.lerpVectors(ingressPos, lbPos, p);
      } else if (p < 2.0) {
        // Segment 1: Load Balancer -> Server Node
        const t = p - 1.0;
        mesh.position.lerpVectors(lbPos, targetServer, t);
      } else {
        // Segment 2: Server Node -> Database Ring
        const t = p - 2.0;
        mesh.position.lerpVectors(targetServer, dbPos, t);
      }
    });
  });

  return (
    <group ref={groupRef}>
      <ambientLight intensity={0.35} />
      <directionalLight position={[10, 10, 5]} intensity={0.8} color="#ffffff" />
      <pointLight position={[0, 0, 3]} intensity={0.5} color="#00e5ff" />

      {/* Network cabling lines between node endpoints */}
      <ConnectionLine start={ingressPos} end={lbPos} color="#ff0077" />
      <ConnectionLine start={lbPos} end={serverAPos} color="#00e5ff" />
      <ConnectionLine start={lbPos} end={serverBPos} color="#00e5ff" />
      <ConnectionLine start={serverAPos} end={dbPos} color="#bd00ff" />
      <ConnectionLine start={serverBPos} end={dbPos} color="#bd00ff" />

      {/* INGRESS GATEWAY (Left Box) */}
      <group position={ingressPos}>
        <mesh>
          <boxGeometry args={[0.8, 0.8, 0.8]} />
          <meshStandardMaterial color="#ff0077" metalness={0.9} roughness={0.15} />
        </mesh>
        <mesh>
          <boxGeometry args={[0.9, 0.9, 0.9]} />
          <meshBasicMaterial color="#ff0077" wireframe transparent opacity={0.2} />
        </mesh>
      </group>

      {/* LOAD BALANCER (Center Sphere) */}
      <group position={lbPos}>
        <mesh>
          <sphereGeometry args={[0.55, 32, 32]} />
          <meshStandardMaterial color="#00e5ff" metalness={0.9} roughness={0.1} />
        </mesh>
      </group>

      {/* SERVER WORKER NODES (Middle Boxes) */}
      <group position={serverAPos}>
        <mesh>
          <boxGeometry args={[0.7, 0.5, 0.7]} />
          <meshStandardMaterial color="#00ff66" metalness={0.8} roughness={0.2} />
        </mesh>
      </group>
      <group position={serverBPos}>
        <mesh>
          <boxGeometry args={[0.7, 0.5, 0.7]} />
          <meshStandardMaterial color="#00ff66" metalness={0.8} roughness={0.2} />
        </mesh>
      </group>

      {/* DATABASE NODE (Right Cylinder) */}
      <group position={dbPos}>
        <mesh>
          <cylinderGeometry args={[0.4, 0.4, 0.8, 32]} />
          <meshStandardMaterial color="#bd00ff" metalness={0.8} roughness={0.2} />
        </mesh>
      </group>

      {/* Render Traffic Particle Spheres */}
      {packets.current.map((packet, index) => (
        <mesh
          key={packet.id}
          ref={(el) => (packetMeshRefs.current[index] = el)}
        >
          <sphereGeometry args={[0.1, 16, 16]} />
          <meshBasicMaterial color="#ffffff" />
          <pointLight intensity={1.5} distance={0.6} color="#ffffff" />
        </mesh>
      ))}
    </group>
  );
};

interface ConnectionLineProps {
  start: Vector3;
  end: Vector3;
  color: string;
}

const ConnectionLine: React.FC<ConnectionLineProps> = ({ start, end, color }) => {
  const points = useMemo(() => [start, end], [start, end]);
  return (
    <line>
      <bufferGeometry attach="geometry">
        <float32BufferAttribute
          attach="attributes-position"
          args={[new Float32Array([start.x, start.y, start.z, end.x, end.y, end.z]), 3]}
        />
      </bufferGeometry>
      <lineBasicMaterial color={color} transparent opacity={0.3} linewidth={2} />
    </line>
  );
};
