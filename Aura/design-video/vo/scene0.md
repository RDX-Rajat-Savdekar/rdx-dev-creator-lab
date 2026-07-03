# Chapter 0 — Problem + hackathon + sphere POC

> **YouTube chapter:** *The problem*  
> **Render:** [`output/scene0_chapter0_2160p60.mp4`](../output/scene0_chapter0_2160p60.mp4)  
> **Total duration:** `1:14.1` (74.1 s measured) · **SCENE-PLAN target:** `0:00` → `1:05` (65 s)  
> **VO status:** draft (read-aloud pending) · **Measured:** 1:14.1 (74.1 s) — trim waits to ~1:05
> **Pace target:** ~140 wpm (~173 words fits 74 s)

**Source acts:** `aura_manim/scenes/scene0_act{1…6}.py`  
**Script seed:** [`SCRIPT.md`](../SCRIPT.md) Chapter 0 — **note:** act 3 narration there is stale (`All code: Rajat`); use this file.

---

## Act timeline (2160p60 · 2026-07-02)

| Act | Start | End | Dur | On-screen label | Manim file |
|-----|-------|-----|-----|-----------------|------------|
| 1 | 0:00.0 | 0:15.2 | 15.2s | Situational audio gap | `scene0_act1.py` |
| 2 | 0:15.2 | 0:26.6 | 11.4s | 24h hackathon · Oct 2025 | `scene0_act2.py` |
| 3 | 0:26.6 | 0:40.6 | 14.0s | Team-built · shared code | `scene0_act3.py` |
| 4 | 0:40.6 | 0:55.5 | 14.9s | Day 0: sphere POC | `scene0_act4.py` |
| 5 | 0:55.5 | 1:04.1 | 8.6s | System design · prototype (+ D1 B-roll) | `scene0_act5.py` |
| 6 | 1:04.1 | 1:14.1 | 10.0s | Aura · visionOS · on-device | `scene0_act6.py` |

*Refresh:* `python Aura/design-video/vo/build_act_timestamps.py --chapter 0 --markdown`

---

## Act descriptions

### Act 1 — Noisy room · situational audio gap (`0:00` → `0:15`)

**What the viewer sees**

- Room frame + corner noise ripples  
- Three columns: speech bubble + sound icon each (`Hey…`/bell · `…wait`/alert · `Behind you!`/wave)  
- Columns replaced by six yellow `?` — context lost  
- Bottom label: **Situational audio gap**

**Story beat**

- Problem statement: deaf/HoH users miss *speech* and *environmental* context in noise.

---

### Act 2 — Hackathon frame (`0:15` → `0:27`)

**What the viewer sees**

- Clock SVG + **24h** (left)  
- **Oct 2025** · LA Tech Week · USC ISI  
- 2×2 team role cards (Lead Developer highlighted)  
- Bottom label: **24h hackathon · Oct 2025**

**Story beat**

- When / where / team frame. Four cards = roles on the project; VO says **three-person team**.

---

### Act 3 — Shared codebase (`0:27` → `0:41`)

**What the viewer sees**

- Git-style trunk: **shared codebase**  
- Line splits into four sections; each dev icon merges in (green pulse + name)  
- Top note: *Everyone contributed to the codebase*  
- Bottom label: **Team-built · shared code**

**Story beat**

- Honest credit: team-built repo, not solo-code erasure. Lead dev highlighted in act 2; merges here.

---

### Act 4 — Sphere POC (`0:41` → `0:56`)

**What the viewer sees**

- *First Vision Pro build*  
- Neutral sphere → cue `"red"` → sphere turns red  
- Cue *louder* + volume bars → sphere + bars **pulsate 3×**  
- Bottom label: **Day 0: sphere POC**

**Story beat**

- Day-zero shakedown: deploy, mic, speech, spatial rendering before the real app.

---

### Act 5 — Prototype disclaimer + live demo (`0:56` → `1:04`)

**What the viewer sees**

