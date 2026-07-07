import { useState, useCallback, useMemo, useEffect } from 'react';
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  MarkerType,
} from 'reactflow';
import type { Connection, Edge, Node } from 'reactflow';
import { Plus, Play, RefreshCw, Layers } from 'lucide-react';

import GatewayNode from './components/GatewayNode';
import ServerNode from './components/ServerNode';
import DatabaseNode from './components/DatabaseNode';

import 'reactflow/dist/style.css';
import './App.css';

// Initial Nodes layout configuration
const initialNodes: Node[] = [
  {
    id: 'gateway',
    type: 'gateway',
    position: { x: 50, y: 180 },
    data: { label: 'API Gateway', throughput: 24, status: 'active' },
  },
  {
    id: 'server-1',
    type: 'server',
    position: { x: 340, y: 80 },
    data: { label: 'Web Server Alpha', cpu: 32, ram: '4.2 GB / 8 GB', status: 'online' },
  },
  {
    id: 'server-2',
    type: 'server',
    position: { x: 340, y: 260 },
    data: { label: 'Web Server Beta', cpu: 18, ram: '3.1 GB / 8 GB', status: 'online' },
  },
  {
    id: 'database-1',
    type: 'database',
    position: { x: 650, y: 170 },
    data: { label: 'SQL DB Core', queries: 48, storage: '124 GB / 500 GB', health: 98 },
  },
];

// Initial Edges configuration
const initialEdges: Edge[] = [
  {
    id: 'e-g-s1',
    source: 'gateway',
    sourceHandle: 'a',
    target: 'server-1',
    targetHandle: 'input',
    animated: true,
    style: { stroke: 'var(--color-cyan)', strokeWidth: 2 },
    markerEnd: { type: MarkerType.ArrowClosed, color: 'var(--color-cyan)' },
  },
  {
    id: 'e-g-s2',
    source: 'gateway',
    sourceHandle: 'a',
    target: 'server-2',
    targetHandle: 'input',
    animated: true,
    style: { stroke: 'var(--color-cyan)', strokeWidth: 2 },
    markerEnd: { type: MarkerType.ArrowClosed, color: 'var(--color-cyan)' },
  },
  {
    id: 'e-s1-db',
    source: 'server-1',
    sourceHandle: 'output',
    target: 'database-1',
    targetHandle: 'input',
    animated: true,
    style: { stroke: 'var(--color-green)', strokeWidth: 2 },
    markerEnd: { type: MarkerType.ArrowClosed, color: 'var(--color-green)' },
  },
  {
    id: 'e-s2-db',
    source: 'server-2',
    sourceHandle: 'output',
    target: 'database-1',
    targetHandle: 'input',
    animated: true,
    style: { stroke: 'var(--color-green)', strokeWidth: 2 },
    markerEnd: { type: MarkerType.ArrowClosed, color: 'var(--color-green)' },
  },
];

