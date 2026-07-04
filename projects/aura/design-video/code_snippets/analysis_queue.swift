// Serial — never block the realtime tap
private let analysisQueue = DispatchQueue(
    label: "com.aura.AnalysisQueue"
)
analysisQueue.async {
    self.classifySound(buffer)
}
