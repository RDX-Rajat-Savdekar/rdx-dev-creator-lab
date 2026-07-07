# Remotion Stage 5: Data Integration & Custom Dashboards 📊📉

Welcome to Stage 5! In this stage, we focus on **animating dynamic datasets**. When building technical videos or SaaS updates, you often need to show telemetry dashboards, latency spikes, or usage growth charts.

---

## 🗺️ What You Are Learning

### 1. Mapping Arrays to SVG Coordinates
To draw a line chart inside an SVG, we map data indices $(x)$ and values $(y)$ to standard pixel coordinates:
* **X-Axis Mapping**:
  $$\text{pixel}_x = \text{padding} + \left( \frac{\text{index}}{\text{totalPoints} - 1} \right) \times (\text{width} - 2 \times \text{padding})$$
* **Y-Axis Mapping**:
  $$\text{pixel}_y = \text{height} - \text{padding} - \left( \frac{\text{value}}{\text{maxValue}} \right) \times (\text{height} - 2 \times \text{padding})$$

By converting a data array into an SVG path string (like `M x1 y1 L x2 y2 ...`), we can draw a perfect vector chart!

---

### 2. Time-Based Data Reveal (The Scanning Laser)
To show a graph drawing itself over time:
- We calculate how many data points are revealed at the current `frame`.
- If the dataset has 100 points and the animation is 100 frames, we slice the array to only draw points up to `frame`:
  ```typescript
  const visibleData = fullDataset.slice(0, Math.floor(frame));
  ```
- This gives us a scrolling/scanning chart effect! We can draw a vertical "laser line" exactly at the latest data point to highlight the current value.

---

### 3. Dynamic Telemetry Calculation
Since we have access to the data subset visible at the current frame, we can compute stats like **current latency**, **max latency so far**, and **average latency** dynamically on the screen:
```typescript
const currentVal = visibleData[visibleData.length - 1];
const maxValSoFar = Math.max(...visibleData);
```
These values will count up in real-time as the graph scans forward, creating a high-fidelity visual experience.

---

## 🛠️ Files to Explore

1. **[SystemDashboard.tsx](file:///Users/rajatsavdekar/Documents/GitHub/rdx-dev-creator-lab/learning/remotion-basics/hello-world-project/src/Stage5_Data/SystemDashboard.tsx)**
   * *What it does:* Renders a Sci-Fi system telemetry dashboard with a scanning SVG line chart, gradient area fill, and dynamic latency calculations. Includes color-shifting highlights based on latency thresholds.
