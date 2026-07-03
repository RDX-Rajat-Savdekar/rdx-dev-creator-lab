// Utterance boundary — gap longer than 1.1s starts a new chunk
let pauseThreshold: TimeInterval = 1.1
if gapSinceLastToken > pauseThreshold {
    flushUtterance()
}
