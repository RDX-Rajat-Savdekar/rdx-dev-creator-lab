// MicrophoneMonitor.swift — AVAudioEngine tap
inputNode.installTap(
    onBus: 0, bufferSize: 4096, format: format
) { buffer, _ in
    self.processAudioBuffer(buffer)
}
