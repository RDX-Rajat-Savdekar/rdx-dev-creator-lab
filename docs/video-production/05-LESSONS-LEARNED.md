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
