import {Circle, makeScene2D, Rect, Grid, Txt, Layout, Node, Spline} from '@motion-canvas/2d';
import {createRef, all, easeInOutCubic, easeOutBack, waitFor, spawn, Reference} from '@motion-canvas/core';

export default makeScene2D(function* (view) {
  // References
  const producerRef = createRef<Rect>();
  const brokerRef = createRef<Rect>();
  const consumerARef = createRef<Rect>();
  const consumerBRef = createRef<Rect>();

  // Line/Spline references
  const splineP0 = createRef<Spline>();
  const splineP1 = createRef<Spline>();
  const splineP2 = createRef<Spline>();
  const splineC_A = createRef<Spline>();
  const splineC_B = createRef<Spline>();

  // Queue slots references (represent messages inside partitions)
  const p0Slots = [createRef<Rect>(), createRef<Rect>(), createRef<Rect>()];
  const p1Slots = [createRef<Rect>(), createRef<Rect>(), createRef<Rect>()];
  const p2Slots = [createRef<Rect>(), createRef<Rect>(), createRef<Rect>()];

  // Packet references
  const packetRef = createRef<Circle>();

  // Add elements
  view.add(
    <Node>
      {/* Background Grid */}
      <Grid
        width={1920}
        height={1080}
        spacing={80}
        stroke={'#1e1e2d'}
        lineWidth={1.5}
      />

      {/* Curved Splines connecting nodes */}
      <Spline
        ref={splineP0}
        points={[[-500, 0], [-250, -100], [-130, -100]]}
        stroke={'#3f3f5c'}
        lineWidth={4}
        end={0}
        lineDash={[8, 8]}
      />
      <Spline
        ref={splineP1}
        points={[[-500, 0], [-250, 0], [-130, 0]]}
        stroke={'#3f3f5c'}
        lineWidth={4}
        end={0}
        lineDash={[8, 8]}
      />
      <Spline
        ref={splineP2}
        points={[[-500, 0], [-250, 100], [-130, 100]]}
        stroke={'#3f3f5c'}
        lineWidth={4}
        end={0}
        lineDash={[8, 8]}
      />

      <Spline
        ref={splineC_A}
        points={[[130, -100], [300, -100], [460, -120]]}
        stroke={'#3f3f5c'}
        lineWidth={4}
        end={0}
        lineDash={[8, 8]}
      />
      <Spline
        ref={splineC_B}
        points={[[130, 100], [300, 100], [460, 120]]}
        stroke={'#3f3f5c'}
        lineWidth={4}
        end={0}
        lineDash={[8, 8]}
      />

      {/* PRODUCER NODE */}
      <Rect
        ref={producerRef}
        x={-500}
        y={0}
        width={180}
        height={80}
        radius={12}
        fill={'#0c0c14'}
        stroke={'#ff0055'}
        lineWidth={3}
        shadowColor={'#ff0055'}
        shadowBlur={15}
        scale={0}
        layout
        alignItems={'center'}
        justifyContent={'center'}
      >
        <Txt
          text={'PRODUCER'}
          fill={'#ffffff'}
          fontFamily={'system-ui, sans-serif'}
          fontSize={16}
          fontWeight={700}
          letterSpacing={1.5}
        />
      </Rect>

      {/* KAFKA BROKER (Center Partition Container) */}
      <Rect
        ref={brokerRef}
        x={0}
        y={0}
        width={260}
        height={340}
        radius={16}
        fill={'#0c0c14'}
        stroke={'#00e5ff'}
        lineWidth={3.5}
        shadowColor={'#00e5ff'}
        shadowBlur={15}
        scale={0}
        layout
        direction={'column'}
        padding={20}
        gap={15}
      >
        <Txt
          text={'KAFKA BROKER'}
          fill={'#00e5ff'}
          fontFamily={'system-ui, sans-serif'}
          fontSize={15}
          fontWeight={800}
          letterSpacing={1}
          textAlign={'center'}
        />

        {/* Partition 0 */}
        <Rect
          layout
          direction={'row'}
          alignItems={'center'}
          gap={10}
          fill={'#141420'}
          radius={8}
          padding={10}
          height={65}
        >
          <Txt text={'P0'} fill={'#a5a5c5'} fontFamily={'system-ui, sans-serif'} fontSize={12} fontWeight={700} />
          <Layout direction={'row'} gap={6}>
            <Rect ref={p0Slots[0]} width={28} height={28} radius={4} fill={'#ff0055'} opacity={0} />
            <Rect ref={p0Slots[1]} width={28} height={28} radius={4} fill={'#ff0055'} opacity={0} />
            <Rect ref={p0Slots[2]} width={28} height={28} radius={4} fill={'#ff0055'} opacity={0} />
          </Layout>
        </Rect>

        {/* Partition 1 */}
        <Rect
          layout
          direction={'row'}
          alignItems={'center'}
          gap={10}
          fill={'#141420'}
          radius={8}
          padding={10}
          height={65}
        >
          <Txt text={'P1'} fill={'#a5a5c5'} fontFamily={'system-ui, sans-serif'} fontSize={12} fontWeight={700} />
          <Layout direction={'row'} gap={6}>
            <Rect ref={p1Slots[0]} width={28} height={28} radius={4} fill={'#bd00ff'} opacity={0} />
            <Rect ref={p1Slots[1]} width={28} height={28} radius={4} fill={'#bd00ff'} opacity={0} />
            <Rect ref={p1Slots[2]} width={28} height={28} radius={4} fill={'#bd00ff'} opacity={0} />
          </Layout>
        </Rect>

        {/* Partition 2 */}
        <Rect
          layout
          direction={'row'}
          alignItems={'center'}
          gap={10}
          fill={'#141420'}
          radius={8}
          padding={10}
          height={65}
        >
          <Txt text={'P2'} fill={'#a5a5c5'} fontFamily={'system-ui, sans-serif'} fontSize={12} fontWeight={700} />
          <Layout direction={'row'} gap={6}>
            <Rect ref={p2Slots[0]} width={28} height={28} radius={4} fill={'#ffea00'} opacity={0} />
            <Rect ref={p2Slots[1]} width={28} height={28} radius={4} fill={'#ffea00'} opacity={0} />
            <Rect ref={p2Slots[2]} width={28} height={28} radius={4} fill={'#ffea00'} opacity={0} />
          </Layout>
        </Rect>
      </Rect>

      {/* CONSUMER A (Top Right) */}
      <Rect
        ref={consumerARef}
        x={550}
        y={-100}
        width={180}
        height={80}
        radius={12}
        fill={'#0c0c14'}
        stroke={'#00ff66'}
        lineWidth={3}
        shadowColor={'#00ff66'}
        shadowBlur={15}
        scale={0}
        layout
        alignItems={'center'}
        justifyContent={'center'}
      >
        <Txt
          text={'CONSUMER A'}
          fill={'#ffffff'}
          fontFamily={'system-ui, sans-serif'}
          fontSize={15}
          fontWeight={700}
          letterSpacing={1}
        />
      </Rect>

      {/* CONSUMER B (Bottom Right) */}
      <Rect
        ref={consumerBRef}
        x={550}
        y={100}
        width={180}
        height={80}
        radius={12}
        fill={'#0c0c14'}
        stroke={'#00ff66'}
        lineWidth={3}
        shadowColor={'#00ff66'}
        shadowBlur={15}
        scale={0}
        layout
        alignItems={'center'}
        justifyContent={'center'}
      >
        <Txt
          text={'CONSUMER B'}
          fill={'#ffffff'}
          fontFamily={'system-ui, sans-serif'}
          fontSize={15}
          fontWeight={700}
          letterSpacing={1}
        />
      </Rect>

      {/* Glowing Packet Particle */}
      <Circle
        ref={packetRef}
        width={22}
        height={22}
        fill={'#ff00cc'}
        shadowColor={'#ff00cc'}
        shadowBlur={15}
        opacity={0}
      />
    </Node>
  );

  // ANIMATION SEQUENCES

  // 1. Entrance of Nodes
  yield* all(
    producerRef().scale(1, 1.0, easeOutBack),
    brokerRef().scale(1, 1.0, easeOutBack),
    consumerARef().scale(1, 1.0, easeOutBack),
    consumerBRef().scale(1, 1.0, easeOutBack)
  );

  // 2. Draw connections (Splines)
  yield* all(
    splineP0().end(1, 1),
    splineP1().end(1, 1),
    splineP2().end(1, 1),
    splineC_A().end(1, 1),
    splineC_B().end(1, 1)
  );

  // 3. Staggered packet push from Producer to Kafka partitions
  
  // -- Packet 1 -> Partition P0
  packetRef().position([-500, 0]);
  yield* packetRef().opacity(1, 0.3);
  // Animate curved Bezier motion to P0 slot 0
  yield* packetRef().position([-250, -100], 0.6, easeInOutCubic).to([-70, -100], 0.5, easeInOutCubic);
  yield* all(
    packetRef().opacity(0, 0.2),
    p0Slots[0]().opacity(1, 0.2),
    p0Slots[0]().scale(1.2, 0.15).to(1.0, 0.15)
  );

  // -- Packet 2 -> Partition P1
  packetRef().position([-500, 0]);
  yield* packetRef().opacity(1, 0.3);
  // Animate straight-ish line to P1 slot 0
  yield* packetRef().position([-250, 0], 0.6, easeInOutCubic).to([-70, 0], 0.5, easeInOutCubic);
  yield* all(
    packetRef().opacity(0, 0.2),
    p1Slots[0]().opacity(1, 0.2),
    p1Slots[0]().scale(1.2, 0.15).to(1.0, 0.15)
  );

  // -- Packet 3 -> Partition P2
  packetRef().position([-500, 0]);
  yield* packetRef().opacity(1, 0.3);
  yield* packetRef().position([-250, 100], 0.6, easeInOutCubic).to([-70, 100], 0.5, easeInOutCubic);
  yield* all(
    packetRef().opacity(0, 0.2),
    p2Slots[0]().opacity(1, 0.2),
    p2Slots[0]().scale(1.2, 0.15).to(1.0, 0.15)
  );

  yield* waitFor(0.5);

  // -- Packet 4 -> Partition P0 slot 1
  packetRef().position([-500, 0]);
  yield* packetRef().opacity(1, 0.3);
  yield* packetRef().position([-250, -100], 0.6, easeInOutCubic).to([-32, -100], 0.5, easeInOutCubic);
  yield* all(
    packetRef().opacity(0, 0.2),
    p0Slots[1]().opacity(1, 0.2),
    p0Slots[1]().scale(1.2, 0.15).to(1.0, 0.15)
  );

  // -- Packet 5 -> Partition P2 slot 1
  packetRef().position([-500, 0]);
  yield* packetRef().opacity(1, 0.3);
  yield* packetRef().position([-250, 100], 0.6, easeInOutCubic).to([-32, 100], 0.5, easeInOutCubic);
  yield* all(
    packetRef().opacity(0, 0.2),
    p2Slots[1]().opacity(1, 0.2),
    p2Slots[1]().scale(1.2, 0.15).to(1.0, 0.15)
  );

  yield* waitFor(0.8);

  // 4. Staggered consumption: Consumer A pulls from P0, Consumer B pulls from P2
  
  // -- Consumer A pulling from P0 (slot 0)
  packetRef().position([-70, -100]);
  yield* all(
    p0Slots[0]().opacity(0, 0.2),
    packetRef().opacity(1, 0.2)
  );
  yield* packetRef().position([300, -100], 0.5, easeInOutCubic).to([550, -100], 0.5, easeInOutCubic);
  yield* all(
    packetRef().opacity(0, 0.2),
    consumerARef().scale(1.15, 0.15).to(1.0, 0.25)
  );

  // Shift remaining P0 slot 1 forward to slot 0
  yield* all(
    p0Slots[1]().opacity(0, 0.3),
    p0Slots[0]().opacity(1, 0.3),
    p0Slots[0]().scale(1.2, 0.15).to(1.0, 0.15)
  );

  // -- Consumer B pulling from P2 (slot 0)
  packetRef().position([-70, 100]);
  yield* all(
    p2Slots[0]().opacity(0, 0.2),
    packetRef().opacity(1, 0.2)
  );
  yield* packetRef().position([300, 100], 0.5, easeInOutCubic).to([550, 100], 0.5, easeInOutCubic);
  yield* all(
    packetRef().opacity(0, 0.2),
    consumerBRef().scale(1.15, 0.15).to(1.0, 0.25)
  );

  // Shift remaining P2 slot 1 forward
  yield* all(
    p2Slots[1]().opacity(0, 0.3),
    p2Slots[0]().opacity(1, 0.3),
    p2Slots[0]().scale(1.2, 0.15).to(1.0, 0.15)
  );

  yield* waitFor(1.5);
});
