import {makeProject} from '@motion-canvas/core';

import stage1 from './scenes/stage1_packet_router?scene';
import stage2 from './scenes/stage2_flex_cluster?scene';
import stage3 from './scenes/stage3_kafka_broker?scene';
import stage4 from './scenes/stage4_bst_traversal?scene';
import stage5 from './scenes/stage5_saga_orchestrator?scene';

export default makeProject({
  scenes: [stage1, stage2, stage3, stage4, stage5],
});
