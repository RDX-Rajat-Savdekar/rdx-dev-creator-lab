import {Circle, makeScene2D, Rect, Line, Grid, Txt, Node} from '@motion-canvas/2d';
import {createRef, all, easeInOutCubic, easeOutBack, waitFor} from '@motion-canvas/core';

export default makeScene2D(function* (view) {
  // Component references
  const gridRef = createRef<Grid>();
  const clientRef = createRef<Rect>();
  const routerRef = createRef<Circle>();
  const dbRef = createRef<Rect>();
  const cacheRef = createRef<Rect>();
  const workerRef = createRef<Rect>();

  const clientLine = createRef<Line>();
  const dbLine = createRef<Line>();
  const cacheLine = createRef<Line>();
  const workerLine = createRef<Line>();

  const packetRef = createRef<Circle>();
  const pulseCoreRef = createRef<Circle>();

  // Add elements to the canvas view
  view.add(
    <Node>
      {/* Subtle modern dark grid background */}
      <Grid
        ref={gridRef}
        width={1920}
        height={1080}
        spacing={80}
        stroke={'#1e1e2d'}
        lineWidth={1.5}
      />

      {/* Dotted vector connections (initially drawn progress end={0}) */}
      <Line
        ref={clientLine}
        points={[[-400, -250], [0, 0]]}
        stroke={'#3f3f5c'}
        lineWidth={4}
        end={0}
        lineDash={[8, 8]}
      />
      <Line
        ref={dbLine}
        points={[[0, 0], [400, -250]]}
        stroke={'#3f3f5c'}
        lineWidth={4}
        end={0}
        lineDash={[8, 8]}
      />
      <Line
        ref={cacheLine}
        points={[[0, 0], [-400, 250]]}
        stroke={'#3f3f5c'}
        lineWidth={4}
        end={0}
        lineDash={[8, 8]}
      />
      <Line
        ref={workerLine}
        points={[[0, 0], [400, 250]]}
        stroke={'#3f3f5c'}
        lineWidth={4}
        end={0}
        lineDash={[8, 8]}
      />

      {/* Central High-Fidelity Router Node */}
      <Circle
        ref={routerRef}
        width={140}
        height={140}
        fill={'#0c0c14'}
        stroke={'#00e5ff'}
        lineWidth={4}
        shadowColor={'#00e5ff'}
        shadowBlur={20}
        scale={0}
      >
        <Circle
          ref={pulseCoreRef}
          width={90}
          height={90}
          fill={'#00e5ff'}
          opacity={0.3}
        />
        <Txt
          text={'ROUTER'}
          fill={'#ffffff'}
          fontFamily={'system-ui, sans-serif'}
          fontSize={16}
          fontWeight={700}
          letterSpacing={2}
        />
      </Circle>

      {/* Endpoint Nodes (Glassmorphic containers with matching neon glows) */}
      
      {/* Client Node */}
      <Rect
        ref={clientRef}
        x={-400}
        y={-250}
        width={180}
        height={70}
        radius={12}
        fill={'#0c0c14'}
        stroke={'#ff0055'}
        lineWidth={3}
        shadowColor={'#ff0055'}
        shadowBlur={10}
        scale={0}
      >
        <Txt
          text={'CLIENT'}
          fill={'#ffffff'}
          fontFamily={'system-ui, sans-serif'}
          fontSize={15}
          fontWeight={600}
          letterSpacing={1}
        />
      </Rect>

      {/* Database Node */}
      <Rect
        ref={dbRef}
        x={400}
        y={-250}
        width={180}
        height={70}
        radius={12}
        fill={'#0c0c14'}
        stroke={'#bd00ff'}
        lineWidth={3}
        shadowColor={'#bd00ff'}
        shadowBlur={10}
        scale={0}
      >
        <Txt
          text={'DATABASE'}
          fill={'#ffffff'}
          fontFamily={'system-ui, sans-serif'}
          fontSize={15}
          fontWeight={600}
          letterSpacing={1}
        />
      </Rect>

      {/* Cache Node */}
      <Rect
        ref={cacheRef}
        x={-400}
        y={250}
        width={180}
        height={70}
        radius={12}
        fill={'#0c0c14'}
        stroke={'#00ff66'}
        lineWidth={3}
        shadowColor={'#00ff66'}
        shadowBlur={10}
        scale={0}
      >
        <Txt
          text={'REDIS CACHE'}
          fill={'#ffffff'}
          fontFamily={'system-ui, sans-serif'}
          fontSize={15}
          fontWeight={600}
          letterSpacing={1}
        />
      </Rect>

      {/* Worker Node */}
      <Rect
        ref={workerRef}
        x={400}
        y={250}
        width={180}
        height={70}
        radius={12}
        fill={'#0c0c14'}
        stroke={'#ffea00'}
        lineWidth={3}
        shadowColor={'#ffea00'}
        shadowBlur={10}
        scale={0}
      >
        <Txt
          text={'WORKER'}
          fill={'#ffffff'}
          fontFamily={'system-ui, sans-serif'}
          fontSize={15}
          fontWeight={600}
          letterSpacing={1}
        />
      </Rect>

      {/* Glowing Data Packet */}
      <Circle
        ref={packetRef}
        x={-400}
        y={-250}
        width={24}
        height={24}
        fill={'#00ffcc'}
        shadowColor={'#00ffcc'}
        shadowBlur={20}
        opacity={0}
      />
    </Node>
  );

  // ANIMATION TIMELINE EXECUTION

  // 1. Staggered Entrance of Nodes
  yield* all(
    routerRef().scale(1, 1.2, easeOutBack),
    clientRef().scale(1, 1.2, easeOutBack),
    dbRef().scale(1, 1.2, easeOutBack),
    cacheRef().scale(1, 1.2, easeOutBack),
    workerRef().scale(1, 1.2, easeOutBack)
  );

  // 2. Draw connecting network cables
  yield* all(
    clientLine().end(1, 1),
    dbLine().end(1, 1),
    cacheLine().end(1, 1),
    workerLine().end(1, 1)
  );

  // 3. Loop simulation of packets routing through the topology
  
  // -- Sequence 1: Client -> Router -> Database
  packetRef().position([-400, -250]);
  yield* packetRef().opacity(1, 0.4);
  yield* packetRef().position([0, 0], 1.2, easeInOutCubic);

  // Impact Pulse on Router Node
  yield* all(
    routerRef().scale(1.15, 0.15).to(1.0, 0.25),
    pulseCoreRef().scale(2.2, 0.35).to(1.0, 0.35),
    pulseCoreRef().opacity(0.8, 0.35).to(0.3, 0.35)
  );

  // Route to Database Node
  yield* packetRef().position([400, -250], 1.2, easeInOutCubic);
  yield* all(
    dbRef().scale(1.15, 0.15).to(1.0, 0.25),
    packetRef().opacity(0, 0.3)
  );

  yield* waitFor(0.5);

  // -- Sequence 2: Client -> Router -> Redis Cache
  packetRef().position([-400, -250]);
  yield* packetRef().opacity(1, 0.4);
  yield* packetRef().position([0, 0], 1.2, easeInOutCubic);

  // Impact Pulse on Router Node
  yield* all(
    routerRef().scale(1.15, 0.15).to(1.0, 0.25),
    pulseCoreRef().scale(2.2, 0.35).to(1.0, 0.35)
  );

  // Route to Redis Cache Node
  yield* packetRef().position([-400, 250], 1.2, easeInOutCubic);
  yield* all(
    cacheRef().scale(1.15, 0.15).to(1.0, 0.25),
    packetRef().opacity(0, 0.3)
  );

  yield* waitFor(0.5);

  // -- Sequence 3: Client -> Router -> Worker
  packetRef().position([-400, -250]);
  yield* packetRef().opacity(1, 0.4);
  yield* packetRef().position([0, 0], 1.2, easeInOutCubic);

  // Impact Pulse on Router Node
  yield* all(
    routerRef().scale(1.15, 0.15).to(1.0, 0.25),
    pulseCoreRef().scale(2.2, 0.35).to(1.0, 0.35)
  );

  // Route to Worker Node
  yield* packetRef().position([400, 250], 1.2, easeInOutCubic);
  yield* all(
    workerRef().scale(1.15, 0.15).to(1.0, 0.25),
    packetRef().opacity(0, 0.3)
  );

  yield* waitFor(1);
});
