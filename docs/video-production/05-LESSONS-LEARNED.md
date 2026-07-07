# Lessons learned

Cross-project mistakes from portfolio video work in this repo.  
Project-specific details: per-project journals (e.g. [`Aura/journal.md`](../../Aura/journal.md)).

---

## Manim production

| Mistake | Fix |
|---------|-----|
| All beats in one Scene | One act/scene per file + layout plop first |
| Hand-drawn icons | SVG assets |
| `VideoMobject` unavailable / brittle | PyAV → `ImageMobject` updaters |
| Scaling groups with `Text` | Typography helpers; size plates, don't scale copy |
| ffmpeg concat relative paths | **Absolute paths** in list files |
| Blocking on plan duration targets | Visual-first; tune after VO |
| Agent asks user to spot layout | Agent runs frame extract + inspects PNGs |
| Monolith before review workflow | Layout scene before motion scene |

---

## Remotion production

| Mistake | Fix |
|---------|-----|
| CSS transitions (`transition: all`) in elements | Non-pure animation flickering. Drive styles purely via `interpolate` or `spring` mapped to `useCurrentFrame()`. |
| Importing media files from outside the project sandbox | Dev server throws `404`. Copy assets to the local `public/` directory and load them via the `staticFile()` helper. |
| Underscores `_` in composition IDs | Compiler crash. Use alphanumeric keys and hyphens `-` only. |
| Raw arrow symbols (`->`) in JSX | Webpack parse crash. Wrap in curly braces `{"->"}` or use HTML entities `&rarr;`. |
| Nested Canvas wrappers in `@remotion/skia` | Reconciler loop crash (`Should not already be working`). Render elements directly as children of Remotion's `<SkiaCanvas>`. |
| Raw TS library checks in node_modules (`react-native` types) | Compilation crash. Add stubs file `src/react-native-stubs.d.ts` and set `"noUnusedLocals": false` in `tsconfig.json`. |
| WebGL context failure in Chromium headless render | `failed to create webgl context: err 0`. Set `Config.setChromiumOpenGlRenderer("angle")` in `remotion.config.ts`. |

---

## VO and pacing

| Mistake | Fix |
|---------|-----|
| SCRIPT.md as timing truth | `vo/sceneN.md` + measured 4K durations |
| Extra pauses in recording for Manim | Trim/hold video, not longer VO silence |
| Resolve required | ffmpeg mux + Whisper |
| Extend video when VO longer → **black** hold | `vo_video_fit.py` — freeze last content frame |
| WAV length Δ vs speech | Whisper `speech_end` |
| Mislabeled act audio | Transcript vs PLAY CHECKLIST |

---

## Act structure (VO mux)

| Pattern | Mux handling |
|---------|--------------|
| `wait` → `FadeOut` | `content_end = duration − fade_run_time` |
| b-roll → blank `wait` | Hold last b-roll frame; strip blank tail |
| b-roll ends with fade | Strip fade; hold last content frame |

---

## Short-form / hybrid

| Mistake | Fix |
|---------|-----|
| EDM music under dense text | Documentary/ambient bed, low volume |
| Teammate VO on solo cut | Mute source; own narration or text only |
| Re-record when no device | Re-cut existing demo footage |

---

## Documentation

| Mistake | Fix |
|---------|-----|
| Decisions only in chat | Project `journal.md` + this playbook |
| Aura-only docs for repo-wide work | **`docs/video-production/`** — generic process |
| Stale act numbers in comments | Fix source + journal |

---

## Honesty (portfolio-wide)

- Match claims to fact records / STORY docs.  
- Separate **integrated** vs **trained**, **prototype** vs **production**.  
- B-roll proves product; Manim explains decisions.