- Title: **System design · prototype** / subtitle **Hackathon Prototype** (~3.3 s hold)  
- Card fades out → **4 s D1 B-roll** (`clips/D1_live-en-captions.mp4`) — real live EN captions on Vision Pro  
- Fade to black → act 6

**Story beat**

- Scope disclaimer + proof hook (captions actually worked in the hackathon demo).

---

### Act 6 — Aura teaser (`1:04` → `1:14`)

**What the viewer sees**

- **Aura** · visionOS · on-device  
- Vision Pro silhouette (left)  
- Mic tap → **Speech** + **SoundAnalysis** branches + *on-device* label  
- Fade out — end chapter 0

**Story beat**

- Product one-liner; sets up chapters 1–3 (on-device dual pipeline).

---

## VO draft (first read-aloud)

Read over [`scene0_chapter0_2160p60.mp4`](../output/scene0_chapter0_2160p60.mp4). Adjust pacing before recording.

### Act 1 (`0:00` → `0:15`) — 15.2 s · ~36 words

> If you're deaf or hard of hearing, a noisy room isn't just loud — you miss what was said and what happened around you. Speech and environmental sounds both carry context.

*Land “carry context” as the `?` marks appear (~0:08). Use the long hold (~0:09–0:15) for the last line or breathe before act 2.*

---

### Act 2 (`0:15` → `0:27`) — 11.4 s · ~26 words

> That's the problem we chased at a twenty-four-hour hackathon in October twenty twenty-five — LA Tech Week at USC ISI. Three-person team.

*Hit “twenty-four-hour” as the clock appears; “three-person team” as the grid fills.*

---

### Act 3 (`0:27` → `0:41`) — 14.0 s · ~30 words

> Everyone contributed to the shared codebase. I led development; teammates owned README, design, and the on-camera demo. One repo — four merges.

*Stretch across green merge pulses; finish on **Team-built · shared code** label.*

---

### Act 4 (`0:41` → `0:56`) — 14.9 s · ~42 words

> It was also our first build on Vision Pro. Before Aura, we shipped a tiny proof of concept: say “red,” the sphere turns red; speak louder, it grows. That proved deploy, microphone, speech, and spatial rendering — before we built the real app.

*Sync “red” / “louder” to color change and pulsate beats.*

---

### Act 5 (`0:56` → `1:04`) — 8.6 s · ~28 words

> This video is the system design story — what we tried, what we cut, and what actually shipped. Hackathon prototype — not a production app.

*Speak during the title card (first ~4 s). **Optional:** stay silent during D1 B-roll so the demo speaks for itself, or add: “Live captions, on device.”*

---

### Act 6 (`1:04` → `1:14`) — 10.0 s · ~22 words

> Aura runs on Apple Vision Pro: live speech transcription plus environmental sound classification — entirely on-device.

*Finish as the pipeline stub completes; hold through fade.*

---

**Chapter totals:** ~184 words · ~79 s at 140 wpm · **~74 s clip** → read slightly brisk or trim ~10 words in act 4/5.

**Plain export for teleprompter** (concatenate acts 1–6 blocks above, or use `tools/prompter.html`).

---

## Trim notes

| Issue | Suggested fix |
|-------|----------------|
| **74 s vs 65 s plan** | After VO lock: cut `self.wait()` in act 1 (7.2 s hold), act 2 (5.3 s), act 4 (7.0 s), act 6 (5.0 s) — ~15 s removable |
| Act 1 long tail | `scene0_act1.py` line ~`scene.wait(7.2)` → 4.0 after read-aloud |
| SCRIPT.md act 3 row | Replace “I wrote all of the code…” with team-built line from this doc |
| Act 5 VO over B-roll | Decide silent vs one line before final record |

---

## Recording notes

- **Punch-ins:** Per act is fine — concat video stays fixed; align in Resolve to act start times in table above  
- **B-roll audio:** D1 source has demo audio — mute in Resolve if VO overlaps act 5  
- **Music:** Documentary bed @ 0.05–0.07 under VO (post-assembly)  
- **Next chapter:** Copy [`_TEMPLATE.md`](_TEMPLATE.md) → `scene1.md` when ch 1 acts exist
