import {Circle, makeScene2D, Rect, Grid, Txt, Node, Line, Code, lines} from '@motion-canvas/2d';
import {createRef, all, easeInOutCubic, easeOutBack, waitFor} from '@motion-canvas/core';

export default makeScene2D(function* (view) {
  // Tree Nodes references
  const node10 = createRef<Circle>();
  const node5 = createRef<Circle>();
  const node15 = createRef<Circle>();
  const node3 = createRef<Circle>();
  const node7 = createRef<Circle>();

  // Tree Lines references
  const line10_5 = createRef<Line>();
  const line10_15 = createRef<Line>();
  const line5_3 = createRef<Line>();
  const line5_7 = createRef<Line>();

  // Code block reference
  const codeRef = createRef<Code>();

  const bstCode = `\
function inorder(node) {
  if (!node) return;
  inorder(node.left);
  visit(node);
  inorder(node.right);
}`;

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

      {/* BST Connections (initially draw progress end={0}) */}
      <Line
        ref={line10_5}
        points={[[-300, -150], [-420, -20]]}
        stroke={'#3f3f5c'}
        lineWidth={4}
        end={0}
      />
      <Line
        ref={line10_15}
        points={[[-300, -150], [-180, -20]]}
        stroke={'#3f3f5c'}
        lineWidth={4}
        end={0}
      />
      <Line
        ref={line5_3}
        points={[[-420, -20], [-480, 110]]}
        stroke={'#3f3f5c'}
        lineWidth={4}
        end={0}
      />
      <Line
        ref={line5_7}
        points={[[-420, -20], [-360, 110]]}
        stroke={'#3f3f5c'}
        lineWidth={4}
        end={0}
      />

      {/* BST Nodes (Centered coordinates, initial scale={0}) */}
      
      {/* Root Node (10) */}
      <Circle
        ref={node10}
        x={-300}
        y={-150}
        width={75}
        height={75}
        fill={'#0c0c14'}
        stroke={'#00e5ff'}
        lineWidth={3}
        shadowColor={'#00e5ff'}
        shadowBlur={10}
        scale={0}
      >
        <Txt
          text={'10'}
          fill={'#ffffff'}
          fontFamily={'system-ui, sans-serif'}
          fontSize={20}
          fontWeight={700}
        />
      </Circle>

      {/* Left Node (5) */}
      <Circle
        ref={node5}
        x={-420}
        y={-20}
        width={75}
        height={75}
        fill={'#0c0c14'}
        stroke={'#bd00ff'}
        lineWidth={3}
        shadowColor={'#bd00ff'}
        shadowBlur={10}
        scale={0}
      >
        <Txt
          text={'5'}
          fill={'#ffffff'}
          fontFamily={'system-ui, sans-serif'}
          fontSize={20}
          fontWeight={700}
        />
      </Circle>

      {/* Right Node (15) */}
      <Circle
        ref={node15}
        x={-180}
        y={-20}
        width={75}
        height={75}
        fill={'#0c0c14'}
        stroke={'#bd00ff'}
        lineWidth={3}
        shadowColor={'#bd00ff'}
        shadowBlur={10}
        scale={0}
      >
        <Txt
          text={'15'}
          fill={'#ffffff'}
          fontFamily={'system-ui, sans-serif'}
          fontSize={20}
          fontWeight={700}
        />
      </Circle>

      {/* Left Leaf Node (3) */}
      <Circle
        ref={node3}
        x={-480}
        y={110}
        width={75}
        height={75}
        fill={'#0c0c14'}
        stroke={'#ff0055'}
        lineWidth={3}
        shadowColor={'#ff0055'}
        shadowBlur={10}
        scale={0}
      >
        <Txt
          text={'3'}
          fill={'#ffffff'}
          fontFamily={'system-ui, sans-serif'}
          fontSize={20}
          fontWeight={700}
        />
      </Circle>

      {/* Right Leaf Node (7) */}
      <Circle
        ref={node7}
        x={-360}
        y={110}
        width={75}
        height={75}
        fill={'#0c0c14'}
        stroke={'#ff0055'}
        lineWidth={3}
        shadowColor={'#ff0055'}
        shadowBlur={10}
        scale={0}
      >
        <Txt
          text={'7'}
          fill={'#ffffff'}
          fontFamily={'system-ui, sans-serif'}
          fontSize={20}
          fontWeight={700}
        />
      </Circle>

      {/* CODE PANEL CONTAINER */}
      <Rect
        x={280}
        y={0}
        width={540}
        height={320}
        radius={16}
        fill={'#0c0c14'}
        stroke={'#3f3f5c'}
        lineWidth={2.5}
        padding={24}
        layout
        direction={'column'}
        alignItems={'stretch'}
      >
        <Txt
          text={'BST IN-ORDER TRAVERSAL'}
          fill={'#a5a5c5'}
          fontFamily={'system-ui, sans-serif'}
          fontSize={14}
          fontWeight={800}
          letterSpacing={1.5}
          margin={[0, 0, 16, 0]}
        />
        <Code
          ref={codeRef}
          code={bstCode}
          fontSize={16}
          fontFamily={'Fira Code, Courier New, monospace'}
          lineHeight={24}
          opacity={0}
        />
      </Rect>
    </Node>
  );

  // ANIMATION EXECUTION

  // 1. Entrance of BST Nodes & Code panel
  yield* all(
    node10().scale(1, 1.0, easeOutBack),
    node5().scale(1, 1.0, easeOutBack),
    node15().scale(1, 1.0, easeOutBack),
    node3().scale(1, 1.0, easeOutBack),
    node7().scale(1, 1.0, easeOutBack),
    codeRef().opacity(1, 0.8)
  );

  // 2. Draw connections
  yield* all(
    line10_5().end(1, 0.6),
    line10_15().end(1, 0.6),
    line5_3().end(1, 0.6),
    line5_7().end(1, 0.6)
  );

  yield* waitFor(0.8);

  // 3. Traversal simulation mapping visual nodes to syntax code lines selection

  // -- Step 1: Call inorder(10)
  yield* all(
    codeRef().selection(lines(0, 1), 0.4),
    node10().stroke('#00ff66', 0.4),
    node10().shadowColor('#00ff66', 0.4)
  );
  yield* waitFor(0.6);

  // -- Step 2: inorder(10.left) -> call inorder(5)
  yield* all(
    codeRef().selection(lines(2), 0.4),
    line10_5().stroke('#00ff66', 0.4)
  );
  yield* all(
    node5().stroke('#00ff66', 0.4),
    node5().shadowColor('#00ff66', 0.4)
  );
  yield* waitFor(0.6);

  // -- Step 3: inorder(5.left) -> call inorder(3)
  yield* all(
    codeRef().selection(lines(2), 0.4),
    line5_3().stroke('#00ff66', 0.4)
  );
  yield* all(
    node3().stroke('#00ff66', 0.4),
    node3().shadowColor('#00ff66', 0.4)
  );
  yield* waitFor(0.6);

  // -- Step 4: inorder(3.left) -> null. visit(3)
  yield* all(
    codeRef().selection(lines(3), 0.4),
    node3().fill('#00ff66', 0.3),
    node3().scale(1.15, 0.15).to(1.0, 0.2)
  );
  yield* waitFor(0.8);

  // -- Step 5: inorder(3.right) -> null. Return. visit(5)
  yield* all(
    codeRef().selection(lines(3), 0.4),
    node5().fill('#00ff66', 0.3),
    node5().scale(1.15, 0.15).to(1.0, 0.2)
  );
  yield* waitFor(0.8);

  // -- Step 6: inorder(5.right) -> call inorder(7)
  yield* all(
    codeRef().selection(lines(4), 0.4),
    line5_7().stroke('#00ff66', 0.4)
  );
  yield* all(
    node7().stroke('#00ff66', 0.4),
    node7().shadowColor('#00ff66', 0.4)
  );
  yield* waitFor(0.6);

  // -- Step 7: inorder(7.left) -> null. visit(7)
  yield* all(
    codeRef().selection(lines(3), 0.4),
    node7().fill('#00ff66', 0.3),
    node7().scale(1.15, 0.15).to(1.0, 0.2)
  );
  yield* waitFor(0.8);

  // -- Step 8: inorder(7.right) -> null. Return. Return. visit(10)
  yield* all(
    codeRef().selection(lines(3), 0.4),
    node10().fill('#00ff66', 0.3),
    node10().scale(1.15, 0.15).to(1.0, 0.2)
  );
  yield* waitFor(0.8);

  // -- Step 9: inorder(10.right) -> call inorder(15)
  yield* all(
    codeRef().selection(lines(4), 0.4),
    line10_15().stroke('#00ff66', 0.4)
  );
  yield* all(
    node15().stroke('#00ff66', 0.4),
    node15().shadowColor('#00ff66', 0.4)
  );
  yield* waitFor(0.6);

  // -- Step 10: inorder(15.left) -> null. visit(15)
  yield* all(
    codeRef().selection(lines(3), 0.4),
    node15().fill('#00ff66', 0.3),
    node15().scale(1.15, 0.15).to(1.0, 0.2)
  );
  yield* waitFor(0.8);

  // Select all code lines to finish
  yield* codeRef().selection(lines(0, 5), 0.4);
  yield* waitFor(1.5);
});
