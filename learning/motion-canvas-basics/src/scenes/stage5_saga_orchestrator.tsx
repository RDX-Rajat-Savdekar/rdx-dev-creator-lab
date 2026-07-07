import {Circle, makeScene2D, Rect, Grid, Txt, Layout, Node, Line} from '@motion-canvas/2d';
import {createRef, all, easeInOutCubic, easeOutBack, waitFor} from '@motion-canvas/core';

export default makeScene2D(function* (view) {
  // Service references
  const sagaRef = createRef<Rect>();
  const orderRef = createRef<Rect>();
  const paymentRef = createRef<Rect>();
  const inventoryRef = createRef<Rect>();

  // State labels references
  const orderStatus = createRef<Txt>();
  const paymentStatus = createRef<Txt>();
  const inventoryStatus = createRef<Txt>();

  // Network wires references
  const wireOrder = createRef<Line>();
  const wirePayment = createRef<Line>();
  const wireInventory = createRef<Line>();

  // Packet particle references
  const packetRef = createRef<Circle>();
  const packetTxt = createRef<Txt>();

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

      {/* Network Connections */}
      <Line
        ref={wireOrder}
        points={[[-400, -150], [0, 0]]}
        stroke={'#3f3f5c'}
        lineWidth={4}
        end={0}
      />
      <Line
        ref={wirePayment}
        points={[[0, -180], [0, 0]]}
        stroke={'#3f3f5c'}
        lineWidth={4}
        end={0}
      />
      <Line
        ref={wireInventory}
        points={[[400, -150], [0, 0]]}
        stroke={'#3f3f5c'}
        lineWidth={4}
        end={0}
      />

      {/* ORDER SERVICE */}
      <Rect
        ref={orderRef}
        x={-400}
        y={-150}
        width={200}
        height={90}
        radius={12}
        fill={'#0c0c14'}
        stroke={'#bd00ff'}
        lineWidth={3}
        shadowColor={'#bd00ff'}
        shadowBlur={10}
        scale={0}
        layout
        direction={'column'}
        alignItems={'center'}
        justifyContent={'center'}
        gap={5}
      >
        <Txt
          text={'ORDER SERVICE'}
          fill={'#ffffff'}
          fontFamily={'system-ui, sans-serif'}
          fontSize={15}
          fontWeight={700}
        />
        <Txt
          ref={orderStatus}
          text={'PENDING'}
          fill={'#a5a5c5'}
          fontFamily={'system-ui, sans-serif'}
          fontSize={11}
          fontWeight={800}
          letterSpacing={1}
        />
      </Rect>

      {/* PAYMENT SERVICE */}
      <Rect
        ref={paymentRef}
        x={0}
        y={-180}
        width={200}
        height={90}
        radius={12}
        fill={'#0c0c14'}
        stroke={'#bd00ff'}
        lineWidth={3}
        shadowColor={'#bd00ff'}
        shadowBlur={10}
        scale={0}
        layout
        direction={'column'}
        alignItems={'center'}
        justifyContent={'center'}
        gap={5}
      >
        <Txt
          text={'PAYMENT SERVICE'}
          fill={'#ffffff'}
          fontFamily={'system-ui, sans-serif'}
          fontSize={15}
          fontWeight={700}
        />
        <Txt
          ref={paymentStatus}
          text={'IDLE'}
          fill={'#a5a5c5'}
          fontFamily={'system-ui, sans-serif'}
          fontSize={11}
          fontWeight={800}
          letterSpacing={1}
        />
      </Rect>

      {/* INVENTORY SERVICE */}
      <Rect
        ref={inventoryRef}
        x={400}
        y={-150}
        width={200}
        height={90}
        radius={12}
        fill={'#0c0c14'}
        stroke={'#bd00ff'}
        lineWidth={3}
        shadowColor={'#bd00ff'}
        shadowBlur={10}
        scale={0}
        layout
        direction={'column'}
        alignItems={'center'}
        justifyContent={'center'}
        gap={5}
      >
        <Txt
          text={'INVENTORY SERVICE'}
          fill={'#ffffff'}
          fontFamily={'system-ui, sans-serif'}
          fontSize={15}
          fontWeight={700}
        />
        <Txt
          ref={inventoryStatus}
          text={'IN STOCK'}
          fill={'#a5a5c5'}
          fontFamily={'system-ui, sans-serif'}
          fontSize={11}
          fontWeight={800}
          letterSpacing={1}
        />
      </Rect>

      {/* SAGA ORCHESTRATOR (Coordinator) */}
      <Rect
        ref={sagaRef}
        x={0}
        y={80}
        width={260}
        height={100}
        radius={16}
        fill={'#0c0c14'}
        stroke={'#00e5ff'}
        lineWidth={4}
        shadowColor={'#00e5ff'}
        shadowBlur={15}
        scale={0}
        layout
        direction={'column'}
        alignItems={'center'}
        justifyContent={'center'}
        gap={4}
      >
        <Txt
          text={'SAGA COORDINATOR'}
          fill={'#ffffff'}
          fontFamily={'system-ui, sans-serif'}
          fontSize={16}
          fontWeight={800}
          letterSpacing={1.5}
        />
        <Txt
          text={'ORCHESTRATOR'}
          fill={'#00e5ff'}
          fontFamily={'system-ui, sans-serif'}
          fontSize={11}
          fontWeight={700}
          letterSpacing={1}
        />
      </Rect>

      {/* Data Packet with text tag */}
      <Circle
        ref={packetRef}
        width={24}
        height={24}
        fill={'#00ffcc'}
        shadowColor={'#00ffcc'}
        shadowBlur={15}
        opacity={0}
        layout
        alignItems={'center'}
        justifyContent={'center'}
      >
        <Txt
          ref={packetTxt}
          text={''}
          fill={'#ffffff'}
          fontFamily={'system-ui, sans-serif'}
          fontSize={10}
          fontWeight={800}
          y={-24}
          opacity={0}
        />
      </Circle>
    </Node>
  );

  // ANIMATION TIMELINE EXECUTION

  // 1. Entrance of Nodes
  yield* all(
    orderRef().scale(1, 1.0, easeOutBack),
    paymentRef().scale(1, 1.0, easeOutBack),
    inventoryRef().scale(1, 1.0, easeOutBack),
    sagaRef().scale(1, 1.0, easeOutBack)
  );

  // 2. Draw Wires
  yield* all(
    wireOrder().end(1, 0.8),
    wirePayment().end(1, 0.8),
    wireInventory().end(1, 0.8)
  );

  yield* waitFor(0.5);

  // -- Step 1: Order Service triggers order create -> notifies Saga Coordinator
  orderStatus().text('PENDING');
  packetRef().position([-400, -150]);
  packetTxt().text('ORDER_CREATED');
  yield* all(
    packetRef().opacity(1, 0.2),
    packetTxt().opacity(1, 0.2)
  );
  yield* packetRef().position([0, 80], 1.0, easeInOutCubic);
  yield* all(
    packetRef().opacity(0, 0.2),
    packetTxt().opacity(0, 0.2),
    sagaRef().scale(1.1, 0.15).to(1.0, 0.2)
  );

  // -- Step 2: Saga Coordinator requests Payment Service to charge
  packetRef().position([0, 80]);
  packetRef().fill('#00ffcc');
  packetRef().shadowColor('#00ffcc');
  packetTxt().text('PROCESS_PAYMENT');
  yield* all(
    packetRef().opacity(1, 0.2),
    packetTxt().opacity(1, 0.2)
  );
  yield* packetRef().position([0, -180], 1.0, easeInOutCubic);
  paymentStatus().text('CHARGED');
  paymentStatus().fill('#00ff66');
  yield* all(
    packetRef().opacity(0, 0.2),
    packetTxt().opacity(0, 0.2),
    paymentRef().stroke('#00ff66', 0.2),
    paymentRef().shadowColor('#00ff66', 0.2)
  );

  yield* waitFor(0.5);

  // -- Step 3: Saga Coordinator requests Inventory Service to reserve stock
  packetRef().position([0, 80]);
  packetTxt().text('RESERVE_STOCK');
  yield* all(
    packetRef().opacity(1, 0.2),
    packetTxt().opacity(1, 0.2)
  );
  yield* packetRef().position([400, -150], 1.0, easeInOutCubic);
  inventoryStatus().text('OUT OF STOCK');
  inventoryStatus().fill('#ff0055');
  yield* all(
    packetRef().opacity(0, 0.2),
    packetTxt().opacity(0, 0.2),
    inventoryRef().stroke('#ff0055', 0.2),
    inventoryRef().shadowColor('#ff0055', 0.2)
  );

  yield* waitFor(0.8);

  // -- Step 4: Inventory failure triggers Rollback! Payments refunded
  packetRef().position([400, -150]);
  packetRef().fill('#ffea00'); // Compensating action (yellow/orange)
  packetRef().shadowColor('#ffea00');
  packetTxt().text('OUT_OF_STOCK_ALERT');
  yield* all(
    packetRef().opacity(1, 0.2),
    packetTxt().opacity(1, 0.2)
  );
  yield* packetRef().position([0, 80], 1.0, easeInOutCubic);
  yield* all(
    packetRef().opacity(0, 0.2),
    packetTxt().opacity(0, 0.2),
    sagaRef().stroke('#ffea00', 0.2),
    sagaRef().shadowColor('#ffea00', 0.2)
  );

  yield* waitFor(0.5);

  // -- Step 5: Saga Coordinator compensating transaction -> Refund Payment
  packetRef().position([0, 80]);
  packetTxt().text('REFUND_PAYMENT');
  yield* all(
    packetRef().opacity(1, 0.2),
    packetTxt().opacity(1, 0.2)
  );
  yield* packetRef().position([0, -180], 1.0, easeInOutCubic);
  paymentStatus().text('REFUNDED');
  paymentStatus().fill('#ffea00');
  yield* all(
    packetRef().opacity(0, 0.2),
    packetTxt().opacity(0, 0.2),
    paymentRef().stroke('#ffea00', 0.2),
    paymentRef().shadowColor('#ffea00', 0.2)
  );

  yield* waitFor(0.5);

  // -- Step 6: Saga Coordinator compensating transaction -> Cancel Order
  packetRef().position([0, 80]);
  packetTxt().text('CANCEL_ORDER');
  yield* all(
    packetRef().opacity(1, 0.2),
    packetTxt().opacity(1, 0.2)
  );
  yield* packetRef().position([-400, -150], 1.0, easeInOutCubic);
  orderStatus().text('CANCELLED');
  orderStatus().fill('#ff0055');
  yield* all(
    packetRef().opacity(0, 0.2),
    packetTxt().opacity(0, 0.2),
    orderRef().stroke('#ff0055', 0.2),
    orderRef().shadowColor('#ff0055', 0.2)
  );

  yield* waitFor(1.5);
});
