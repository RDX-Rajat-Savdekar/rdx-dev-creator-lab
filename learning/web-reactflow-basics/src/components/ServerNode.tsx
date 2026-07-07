import { Handle, Position } from 'reactflow';
import { Server } from 'lucide-react';

interface ServerNodeProps {
  data: {
    label: string;
    cpu: number;
    ram: string;
    status: 'online' | 'load' | 'offline';
  };
}

export function ServerNode({ data }: ServerNodeProps) {
  const statusColor = 
    data.status === 'online' ? 'var(--color-green)' : 
    data.status === 'load' ? 'var(--color-orange)' : 'var(--color-magenta)';

  return (
    <div className="custom-flow-node server-node">
      {/* Target connection input handle (Left) */}
      <Handle 
        type="target" 
        position={Position.Left} 
        id="input" 
        className="flow-handle target-handle" 
      />

      {/* Node Header */}
      <div className="node-header">
        <div className="node-icon-wrapper" style={{ borderColor: 'var(--color-green)' }}>
          <Server size={16} className="color-green" />
        </div>
        <div className="node-title-group">
          <div className="node-title">{data.label}</div>
          <div className="node-subtitle">Compute Instance</div>
        </div>
        <div 
          className="node-status-dot" 
          style={{ 
            backgroundColor: statusColor,
            boxShadow: `0 0 8px ${statusColor}`
          }}
        />
      </div>

      {/* CPU Progress Bar */}
      <div className="node-body">
        <div className="node-metric-row">
          <span className="node-metric-label">CPU LOAD</span>
          <span className="node-metric-value" style={{ color: statusColor }}>{data.cpu}%</span>
        </div>
        <div className="node-progress-container">
          <div 
            className="node-progress-bar" 
            style={{ 
              width: `${data.cpu}%`,
              backgroundColor: statusColor
            }}
          />
        </div>
        
        <div className="node-metric-row" style={{ marginTop: '8px' }}>
          <span className="node-metric-label">MEMORY USAGE</span>
          <span className="node-metric-value">{data.ram}</span>
        </div>
      </div>

      {/* Source connection output handle (Right) */}
      <Handle 
        type="source" 
        position={Position.Right} 
        id="output" 
        className="flow-handle source-handle" 
      />
    </div>
  );
}
export default ServerNode;
