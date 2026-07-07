import { LoadSkia } from "@shopify/react-native-skia/src/web";
import { registerRoot } from "remotion";

(async () => {
  // Load the Skia WebAssembly binary before mounting the React tree
  await LoadSkia();
  
  // Dynamically import Root to ensure Skia WebAssembly is fully ready
  const { RemotionRoot } = await import("./Root");
  registerRoot(RemotionRoot);
})();
