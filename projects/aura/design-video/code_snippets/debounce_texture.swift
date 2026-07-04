// Texture bake — decouple SwiftUI layout from 90 Hz loop
private let debounceInterval: TimeInterval = 0.1
if now.timeIntervalSince(lastBake) >= debounceInterval {
    bakeCaptionTexture()
}
