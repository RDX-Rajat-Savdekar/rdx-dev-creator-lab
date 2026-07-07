import {Circle, makeScene2D, Rect, Grid, Txt, Layout, Node} from '@motion-canvas/2d';
import {createRef, all, easeInOutCubic, easeOutBack, waitFor, spawn, Reference} from '@motion-canvas/core';

export default makeScene2D(function* (view) {
  // Container reference
  const containerRef = createRef<Layout>();

  // Database card references
  const db1Ref = createRef<Rect>();
  const db2Ref = createRef<Rect>();
  const db3Ref = createRef<Rect>();

  // Heartbeat signal circle references
  const heart1Ref = createRef<Circle>();
  const heart2Ref = createRef<Circle>();
  const heart3Ref = createRef<Circle>();

  // Text status metrics references (for detail panel fade-in)
  const detail1Ref = createRef<Layout>();
  const detail2Ref = createRef<Layout>();
  const detail3Ref = createRef<Layout>();

  // Add elements to view
  view.add(
    <Node>
      {/* Dark background grid */}
      <Grid
        width={1920}
        height={1080}
        spacing={80}
        stroke={'#1e1e2d'}
        lineWidth={1.5}
      />

      {/* Centered CSS Flexbox layout container */}
      <Layout
        ref={containerRef}
        layout
        direction={'column'}
        gap={30}
        alignItems={'center'}
        justifyContent={'center'}
        width={600}
        scale={0}
      >
        {/* DATABASE CARD 1 (PRIMARY) */}
        <Rect
          ref={db1Ref}
          layout
          direction={'column'}
          alignItems={'stretch'}
          width={500}
          height={90}
          radius={16}
          fill={'#0c0c14'}
          stroke={'#3f3f5c'}
          lineWidth={2.5}
          clip={true}
          padding={20}
        >
          {/* Header Row */}
          <Layout direction={'row'} alignItems={'center'} justifyContent={'space-between'} height={50}>
            <Layout direction={'row'} alignItems={'center'} gap={15}>
              <Circle
                ref={heart1Ref}
                width={16}
                height={16}
                fill={'#00e5ff'}
                opacity={0.4}
              />
              <Txt
                text={'DB-PRIMARY-01'}
                fill={'#ffffff'}
                fontFamily={'system-ui, sans-serif'}
                fontSize={18}
                fontWeight={700}
                letterSpacing={1.5}
              />
            </Layout>
            <Rect fill={'#00ff66'} radius={6} padding={[6, 12]}>
              <Txt
                text={'PRIMARY'}
                fill={'#000000'}
                fontFamily={'system-ui, sans-serif'}
                fontSize={11}
                fontWeight={800}
                letterSpacing={1}
              />
            </Rect>
          </Layout>

          {/* Separator line */}
          <Rect height={2} fill={'#242436'} margin={[12, 0]} />

          {/* Detail metrics panel */}
          <Layout ref={detail1Ref} direction={'column'} gap={12} opacity={0}>
            <Layout direction={'row'} justifyContent={'space-between'}>
              <Txt text={'Latency:'} fill={'#a5a5c5'} fontFamily={'system-ui, sans-serif'} fontSize={14} />
              <Txt text={'1.2ms'} fill={'#00e5ff'} fontFamily={'system-ui, sans-serif'} fontSize={14} fontWeight={600} />
            </Layout>
            <Layout direction={'row'} justifyContent={'space-between'}>
              <Txt text={'CPU Usage:'} fill={'#a5a5c5'} fontFamily={'system-ui, sans-serif'} fontSize={14} />
              <Txt text={'28%'} fill={'#00ff66'} fontFamily={'system-ui, sans-serif'} fontSize={14} fontWeight={600} />
            </Layout>
            <Layout direction={'row'} justifyContent={'space-between'}>
              <Txt text={'Active Conns:'} fill={'#a5a5c5'} fontFamily={'system-ui, sans-serif'} fontSize={14} />
              <Txt text={'1,420 / 5,000'} fill={'#ffffff'} fontFamily={'system-ui, sans-serif'} fontSize={14} fontWeight={600} />
            </Layout>
          </Layout>
        </Rect>

        {/* DATABASE CARD 2 (REPLICA A) */}
        <Rect
          ref={db2Ref}
          layout
          direction={'column'}
          alignItems={'stretch'}
          width={500}
          height={90}
          radius={16}
          fill={'#0c0c14'}
          stroke={'#3f3f5c'}
          lineWidth={2.5}
          clip={true}
          padding={20}
        >
          {/* Header Row */}
          <Layout direction={'row'} alignItems={'center'} justifyContent={'space-between'} height={50}>
            <Layout direction={'row'} alignItems={'center'} gap={15}>
              <Circle
                ref={heart2Ref}
                width={16}
                height={16}
                fill={'#bd00ff'}
                opacity={0.4}
              />
              <Txt
                text={'DB-REPLICA-02'}
                fill={'#ffffff'}
                fontFamily={'system-ui, sans-serif'}
                fontSize={18}
                fontWeight={700}
                letterSpacing={1.5}
              />
            </Layout>
            <Rect fill={'#bd00ff'} radius={6} padding={[6, 12]}>
              <Txt
                text={'REPLICA'}
                fill={'#ffffff'}
                fontFamily={'system-ui, sans-serif'}
                fontSize={11}
                fontWeight={800}
                letterSpacing={1}
              />
            </Rect>
          </Layout>

          {/* Separator line */}
          <Rect height={2} fill={'#242436'} margin={[12, 0]} />

          {/* Detail metrics panel */}
          <Layout ref={detail2Ref} direction={'column'} gap={12} opacity={0}>
            <Layout direction={'row'} justifyContent={'space-between'}>
              <Txt text={'Latency:'} fill={'#a5a5c5'} fontFamily={'system-ui, sans-serif'} fontSize={14} />
              <Txt text={'8.4ms'} fill={'#bd00ff'} fontFamily={'system-ui, sans-serif'} fontSize={14} fontWeight={600} />
            </Layout>
            <Layout direction={'row'} justifyContent={'space-between'}>
              <Txt text={'CPU Usage:'} fill={'#a5a5c5'} fontFamily={'system-ui, sans-serif'} fontSize={14} />
              <Txt text={'14%'} fill={'#00ff66'} fontFamily={'system-ui, sans-serif'} fontSize={14} fontWeight={600} />
            </Layout>
            <Layout direction={'row'} justifyContent={'space-between'}>
              <Txt text={'Replication Lag:'} fill={'#a5a5c5'} fontFamily={'system-ui, sans-serif'} fontSize={14} />
              <Txt text={'45ms'} fill={'#ffea00'} fontFamily={'system-ui, sans-serif'} fontSize={14} fontWeight={600} />
            </Layout>
          </Layout>
        </Rect>

        {/* DATABASE CARD 3 (REPLICA B) */}
        <Rect
          ref={db3Ref}
          layout
          direction={'column'}
          alignItems={'stretch'}
          width={500}
          height={90}
          radius={16}
          fill={'#0c0c14'}
          stroke={'#3f3f5c'}
          lineWidth={2.5}
          clip={true}
          padding={20}
        >
          {/* Header Row */}
          <Layout direction={'row'} alignItems={'center'} justifyContent={'space-between'} height={50}>
            <Layout direction={'row'} alignItems={'center'} gap={15}>
              <Circle
                ref={heart3Ref}
                width={16}
                height={16}
                fill={'#ffea00'}
                opacity={0.4}
              />
              <Txt
                text={'DB-REPLICA-03'}
                fill={'#ffffff'}
                fontFamily={'system-ui, sans-serif'}
                fontSize={18}
                fontWeight={700}
                letterSpacing={1.5}
              />
            </Layout>
            <Rect fill={'#bd00ff'} radius={6} padding={[6, 12]}>
              <Txt
                text={'REPLICA'}
                fill={'#ffffff'}
                fontFamily={'system-ui, sans-serif'}
                fontSize={11}
                fontWeight={800}
                letterSpacing={1}
              />
            </Rect>
          </Layout>

          {/* Separator line */}
          <Rect height={2} fill={'#242436'} margin={[12, 0]} />

          {/* Detail metrics panel */}
          <Layout ref={detail3Ref} direction={'column'} gap={12} opacity={0}>
            <Layout direction={'row'} justifyContent={'space-between'}>
              <Txt text={'Latency:'} fill={'#a5a5c5'} fontFamily={'system-ui, sans-serif'} fontSize={14} />
              <Txt text={'7.9ms'} fill={'#ffea00'} fontFamily={'system-ui, sans-serif'} fontSize={14} fontWeight={600} />
            </Layout>
            <Layout direction={'row'} justifyContent={'space-between'}>
              <Txt text={'CPU Usage:'} fill={'#a5a5c5'} fontFamily={'system-ui, sans-serif'} fontSize={14} />
              <Txt text={'16%'} fill={'#00ff66'} fontFamily={'system-ui, sans-serif'} fontSize={14} fontWeight={600} />
            </Layout>
            <Layout direction={'row'} justifyContent={'space-between'}>
              <Txt text={'Replication Lag:'} fill={'#a5a5c5'} fontFamily={'system-ui, sans-serif'} fontSize={14} />
              <Txt text={'38ms'} fill={'#ffea00'} fontFamily={'system-ui, sans-serif'} fontSize={14} fontWeight={600} />
            </Layout>
          </Layout>
        </Rect>
      </Layout>
    </Node>
  );

  // Background Heartbeat Generator function
  function* heartbeat(heartRef: Reference<Circle>, strokeRef: Reference<Rect>, color: string) {
    while (true) {
      // Pulse animation: expand core, light up card borders
      yield* all(
        heartRef().scale(1.6, 0.25).to(1.0, 0.45),
        heartRef().opacity(0.85, 0.25).to(0.4, 0.45),
        strokeRef().stroke(color, 0.25).to('#3f3f5c', 0.45),
        strokeRef().shadowBlur(10, 0.25).to(0, 0.45)
      );
      yield* waitFor(1.1); // Stagger interval pause
    }
  }

  // ANIMATION TIMELINE EXECUTION

  // 1. Entrance of DB Cluster Layout
  yield* containerRef().scale(1, 1.2, easeOutBack);

  // 2. Spawn concurrent background heartbeats using spawn()
  spawn(() => heartbeat(heart1Ref, db1Ref, '#00e5ff'));
  yield* waitFor(0.3); // Stagger replication heartbeat
  spawn(() => heartbeat(heart2Ref, db2Ref, '#bd00ff'));
  yield* waitFor(0.3); // Stagger third replication heartbeat
  spawn(() => heartbeat(heart3Ref, db3Ref, '#ffea00'));

  yield* waitFor(1.5);

  // 3. Interaction Sequence: Expand Card 1 (Primary)
  // When db1 height increases, layout flexbox pushes db2 and db3 downwards automatically!
  yield* all(
    db1Ref().height(240, 0.7, easeInOutCubic),
    detail1Ref().opacity(1, 0.5)
  );

  yield* waitFor(2.0);

  // 4. Collapse Card 1, Expand Card 2 (Replica A)
  yield* all(
    db1Ref().height(90, 0.6, easeInOutCubic),
    detail1Ref().opacity(0, 0.3),
    db2Ref().height(240, 0.6, easeInOutCubic),
    detail2Ref().opacity(1, 0.4)
  );

  yield* waitFor(2.0);

  // 5. Collapse Card 2, Expand Card 3 (Replica B)
  yield* all(
    db2Ref().height(90, 0.6, easeInOutCubic),
    detail2Ref().opacity(0, 0.3),
    db3Ref().height(240, 0.6, easeInOutCubic),
    detail3Ref().opacity(1, 0.4)
  );

  yield* waitFor(2.0);

  // 6. Collapse all back to initial cluster layout
  yield* all(
    db3Ref().height(90, 0.7, easeInOutCubic),
    detail3Ref().opacity(0, 0.4)
  );

  yield* waitFor(1.5);
});
