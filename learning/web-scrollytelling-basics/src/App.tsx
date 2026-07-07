import { useState, useEffect, useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

// Import R3F stages for Microservices project
import { Stage1_ServerRack } from './components/Stage1_ServerRack';
import { Stage2_LoadBalancer } from './components/Stage2_LoadBalancer';
import { Stage3_DatabaseRing } from './components/Stage3_DatabaseRing';
import { Stage4_KubernetesGrid } from './components/Stage4_KubernetesGrid';
import { Stage5_TrafficFlow } from './components/Stage5_TrafficFlow';
import { Stage6_CreativeSandbox } from './components/Stage6_CreativeSandbox';
import { Stage7_CacheValidation } from './components/Stage7_CacheValidation';

// Import R3F stage for Exosuit project
import { AresExosuit } from './components/AresExosuit';

// Import MDX documents
// @ts-ignore
import Article from './article.mdx';
// @ts-ignore
import SuitArticle from './suit_article.mdx';
import './App.css';

// Register GSAP ScrollTrigger plugin
gsap.registerPlugin(ScrollTrigger);

interface Pod {
  id: string;
  r: number;
  c: number;
  ip: string;
  cpu: string;
  status: string;
}

// 🎥 Smooth cinematic camera and pivot interpolation rig
const CameraRig = ({ stage, isExosuit = false }: { stage: number; isExosuit?: boolean }) => {
  const lookAtRef = useRef(new THREE.Vector3(0, 0, 0));

  useFrame((state) => {
    const targetPos = new THREE.Vector3(0, 0, 7.5);
    const targetLook = new THREE.Vector3(0, 0, 0);

    if (isExosuit) {
      // 🦾 Flight path coordinates targeting ARES-1 Exosuit features
      switch (stage) {
        case 1: // Intro wide overview (Text Left -> Suit Right)
          targetPos.set(-1.1, 0.2, 5.0);
          targetLook.set(-1.1, 0, 0);
          break;
        case 2: // Arc Reactor close-up (Text Right -> Suit Left)
          targetPos.set(0.9, 0.65, 1.8);
          targetLook.set(0.9, 0.65, 0);
          break;
        case 3: // Visor close-up (Text Left -> Suit Right)
          targetPos.set(-0.8, 1.32, 1.25);
          targetLook.set(-0.8, 1.32, 0);
          break;
        case 4: // Thrusters close-up (Text Right -> Suit Left)
          targetPos.set(0.9, -1.8, 2.5);
          targetLook.set(0.9, -1.6, 0);
          break;
        case 5: // Shoulder Plates details (Text Left -> Suit Right)
          targetPos.set(-1.0, 0.5, 2.2);
          targetLook.set(-2.0, 0.4, 0);
          break;
        case 6: // Outro floating (Text Right -> Suit Left)
          targetPos.set(1.1, 0, 5.5);
          targetLook.set(1.1, 0, 0);
          break;
      }
    } else {
      // 🖥️ Layout viewports for Microservices stages
      switch (stage) {
        case 1: // Server Rack close-up
          targetPos.set(0, 0.6, 5.0);
          targetLook.set(0, 0.6, 0);
          break;
        case 2: // Load Balancer side profile
          targetPos.set(-1.6, 0.5, 4.2);
          targetLook.set(0, 0, 0);
          break;
        case 3: // Sharded DB Ring elevated bird's-eye
          targetPos.set(0, 5.0, 5.0);
          targetLook.set(0, -0.6, 0);
          break;
        case 4: // Kubernetes grid side-focus
          targetPos.set(2.8, 2.8, 4.5);
          targetLook.set(0, 0.5, 0);
          break;
        case 5: // Traffic Flow wide network overview
          targetPos.set(0, 2.2, 6.8);
          targetLook.set(0, 0, 0);
          break;
        case 6: // Creative Sandbox macro detailed view
          targetPos.set(0.8, 0.8, 3.8);
          targetLook.set(0, -0.2, 0);
          break;
        case 7: // Cache & Validation perspective
          targetPos.set(0, 1.8, 5.8);
          targetLook.set(0, 0.3, 0);
          break;
      }
    }

    // Lerp camera position
    state.camera.position.lerp(targetPos, 0.05);
    // Lerp camera look-at vector
    lookAtRef.current.lerp(targetLook, 0.05);
    state.camera.lookAt(lookAtRef.current);
  });

  return null;
};

function App() {
  // Global Project Switch: 'exosuit' or 'microservices'
  const [project, setProject] = useState<'exosuit' | 'microservices'>('exosuit');
  
  // Navigation mode for microservices: 'tabbed' (interactive playground) or 'scrolly' (cinematic article)
  const [mode, setMode] = useState<'tabbed' | 'scrolly'>('scrolly');
  const [activeStage, setActiveStage] = useState<number>(1);
  
  // Active section index for Exosuit scroll triggers
  const [activeSuitSection, setActiveSuitSection] = useState<number>(1);

  // Interactive parameters for Stage 2
  const [lbClicked, setLbClicked] = useState(false);
  const [lbHovered, setLbHovered] = useState(false);

  // Interactive parameters for Stage 4
  const [selectedPod, setSelectedPod] = useState<Pod | null>(null);

  // Parameters for Stage 6
  const [waveSpeed, setWaveSpeed] = useState<number>(1.0);
  const [colorSpeed, setColorSpeed] = useState<number>(1.0);
  const [isKnot, setIsKnot] = useState<boolean>(true);

  // 1. Hook to bind ScrollTrigger to active stages in microservices scrollytelling mode
  useEffect(() => {
    if (project !== 'microservices' || mode !== 'scrolly') return;

    const timer = setTimeout(() => {
      const sections = document.querySelectorAll('.scrolly-section');
      const scrollTriggers: any[] = [];

      sections.forEach((section) => {
        const stageId = parseInt(section.getAttribute('data-stage') || '1', 10);
        
        const trigger = ScrollTrigger.create({
          trigger: section,
          scroller: '.scrolly-content',
          start: 'top 55%',
          end: 'bottom 45%',
          onEnter: () => setActiveStage(stageId),
          onEnterBack: () => setActiveStage(stageId),
        });
        scrollTriggers.push(trigger);
      });

      ScrollTrigger.refresh();
    }, 150);

    return () => {
      clearTimeout(timer);
      ScrollTrigger.getAll().forEach(t => t.kill());
    };
  }, [project, mode]);

  // 2. Hook to bind ScrollTrigger to Exosuit details on scroll
  useEffect(() => {
    if (project !== 'exosuit') return;

    const timer = setTimeout(() => {
      const sections = document.querySelectorAll('.suit-section');
      const scrollTriggers: any[] = [];

      sections.forEach((section) => {
        const sectionId = parseInt(section.getAttribute('data-section') || '1', 10);
        
        const trigger = ScrollTrigger.create({
          trigger: section,
          scroller: '.suit-scroll-container',
          start: 'top 50%',
          end: 'bottom 50%',
          onEnter: () => setActiveSuitSection(sectionId),
          onEnterBack: () => setActiveSuitSection(sectionId),
        });
        scrollTriggers.push(trigger);
      });

      ScrollTrigger.refresh();
    }, 150);

    return () => {
      clearTimeout(timer);
      ScrollTrigger.getAll().forEach(t => t.kill());
    };
  }, [project]);

  const stages = [
    { id: 1, title: 'Server Rack Cabinet', desc: 'Scene setup, lighting, & materials' },
    { id: 2, title: 'Interactive Load Balancer', desc: 'useFrame loops & click/hover triggers' },
    { id: 3, title: 'Sharded Database Ring', desc: 'Trigonometry & circular layouts' },
    { id: 4, title: 'Kubernetes Pod Grid', desc: 'Orbit controls & camera target focus' },
    { id: 5, title: 'Traffic Packet Flow', desc: 'Full integration & particle streams' },
    { id: 6, title: 'Creative Shader Sandbox', desc: 'Custom shaders & 3D MSDF text' },
    { id: 7, title: 'Cache & ETag Validation', desc: 'Caching hits, misses, and validation' },
  ];

  return (
    <div className="main-wrapper">
      {/* 🧭 Global Header Toggle */}
      <header className="global-header">
        <div className="header-logo">
          <span className="dot"></span>
          <span>RDX CREATIVE LABS</span>
        </div>
        
        {/* Toggle projects */}
        <div className="project-selector">
          <button 
            className={`project-tab-btn ${project === 'exosuit' ? 'active' : ''}`}
            onClick={() => setProject('exosuit')}
          >
            🦾 ARES-1 EXOSUIT
          </button>
          <button 
            className={`project-tab-btn ${project === 'microservices' ? 'active' : ''}`}
            onClick={() => setProject('microservices')}
          >
            🖥️ 3D MICROSERVICES
          </button>
        </div>

        {/* Mode toggle (Only shown when microservices project is active) */}
        {project === 'microservices' && (
          <div className="mode-toggle">
            <button 
              className={`toggle-mode-btn ${mode === 'scrolly' ? 'active' : ''}`}
              onClick={() => setMode('scrolly')}
            >
              📖 ARTICLE
            </button>
            <button 
              className={`toggle-mode-btn ${mode === 'tabbed' ? 'active' : ''}`}
              onClick={() => setMode('tabbed')}
            >
              🎛️ PLAYGROUND
            </button>
          </div>
        )}
      </header>

      {/* ======================================= */}
      {/* 🦾 ARES-1 EXOSUIT LAYOUT (APPLE STYLE)  */}
      {/* ======================================= */}
      {project === 'exosuit' && (
        <div className="exosuit-layout">
          {/* Fixed Background Canvas */}
          <div className="exosuit-canvas-container">
            <Canvas camera={{ position: [0, 0, 5], fov: 45 }}>
              <CameraRig stage={activeSuitSection} isExosuit={true} />
              <AresExosuit activeSection={activeSuitSection} />
            </Canvas>
          </div>

          {/* Full Screen Scroll overlay */}
          <div className="suit-scroll-container">
            <div className="suit-article-body">
              <SuitArticle />
            </div>
          </div>

          {/* Telemetry HUD Panel */}
          <div className="telemetry-hud">
            <div className="hud-header">SYSTEM METRICS</div>
            <div className="hud-row">
              <span className="hud-label">DIAGNOSTICS</span>
              <span className="hud-value color-cyan">ARES-1 OK</span>
            </div>
            <div className="hud-row">
              <span className="hud-label">POWER INGRESS</span>
              <span className="hud-value color-green">1.2 GigaWatts</span>
            </div>
            <div className="hud-row">
              <span className="hud-label">THRUST RATE</span>
              <span className="hud-value color-magenta">
                {activeSuitSection === 4 ? '98.5% (STABLE)' : '0% (STBY)'}
              </span>
            </div>
            <div className="hud-row">
              <span className="hud-label">NEURAL SYNC</span>
              <span className="hud-value">99.8% (Visor)</span>
            </div>
            <div className="hud-progress-container">
              <div 
                className="hud-progress-bar"
                style={{ 
                  width: `${(activeSuitSection / 6) * 100}%`,
                  backgroundColor: activeSuitSection === 4 ? 'var(--color-magenta)' : 'var(--color-cyan)'
                }}
              />
            </div>
          </div>
        </div>
      )}

      {/* ======================================= */}
      {/* 🖥️ 3D MICROSERVICES SCROLLY ARTICLE     */}
      {/* ======================================= */}
      {project === 'microservices' && mode === 'scrolly' && (
        <div className="scrolly-layout">
          <div className="scrolly-content">
            <div className="article-body">
              <Article />
            </div>
          </div>
          
          <div className="sticky-viewport">
            <div className="canvas-container scrolly-canvas">
              <Canvas camera={{ position: [0, 0, 7.5], fov: 45 }}>
                <CameraRig stage={activeStage} />
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
                {activeStage === 6 && (
                  <Stage6_CreativeSandbox
                    waveSpeed={waveSpeed}
                    colorSpeed={colorSpeed}
                    isKnot={isKnot}
                  />
                )}
                {activeStage === 7 && <Stage7_CacheValidation />}
              </Canvas>
              
              {/* Floating Stage Indicator */}
              <div className="floating-indicator">
                <span className="stage-tag">ACTIVE COMPONENT</span>
                <h3>{stages[activeStage - 1].title}</h3>
                <p>{stages[activeStage - 1].desc}</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ======================================= */}
      {/* 🎛️ 3D MICROSERVICES TABBED PLAYGROUND   */}
      {/* ======================================= */}
      {project === 'microservices' && mode === 'tabbed' && (
        <div className="app-container">
          <div className="sidebar">
            <div className="sidebar-header">
              <span className="badge">R3F PLAYGROUND</span>
              <h1>3D Microservices</h1>
            </div>

            <div className="stages-list">
              {stages.map((stage) => (
                <button
                  key={stage.id}
                  className={`stage-btn ${activeStage === stage.id ? 'active' : ''}`}
                  onClick={() => {
                    setActiveStage(stage.id);
                    setSelectedPod(null);
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
                  <h2>Stage 3: Coordinate Layout Math</h2>
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

              {activeStage === 6 && (
                <>
                  <h2>Stage 6: Custom Shader Materials</h2>
                  <p>
                    Custom shaders let you bypass standard materials, manipulating vertex coordinates 
                    programmatically and executing procedural math equations on pixel fragment colors.
                  </p>
                  <div className="code-box">
                    <pre>{`// Vertex Shader displacement
pos += normal * sin(pos.y * 4.0 + uTime * uWaveSpeed);

// Fragment Shader color shift
float r = 0.5 + 0.5 * sin(uTime * uColorSpeed);
gl_FragColor = vec4(r, g, b, 1.0);`}</pre>
                  </div>

                  <h2>Shader Control Panel</h2>
                  <div className="controls-section">
                    <div className="control-group">
                      <div className="control-label">
                        WAVE SPEED <span>{waveSpeed.toFixed(1)}x</span>
                      </div>
                      <input
                        type="range"
                        min="0"
                        max="3"
                        step="0.1"
                        value={waveSpeed}
                        onChange={(e) => setWaveSpeed(parseFloat(e.target.value))}
                        className="slider-input"
                      />
                    </div>

                    <div className="control-group">
                      <div className="control-label">
                        COLOR MORPH SPEED <span>{colorSpeed.toFixed(1)}x</span>
                      </div>
                      <input
                        type="range"
                        min="0"
                        max="3"
                        step="0.1"
                        value={colorSpeed}
                        onChange={(e) => setColorSpeed(parseFloat(e.target.value))}
                        className="slider-input"
                      />
                    </div>

                    <div className="control-group">
                      <span className="control-label">3D GEOMETRY SHAPE</span>
                      <div className="toggle-group">
                        <button
                          className={`toggle-btn ${isKnot ? 'active' : ''}`}
                          onClick={() => setIsKnot(true)}
                        >
                          TORUS KNOT
                        </button>
                        <button
                          className={`toggle-btn ${!isKnot ? 'active' : ''}`}
                          onClick={() => setIsKnot(false)}
                        >
                          SPHERE
                        </button>
                      </div>
                    </div>
                  </div>
                </>
              )}

              {activeStage === 7 && (
                <>
                  <h2>Stage 7: Caching & ETag Validation</h2>
                  <p>
                    Distributed caching places a fast in-memory key-value store (like Redis) 
                    in front of the database. Conditionally validating files with <code>ETag</code> 
                    headers lets the server respond with a tiny <code>304 Not Modified</code> packet, 
                    saving downstream bandwidth.
                  </p>
                  <div className="code-box">
                    <pre>{`// Express Cache validation checking
const clientTag = req.headers['if-none-match'];
if (clientTag === eTag) {
  res.status(304).end();
}`}</pre>
                  </div>
                  <div className="metrics-grid">
                    <div className="metric-card">
                      <span className="metric-label">CACHE STRATEGY</span>
                      <span className="metric-val" style={{ color: 'var(--color-cyan)' }}>Redis Memory</span>
                    </div>
                    <div className="metric-card">
                      <span className="metric-label">VALIDATION TYPE</span>
                      <span className="metric-val" style={{ color: 'var(--color-magenta)' }}>ETag Headers</span>
                    </div>
                  </div>
                </>
              )}
            </div>
          </div>

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
              {activeStage === 6 && (
                <Stage6_CreativeSandbox
                  waveSpeed={waveSpeed}
                  colorSpeed={colorSpeed}
                  isKnot={isKnot}
                />
              )}
              {activeStage === 7 && <Stage7_CacheValidation />}
            </Canvas>

            <div className="instructions-overlay">
              <div className="pulse-dot"></div>
              <span>
                {activeStage === 4 
                  ? 'Click pod to focus. Left-Click + Drag to rotate, Scroll to zoom.' 
                  : activeStage === 6
                  ? 'Drag to rotate, Scroll to zoom. Use sliders to tweak shaders.'
                  : activeStage === 7
                  ? '3D Cache routing: cycles Miss (Red) -> Hit (Green) -> ETag (Purple)'
                  : 'Interactive 3D Viewport. Left-Click + Drag to rotate.'}
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
