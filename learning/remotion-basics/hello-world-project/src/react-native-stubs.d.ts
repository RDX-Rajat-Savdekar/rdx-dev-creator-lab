/* eslint-disable */
// TypeScript stubs for React Native packages referenced by @shopify/react-native-skia internal sources
declare module "react-native" {
  export const View: any;
  export const StyleSheet: any;
  export type ViewStyle = any;
  export type TextStyle = any;
  export type ImageStyle = any;
  export type RegisteredStyle<T> = any;
  export type StyleProp<T> = any;
  
  // Specific exports required by @shopify/react-native-skia Platform layers
  export type NodeHandle = any;
  export const ViewComponent: any;
  export const Image: any;
  export const PixelRatio: any;
  export const Platform: any;
  export const findNodeHandle: any;
}

declare module "react-native-reanimated" {
  export const useSharedValue: any;
  export const useAnimatedStyle: any;
  export type SharedValue<T> = any;
}
