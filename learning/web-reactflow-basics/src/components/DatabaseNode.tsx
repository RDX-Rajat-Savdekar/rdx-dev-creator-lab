import { Handle, Position } from 'reactflow';
import { Database } from 'lucide-react';

interface DatabaseNodeProps {
  data: {
    label: string;
    queries: number;
    storage: string;
    health: number;
  };
}

export function DatabaseNode({ data }: DatabaseNodeProps) {
  const healthColor = data.health > 80 ? 'var(--color-cyan)' : 'var(--color-orange)';

  return (
    <div className="custom-flow-node database-node">
      {/* Target connection input handle (Left) */}
      <Handle 
        type="target" 
        position={Position.Left} 
        id="input" 
        className="flow-handle target-handle" 
      />

      {/* Node Header */}
      <div className="node-header">
        <div className="node-icon-wrapper" style={{ borderColor: 'var(--color-magenta)' }}>
          <Database size={16} className="color-magenta" />
        </div>
        <div className="node-title-group">
          <div className="node-title">{data.label}</div>
          <div className="node-subtitle">SQL Shard Ring</div>
        </div>
        <div 
          className="node-status-dot" 
          style={{ 
            backgroundColor: 'var(--color-magenta)',
            boxShadow: '0 0 8px var(--color-magenta)'
          }}
        />
      </div>

      {/* Telemetry metrics */}
      <div className="node-body">
        <div className="node-metric-row">
          <span className="node-metric-label">ACTIVE QUERIES</span>
          <span className="node-metric-value color-magenta">{data.queries} q/s</span>
        </div>
        <div className="node-metric-row" style={{ marginTop: '8px' }}>
          <span className="node-metric-label">STORAGE LIMIT</span>
          <span className="node-metric-value">{data.storage}</span>
        </div>
        <div className="node-metric-row" style={{ marginTop: '8px' }}>
          <span className="node-metric-label">REPLICA HEALTH</span>
          <span className="node-metric-value" style={{ color: healthColor }}>{data.health}%</span>
        </div>
      </div>
    </div>
  );
}
export default DatabaseNode;
