import { useState } from 'react';
import { Canvas } from '@react-three/fiber';
import { Stage1_ServerRack } from './components/Stage1_ServerRack';
import { Stage2_LoadBalancer } from './components/Stage2_LoadBalancer';
import { Stage3_DatabaseRing } from './components/Stage3_DatabaseRing';
import { Stage4_KubernetesGrid } from './components/Stage4_KubernetesGrid';
import { Stage5_TrafficFlow } from './components/Stage5_TrafficFlow';
import './App.css';

interface Pod {
  id: string;
  r: number;
  c: number;
  ip: string;
  cpu: string;
  status: string;
}

function App() {
  const [activeStage, setActiveStage] = useState<number>(1);
  
  // Interactive metrics for Stage 2 (Load Balancer)
  const [lbClicked, setLbClicked] = useState(false);
  const [lbHovered, setLbHovered] = useState(false);

  // Interactive metrics for Stage 4 (Kubernetes Grid)
  const [selectedPod, setSelectedPod] = useState<Pod | null>(null);

  const stages = [
    { id: 1, title: 'Server Rack Cabinet', desc: 'Scene setup, lighting, & materials' },
    { id: 2, title: 'Interactive Load Balancer', desc: 'useFrame loops & click/hover triggers' },
    { id: 3, title: 'Sharded Database Ring', desc: 'Trigonometry & circular layouts' },
    { id: 4, title: 'Kubernetes Pod Grid', desc: 'Orbit controls & camera target focus' },
    { id: 5, title: 'Traffic Packet Flow', desc: 'Full integration & particle streams' },
  ];

  return (
    <div className="app-container">
      {/* LEFT SIDEBAR: Controls & Information */}
      <div className="sidebar">
        <div className="sidebar-header">
          <span className="badge">R3F PLAYGROUND</span>
          <h1>3D Microservices</h1>
        </div>

        {/* Navigation Tabs */}
        <div className="stages-list">
          {stages.map((stage) => (
            <button
              key={stage.id}
              className={`stage-btn ${activeStage === stage.id ? 'active' : ''}`}
              onClick={() => {
                setActiveStage(stage.id);
                setSelectedPod(null); // Reset detail overlays
              }}
            >
              <div className="stage-num">{stage.id}</div>
              <div>
                <div style={{ fontSize: '13px', fontWeight: 700 }}>{stage.title}</div>
                <div style={{ fontSize: '11px', color: '#64748b', marginTop: '2px' }}>{stage.desc}</div>
              </div>
            </button>
          ))}
        </div>

        {/* Scrollable Information / Documentation Panel */}
        <div className="info-panel">
          {activeStage === 1 && (
            <>
              <h2>Stage 1: Scene & Materials</h2>
              <p>
                In Three.js, directional and ambient lights act on metallic surfaces. 
                Applying <code>metalness={0.9}</code> and <code>roughness={0.15}</code> to 
                cabinet materials renders sleek reflective server blades.
              </p>
              <div className="code-box">
                <pre>{`<mesh>
  <boxGeometry args={[2.2, 3.4, 1.8]} />
  <meshStandardMaterial 
    color="#0d0d18" 
    metalness={0.9} 
    roughness={0.15} 
  />
</mesh>`}</pre>
              </div>
              <div className="metrics-grid">
                <div className="metric-card">
                  <span className="metric-label">METALNESS</span>
                  <span className="metric-val" style={{ color: 'var(--color-cyan)' }}>0.90</span>
                </div>
                <div className="metric-card">
                  <span className="metric-label">ROUGHNESS</span>
                  <span className="metric-val" style={{ color: 'var(--color-magenta)' }}>0.15</span>
                </div>
              </div>
            </>
          )}

          {activeStage === 2 && (
            <>
              <h2>Stage 2: useFrame Loops & Clicks</h2>
              <p>
                The <code>useFrame()</code> hook executes animations at 60fps inside the WebGL loop. 
                React states update pointer hooks dynamically to scale meshes and change emissive colors.
              </p>
              <div className="code-box">
                <pre>{`useFrame((state, delta) => {
  // Rotate core on tick
  coreRef.current.rotation.y += delta * 0.4;
  
  // Spring lerp scale values
  const target = clicked ? 1.3 : 1.0;
  groupRef.current.scale.lerp(
    new Vector3(target, target, target),
    0.15
  );
});`}</pre>
              </div>
              <div className="metrics-grid">
                <div className="metric-card">
                  <span className="metric-label">POINTER HOVER</span>
                  <span className="metric-val" style={{ color: lbHovered ? 'var(--color-cyan)' : '#64748b' }}>
                    {lbHovered ? 'ACTIVE' : 'IDLE'}
                  </span>
                </div>
                <div className="metric-card">
                  <span className="metric-label">SCALE MODE</span>
                  <span className="metric-val" style={{ color: lbClicked ? 'var(--color-magenta)' : 'var(--color-green)' }}>
                    {lbClicked ? 'BOOSTED (1.3x)' : 'DEFAULT (1.0x)'}
                  </span>
                </div>
              </div>
            </>
          )}

          {activeStage === 3 && (
            <>
              <h2>Stage 3: Coordinate Layout math</h2>
              <p>
                Database cluster rings are generated dynamically. Using trigonometry 
                (sine and cosine distribution), we space cylinder elements evenly 
                around a radius.
              </p>
              <div className="code-box">
                <pre>{`const radius = 2.8;
{dbNodes.map((node, index) => {
  const angle = (index * 2 * Math.PI) / count;
  const x = Math.cos(angle) * radius;
  const z = Math.sin(angle) * radius;
  
  return <DatabaseNode position={[x, 0, z]} />;
})}`}</pre>
              </div>
              <div className="metrics-grid">
                <div className="metric-card">
                  <span className="metric-label">RING NODES</span>
                  <span className="metric-val">5 Units</span>
                </div>
                <div className="metric-card">
                  <span className="metric-label">SPACING ANGLE</span>
                  <span className="metric-val" style={{ color: 'var(--color-cyan)' }}>72° (2π/5)</span>
                </div>
              </div>
            </>
          )}

          {activeStage === 4 && (
            <>
              <h2>Stage 4: Camera Target Focus</h2>
              <p>
                Clicking on a pod cube changes our camera target offset. Inside the loop, the camera 
                and Drei's <code>OrbitControls</code> target coordinates smooth-interpolate (lerp) 
                directly to focus on the selected node.
              </p>
              <div className="code-box">
                <pre>{`useFrame((state) => {
  // Smooth lerp camera
  state.camera.position.lerp(targetCam, 0.08);
  
  // Smooth lerp pivot center
  controlsRef.current.target.lerp(targetLook, 0.08);
});`}</pre>
              </div>
              
              <h2>Pod Metadata</h2>
              {selectedPod ? (
                <div className="metrics-grid">
                  <div className="metric-card">
                    <span className="metric-label">POD ID</span>
                    <span className="metric-val" style={{ color: 'var(--color-cyan)' }}>{selectedPod.id}</span>
                  </div>
                  <div className="metric-card">
                    <span className="metric-label">STATUS</span>
                    <span className="metric-val" style={{ color: selectedPod.status === 'RUNNING' ? 'var(--color-green)' : 'var(--color-orange)' }}>
                      {selectedPod.status}
                    </span>
                  </div>
                  <div className="metric-card">
                    <span className="metric-label">IP ROUTE</span>
                    <span className="metric-val" style={{ fontSize: '13px', marginTop: '3px' }}>{selectedPod.ip}</span>
                  </div>
                  <div className="metric-card">
                    <span className="metric-label">CPU LOAD</span>
                    <span className="metric-val">{selectedPod.cpu}</span>
                  </div>
                </div>
              ) : (
                <p style={{ fontStyle: 'italic', fontSize: '12px', marginTop: '8px' }}>
                  Click on any pod node in the 3D grid viewport to inspect and zoom-focus the camera.
                </p>
              )}
            </>
          )}

          {activeStage === 5 && (
            <>
              <h2>Stage 5: Traffic Particle Flows</h2>
              <p>
                Combines elements to represent complete systems. Particle meshes containing point lights 
                increment their segment boundaries and lerp coordinates sequentially to simulate 
                API requests flying between endpoints.
              </p>
              <div className="code-box">
                <pre>{`useFrame((state, delta) => {
  packets.forEach((packet) => {
    packet.progress += delta * speed;
    
    // Segmented lerp calculations
    if (progress < 1.0) {
      mesh.position.lerpVectors(ingress, lb, progress);
    } else {
      mesh.position.lerpVectors(lb, worker, t);
    }
  });
});`}</pre>
              </div>
              <div className="metrics-grid">
                <div className="metric-card">
                  <span className="metric-label">ACTIVE PACKETS</span>
                  <span className="metric-val">3 Streams</span>
                </div>
                <div className="metric-card">
                  <span className="metric-label">INGRESS ROUTE</span>
                  <span className="metric-val" style={{ color: 'var(--color-cyan)' }}>Active</span>
                </div>
              </div>
            </>
          )}
        </div>
      </div>

      {/* RIGHT VIEWPORT: 3D Canvas */}
      <div className="canvas-container">
        <Canvas camera={{ position: [0, 0, 7.5], fov: 45 }}>
          {activeStage === 1 && <Stage1_ServerRack />}
          {activeStage === 2 && (
            <Stage2_LoadBalancer 
              onInteraction={(clicked, hovered) => {
                setLbClicked(clicked);
                setLbHovered(hovered);
              }} 
            />
          )}
          {activeStage === 3 && <Stage3_DatabaseRing />}
          {activeStage === 4 && (
            <Stage4_KubernetesGrid 
              onPodSelect={(pod) => setSelectedPod(pod)} 
            />
          )}
          {activeStage === 5 && <Stage5_TrafficFlow />}
        </Canvas>

        {/* Viewport Interactivity Instructions */}
        <div className="instructions-overlay">
          <div className="pulse-dot"></div>
          <span>
            {activeStage === 4 
              ? 'Click pod to focus. Left-Click + Drag to rotate, Scroll to zoom.' 
              : 'Interactive 3D Viewport. Left-Click + Drag to rotate.'}
          </span>
        </div>
      </div>
    </div>
  );
}

export default App;
