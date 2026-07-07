import { Handle, Position } from 'reactflow';
import { Globe } from 'lucide-react';

interface GatewayNodeProps {
  data: {
    label: string;
    throughput: number;
    status: 'active' | 'idle' | 'error';
  };
}

export function GatewayNode({ data }: GatewayNodeProps) {
  const statusColor = 
    data.status === 'active' ? 'var(--color-green)' : 
    data.status === 'error' ? 'var(--color-magenta)' : '#64748b';

  return (
    <div className="custom-flow-node gateway-node">
      {/* Node Header */}
      <div className="node-header">
        <div className="node-icon-wrapper" style={{ borderColor: 'var(--color-cyan)' }}>
          <Globe size={16} className="color-cyan" />
        </div>
        <div className="node-title-group">
          <div className="node-title">{data.label}</div>
          <div className="node-subtitle">Ingress API Router</div>
        </div>
        <div 
          className="node-status-dot" 
          style={{ 
            backgroundColor: statusColor,
            boxShadow: `0 0 8px ${statusColor}`
          }}
        />
      </div>

      {/* Telemetry Stats */}
      <div className="node-body">
        <div className="node-metric-row">
          <span className="node-metric-label">THROUGHPUT</span>
          <span className="node-metric-value color-cyan">{data.throughput} req/s</span>
        </div>
      </div>

      {/* Connection Handle (Right for output flow) */}
      <Handle 
        type="source" 
        position={Position.Right} 
        id="a" 
        className="flow-handle source-handle" 
      />
    </div>
  );
}
export default GatewayNode;
