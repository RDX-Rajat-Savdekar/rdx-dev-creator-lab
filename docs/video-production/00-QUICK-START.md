# Quick start — portfolio video pipeline

Generic one-page flow for **long-form Manim explainers with phone VO**.  
Shorter or VO-free projects: see [projects/](projects/) for variants.

Replace `{project}` with your folder (e.g. `Aura/design-video`).

---

## Phase 0 — Lock story (before Manim)

```
1. STORY.md or HACKATHON-STORY.md — facts, rejected paths, never_claim list
2. SCRIPT.md — chapter beats + narration seeds
3. SCENE-PLAN.md — target timestamps (will drift — OK)
```

---

## Phase A — Plan & build (per chapter)

```
1. vo/sceneN.md        PLAY CHECKLIST + VO seeds (user edits checklists)
2. sceneN_actM.py      Layout plop → motion → play_actM(scene, state)
3. -ql preview         SceneNActMLayout + SceneNActM + SceneNFull
4. -qk 4K acts         manim -qk --frame_rate 60 per act
5. ffmpeg concat       output/sceneN_chapterN_2160p60.mp4 (absolute paths!)
6. build_act_timestamps.py → paste timeline into vo/sceneN.md
7. adjust_waits.py     optional — after read-aloud if holds feel wrong
```

**Default VO hold:** `scene.wait(5.5)` before terminal `FadeOut`. Tune after recording.

---

## Phase B — Record VO (phone)

```
1. python {project}/tools/build_teleprompter.py
2. python {project}/tools/serve.py
3. http://127.0.0.1:8765/prompter.html → Record tab
4. Save → {project}/.../audio_record_{project}/{chapter}{act}.m4a
```

Naming: two digits `CN` = chapter C, act N (e.g. `31` = ch3 act1).

---

## Phase C — Clean, transcribe, mux (no Resolve)

```bash
# Reference paths: Aura/design-video (adapt for your project)
python Aura/design-video/tools/process_vo_audio.py

Aura/design-video/.venv/bin/python Aura/design-video/tools/process_vo_audio.py --skip-process --transcribe

Aura/design-video/.venv/bin/python Aura/design-video/tools/mux_chapter_vo.py --all --banner

Aura/design-video/.venv/bin/python Aura/design-video/tools/build_full_film.py
```

Mux uses **hold last visible frame** — strips `FadeOut` black tails (`vo_video_fit.py`).

---

## Key rules

| Rule | Why |
|------|-----|
| Measured durations from 4K act MP4s | Plans drift |
| Absolute paths in ffmpeg concat lists | Relative paths break |
| Hold last frame in mux, not black tail | Acts end with `FadeOut` |
| `vo/sceneN.md` beats SCRIPT after first render | SCRIPT lags visuals |
| Agent inspects layout PNGs before user QA | `extract_act_frames.py` |

---

## Ship checklist

- [ ] Silent chapter concats (`*_2160p60.mp4`)
- [ ] Cleaned VO (`processed/chN_actM.wav`)
- [ ] `vo/vo_clips.json` + transcripts
- [ ] Chapter exports with VO + 2s banner
- [ ] Full film concat
- [ ] Journal entry in `{project}/journal.md`
