import { useRef, useState } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import { Text } from '@react-three/drei';

interface CacheValidationProps {
  manualMode?: 'HIT' | 'MISS' | 'VALIDATION' | null;
}

export function Stage7_CacheValidation({ manualMode = null }: CacheValidationProps) {
  const clientPos = new THREE.Vector3(-2.8, 0, 0);
  const cachePos = new THREE.Vector3(0, 1.2, 0);
  const dbPos = new THREE.Vector3(2.8, -0.5, 0);

  const packetRef = useRef<THREE.Group>(null);
  const cacheOutlineRef = useRef<THREE.Mesh>(null);
  const dbRef = useRef<THREE.Group>(null);

  // Simulation state
  const [simType, setSimType] = useState<'HIT' | 'MISS' | 'VALIDATION'>('MISS');
  const [statusText, setStatusText] = useState<string>('MISS: Reading from Origin DB');
  const [cacheIndicatorColor, setCacheIndicatorColor] = useState<string>('#ff0055'); // Default miss color

  // Refs to gate React state updates and avoid 60fps render-loops
  const prevTextRef = useRef('');
  const prevColorRef = useRef('');

  const updateStatusText = (newText: string) => {
    if (prevTextRef.current !== newText) {
      prevTextRef.current = newText;
      setStatusText(newText);
    }
  };

  const updateIndicatorColor = (newColor: string) => {
    if (prevColorRef.current !== newColor) {
      prevColorRef.current = newColor;
      setCacheIndicatorColor(newColor);
    }
  };

  useFrame((state) => {
    const elapsed = state.clock.getElapsedTime();
    const cycleDuration = 7.0;
    const currentCycleTime = elapsed % cycleDuration;

    // Determine simulation phase (Hit, Miss, or ETag Validation)
    const stageIndex = Math.floor(elapsed / cycleDuration) % 3;
    let activeSim: 'HIT' | 'MISS' | 'VALIDATION' = 'MISS';

    if (manualMode) {
      activeSim = manualMode;
    } else {
      if (stageIndex === 0) activeSim = 'MISS';
      else if (stageIndex === 1) activeSim = 'HIT';
      else activeSim = 'VALIDATION';
    }

    if (simType !== activeSim) {
      setSimType(activeSim);
    }

    const packet = packetRef.current;
    if (!packet) return;

    // Reset default properties
    packet.scale.set(1, 1, 1);
    packet.visible = true;

    // Helper to interpolate between vectors
    const lerpBetween = (start: THREE.Vector3, end: THREE.Vector3, alpha: number) => {
      packet.position.lerpVectors(start, end, alpha);
    };

    if (activeSim === 'MISS') {
      // 0.0 to 1.5s: Client -> Cache
      if (currentCycleTime < 1.5) {
        const t = currentCycleTime / 1.5;
        lerpBetween(clientPos, cachePos, t);
        updateStatusText('Client Requesting -> Cache checking...');
        updateIndicatorColor('#ffaa00'); // orange checking
      }
      // 1.5 to 2.2s: Cache Miss Alert (red light flashes)
      else if (currentCycleTime < 2.2) {
        packet.position.copy(cachePos);
        updateStatusText('CACHE MISS! Routing to Database...');
        updateIndicatorColor('#ff0055'); // Red miss
      }
      // 2.2 to 3.7s: Cache -> DB
      else if (currentCycleTime < 3.7) {
        const t = (currentCycleTime - 2.2) / 1.5;
        lerpBetween(cachePos, dbPos, t);
        updateStatusText('DB Query Executing...');
      }
      // 3.7 to 4.2s: DB Processing
      else if (currentCycleTime < 4.2) {
        packet.position.copy(dbPos);
        updateStatusText('Reading records from Disk...');
        if (dbRef.current) {
          dbRef.current.scale.set(1.06, 1.06, 1.06);
        }
      }
      // 4.2 to 5.4s: DB -> Cache (writing to cache)
      else if (currentCycleTime < 5.4) {
        if (dbRef.current) dbRef.current.scale.set(1, 1, 1);
        const t = (currentCycleTime - 4.2) / 1.2;
        lerpBetween(dbPos, cachePos, t);
        updateStatusText('Writing retrieved data to Cache...');
      }
      // 5.4 to 5.8s: Cache glowing blue (writing state)
      else if (currentCycleTime < 5.8) {
        packet.position.copy(cachePos);
        updateStatusText('Cache populated successfully');
        updateIndicatorColor('#00e5ff'); // blue writing
      }
      // 5.8 to 6.8s: Cache -> Client (return response)
      else if (currentCycleTime < 6.8) {
        const t = (currentCycleTime - 5.8) / 1.0;
        lerpBetween(cachePos, clientPos, t);
        updateStatusText('Returning Data to Client');
      }
      // 6.8 to 7.0s: Finished
      else {
        packet.visible = false;
        updateStatusText('Cycle Completed.');
        updateIndicatorColor('#334155');
      }
    } 
    else if (activeSim === 'HIT') {
      // 0.0 to 1.5s: Client -> Cache
      if (currentCycleTime < 1.5) {
        const t = currentCycleTime / 1.5;
        lerpBetween(clientPos, cachePos, t);
        updateStatusText('Client Requesting -> Cache checking...');
        updateIndicatorColor('#ffaa00'); // orange checking
      }
      // 1.5 to 2.2s: Cache Hit Alert (green flash)
      else if (currentCycleTime < 2.2) {
        packet.position.copy(cachePos);
        updateStatusText('CACHE HIT! Instant memory response');
        updateIndicatorColor('#00ff66'); // green hit
      }
      // 2.2 to 3.7s: Cache -> Client (instant return)
      else if (currentCycleTime < 3.7) {
        const t = (currentCycleTime - 2.2) / 1.5;
        lerpBetween(cachePos, clientPos, t);
        updateStatusText('Serving from Cache memory...');
      }
      // 3.7 to 7.0s: Idle pause (shows speed contrast)
      else {
        packet.visible = false;
        updateStatusText('Finished: Response ready 3.5s faster');
        updateIndicatorColor('#334155');
      }
    } 
    else if (activeSim === 'VALIDATION') {
      // 0.0 to 1.5s: Client -> Cache (conditional check)
      if (currentCycleTime < 1.5) {
        const t = currentCycleTime / 1.5;
        lerpBetween(clientPos, cachePos, t);
        updateStatusText('GET request with conditional ETag: "v1"');
        updateIndicatorColor('#ffaa00'); // orange checking
      }
      // 1.5 to 3.0s: Cache -> DB (ETag validation)
      else if (currentCycleTime < 3.0) {
        const t = (currentCycleTime - 1.5) / 1.5;
        lerpBetween(cachePos, dbPos, t);
        updateStatusText('Checking If-None-Match header value on Server...');
      }
      // 3.0 to 3.5s: DB checking ETag
      else if (currentCycleTime < 3.5) {
        packet.position.copy(dbPos);
        updateStatusText('Server validating ETag string...');
      }
      // 3.5 to 5.0s: DB -> Client response (304 Not Modified)
      else if (currentCycleTime < 5.0) {
        const t = (currentCycleTime - 3.5) / 1.5;
        lerpBetween(dbPos, clientPos, t);
        updateStatusText('ETag match: Returning 304 Not Modified headers');
        // Packet scale is tiny, representing metadata/header-only payload
        packet.scale.set(0.4, 0.4, 0.4);
        updateIndicatorColor('#bd00ff'); // validation purple
      }
      // 5.0 to 7.0s: Idle pause
      else {
        packet.visible = false;
        updateStatusText('Finished: Saved bandwidth using 304');
        updateIndicatorColor('#334155');
      }
    }

    // Spin cache wireframe outline
    if (cacheOutlineRef.current) {
      cacheOutlineRef.current.rotation.y += 0.008;
      cacheOutlineRef.current.rotation.x += 0.004;
    }
  });

  return (
    <group>
      <ambientLight intensity={0.4} />
      <directionalLight position={[4, 8, 4]} intensity={6} color="#00e5ff" />
      <directionalLight position={[-4, 8, -4]} intensity={2} color="#ff0077" />

      {/* 🖥️ CLIENT NODE */}
      <group position={clientPos}>
        <mesh>
          <sphereGeometry args={[0.5, 32, 32]} />
          <meshStandardMaterial color="#cbd5e1" roughness={0.2} metalness={0.8} />
        </mesh>
        <Text
          position={[0, 0.9, 0]}
          fontSize={0.22}
          color="#ffffff"
          anchorX="center"
        >
          CLIENT BROWSER
        </Text>
      </group>

      {/* 🎛️ REDIS DISTRIBUTED CACHE */}
      <group position={cachePos}>
        {/* Translucent glass outer box */}
        <mesh>
          <boxGeometry args={[1.0, 1.0, 1.0]} />
          <meshPhysicalMaterial
            color="#0f172a"
            transparent
            opacity={0.65}
            roughness={0.05}
            metalness={0.1}
            transmission={0.9}
            thickness={0.6}
          />
        </mesh>
        {/* Glow indicator core */}
        <mesh>
          <sphereGeometry args={[0.25, 16, 16]} />
          <meshBasicMaterial color={cacheIndicatorColor} />
        </mesh>
        {/* Wireframe outer box */}
        <mesh ref={cacheOutlineRef}>
          <boxGeometry args={[1.2, 1.2, 1.2]} />
          <meshBasicMaterial color={cacheIndicatorColor} wireframe />
        </mesh>
        <Text
          position={[0, 1.0, 0]}
          fontSize={0.22}
          color="#00e5ff"
          anchorX="center"
        >
          DISTRIBUTED CACHE
        </Text>
      </group>

      {/* 💿 ORIGIN DATABASE */}
      <group position={dbPos} ref={dbRef}>
        <mesh position={[0, -0.4, 0]}>
          <cylinderGeometry args={[0.6, 0.6, 0.35, 32]} />
          <meshStandardMaterial color="#334155" roughness={0.3} metalness={0.7} />
        </mesh>
        <mesh position={[0, 0.05, 0]}>
          <cylinderGeometry args={[0.6, 0.6, 0.35, 32]} />
          <meshStandardMaterial color="#475569" roughness={0.3} metalness={0.7} />
        </mesh>
        <mesh position={[0, 0.5, 0]}>
          <cylinderGeometry args={[0.6, 0.6, 0.35, 32]} />
          <meshStandardMaterial color="#64748b" roughness={0.3} metalness={0.7} />
        </mesh>
        <Text
          position={[0, 1.1, 0]}
          fontSize={0.22}
          color="#ff0077"
          anchorX="center"
        >
          ORIGIN SERVER
        </Text>
      </group>

      {/* ⚡ PACKET PARTICLE */}
      <group ref={packetRef}>
        <mesh>
          <sphereGeometry args={[0.15, 16, 16]} />
          <meshBasicMaterial color="#ffffff" />
        </mesh>
        <pointLight intensity={2.0} color="#ffffff" distance={2.0} />
      </group>

      {/* 📟 Realtime Status Text */}
      <Text
        position={[0, -1.2, 0]}
        fontSize={0.25}
        color="#e2e8f0"
        anchorX="center"
      >
        {statusText}
      </Text>
    </group>
  );
}