export function App() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  
  // Simulation and UI State
  const [isSimulating, setIsSimulating] = useState(false);
  const [serverCount, setServerCount] = useState(2);
  const [logMessages, setLogMessages] = useState<string[]>([
    'System status: ONLINE',
    'Gateway initialized on port 8080.',
  ]);

  // Bind custom node components to types
  const nodeTypes = useMemo(
    () => ({
      gateway: GatewayNode,
      server: ServerNode,
      database: DatabaseNode,
    }),
    []
  );

  // Add logger line helper
  const addLog = useCallback((msg: string) => {
    setLogMessages((prev) => [
      `[${new Date().toLocaleTimeString()}] ${msg}`,
      ...prev.slice(0, 8), // Keep last 10 messages
    ]);
  }, []);

  // Connection callback (enables manual node dragging/linking)
  const onConnect = useCallback(
    (params: Edge | Connection) => {
      const formattedParams = {
        ...params,
        animated: true,
        style: { stroke: 'var(--color-cyan)', strokeWidth: 2 },
        markerEnd: { type: MarkerType.ArrowClosed, color: 'var(--color-cyan)' },
      };
      setEdges((eds) => addEdge(formattedParams, eds));
      addLog(`Created network route: ${params.source} ➔ ${params.target}`);
    },
    [setEdges, addLog]
  );

  // Programmatic Spawning: Adds a third server instance and automatically routes it
  const handleAddServer = useCallback(() => {
    if (serverCount >= 4) {
      addLog('⚠️ Max server instances reached (cluster scale limit).');
      return;
    }

    const nextId = serverCount + 1;
    const nodeId = `server-${nextId}`;
    const nodeY = 80 + serverCount * 130;

    // 1. Add node
    const newServerNode: Node = {
      id: nodeId,
      type: 'server',
      position: { x: 340, y: nodeY },
      data: {
        label: `Web Server ${String.fromCharCode(64 + nextId)}`, // Server C, Server D
        cpu: 0,
        ram: '0 GB / 8 GB',
        status: 'online',
      },
    };

    // 2. Add edges linking it to API gateway and SQL database
    const newGatewayEdge: Edge = {
      id: `e-g-${nodeId}`,
      source: 'gateway',
      sourceHandle: 'a',
      target: nodeId,
      targetHandle: 'input',
      animated: true,
      style: { stroke: 'var(--color-cyan)', strokeWidth: 2 },
      markerEnd: { type: MarkerType.ArrowClosed, color: 'var(--color-cyan)' },
    };

    const newDatabaseEdge: Edge = {
      id: `e-${nodeId}-db`,
      source: nodeId,
      sourceHandle: 'output',
      target: 'database-1',
      targetHandle: 'input',
      animated: true,
      style: { stroke: 'var(--color-green)', strokeWidth: 2 },
      markerEnd: { type: MarkerType.ArrowClosed, color: 'var(--color-green)' },
    };

    setNodes((nds) => [...nds, newServerNode]);
    setEdges((eds) => [...eds, newGatewayEdge, newDatabaseEdge]);
    setServerCount(nextId);
    addLog(`🚀 Spawned & registered container: ${newServerNode.data.label}`);
  }, [serverCount, setNodes, setEdges, addLog]);

  // Request Traffic Simulator
  const handleSimulateRequest = useCallback(() => {
    if (isSimulating) return;

    setIsSimulating(true);
    addLog('⚡ API Traffic spike initiated. Sending payload batch...');

    // 1. Instantly increase node load metrics
    setNodes((nds) =>
      nds.map((node) => {
        if (node.type === 'gateway') {
          return { ...node, data: { ...node.data, throughput: 142 } };
        }
        if (node.type === 'server') {
          return {
            ...node,
            data: {
              ...node.data,
              cpu: Math.floor(65 + Math.random() * 25),
              ram: '5.8 GB / 8 GB',
              status: 'load',
            },
          };
        }
        if (node.type === 'database') {
          return { ...node, data: { ...node.data, queries: 198, health: 95 } };
        }
        return node;
      })
    );

    // 2. Make connection lines visually speed up (we simulate this by modifying edge styling)
    setEdges((eds) =>
      eds.map((edge) => ({
        ...edge,
        style: { ...edge.style, strokeWidth: 4, stroke: 'var(--color-orange)' },
      }))
    );

    // 3. Reset to baseline after 3 seconds
    setTimeout(() => {
      setNodes((nds) =>
        nds.map((node) => {
          if (node.type === 'gateway') {
            return { ...node, data: { ...node.data, throughput: 28, status: 'active' } };
          }
          if (node.type === 'server') {
            return {
              ...node,
              data: {
                ...node.data,
                cpu: Math.floor(10 + Math.random() * 15),
                ram: '3.4 GB / 8 GB',
                status: 'online',
              },
            };
          }
          if (node.type === 'database') {
            return { ...node, data: { ...node.data, queries: 42, health: 99 } };
          }
          return node;
        })
      );

      setEdges((eds) =>
        eds.map((edge) => {
          const originalColor = edge.id.includes('db') ? 'var(--color-green)' : 'var(--color-cyan)';
          return {
            ...edge,
            style: { ...edge.style, strokeWidth: 2, stroke: originalColor },
          };
        })
      );

      setIsSimulating(false);
      addLog('✅ Traffic spike settled. Nodes returning to idle baseline.');
    }, 3500);
  }, [isSimulating, setNodes, setEdges, addLog]);

  // Reset Topology to defaults
  const handleResetTopology = useCallback(() => {
    setNodes(initialNodes);
    setEdges(initialEdges);
    setServerCount(2);
    setIsSimulating(false);
    setLogMessages([
      `[${new Date().toLocaleTimeString()}] Topology reset to cluster baseline.`,
    ]);
  }, [setNodes, setEdges]);

  return (
    <div className="reactflow-dashboard">
      {/* Sidebar Control Panel */}
      <div className="flow-sidebar">
        <div className="flow-sidebar-header">
          <span className="flow-badge">REACT FLOW STAGE</span>
          <h1>Topology Hub</h1>
          <p>Design and orchestrate connected service node architectures.</p>
        </div>

        {/* Dashboard Actions */}
        <div className="flow-actions-section">
          <h2>DIAGNOSTICS & ACTIONS</h2>
          <div className="flow-buttons-grid">
            <button 
              className="action-button-tour"
              onClick={handleSimulateRequest}
              disabled={isSimulating}
            >
              <Play size={15} />
              <span>{isSimulating ? 'ROUTING...' : 'SEND TRAFFIC'}</span>
            </button>
            <button 
              className="action-button-tour secondary"
              onClick={handleAddServer}
              disabled={serverCount >= 4}
            >
              <Plus size={15} />
              <span>SPAWN SERVER</span>
            </button>
            <button 
              className="action-button-tour secondary"
              onClick={handleResetTopology}
            >
              <RefreshCw size={14} />
              <span>RESET SYSTEM</span>
            </button>
          </div>
        </div>

        {/* Telemetry Logger */}
        <div className="telemetry-logger">
          <h2>NETWORK LOGS</h2>
          <div className="logger-terminal">
            {logMessages.map((log, index) => (
              <div key={index} className="log-line">
                {log}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* React Flow Canvas Viewport */}
      <div className="flow-canvas-container">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          nodeTypes={nodeTypes}
          fitView
          fitViewOptions={{ padding: 0.15 }}
          className="flow-viewport"
        >
          <Background color="#cbd5e1" gap={18} size={1} />
          <Controls className="flow-controls-hud" />
          <MiniMap 
            nodeColor={() => 'rgba(12, 12, 22, 0.9)'}
            maskColor="rgba(3, 3, 6, 0.6)"
            className="flow-minimap"
          />
        </ReactFlow>

        {/* Interactive Overlay Tag */}
        <div className="flow-canvas-instructions">
          <Layers size={14} className="color-cyan" />
          <span>Drag nodes to organize. Drag handles to connect custom routes manually.</span>
        </div>
      </div>
    </div>
  );
}

export default App;
