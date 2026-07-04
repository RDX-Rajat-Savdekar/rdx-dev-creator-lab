// MicrophoneMonitor.swift — bridge ML delegate to @Published UI
// Source: Aura-Vision-Pro/Aura/Monitoring/MicrophoneMonitor.swift

func speechRecognizer(
    _ recognizer: SFSpeechRecognizer,
    didRecognize result: SFSpeechRecognitionResult
) {
    let text = result.bestTranscription.formattedString
    Task { @MainActor in
        self.captionText = text  // @Published
    }
}
