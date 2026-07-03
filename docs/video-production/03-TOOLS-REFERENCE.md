# Tools reference

CLI tools for portfolio video production. **Full suite today:** `Aura/design-video/tools/`  
Copy or generalize paths when standing up a new project.

Paths below use `{repo}` = repo root and `{dv}` = `Aura/design-video` unless noted.

---

## Manim render

```bash
cd {project}/{manim_pkg}
{repo}/.venv/bin/manim -ql scenes/sceneN_actM.py SceneNActM
{repo}/.venv/bin/manim -qk --frame_rate 60 scenes/sceneN_actM.py SceneNActM
```

Celestia uses OpenGL: `uv run manim --renderer=opengl -qh scene3.py S3_Clip1_...`

---

## Planning & VO docs ({dv})

| Tool | Command |
|------|---------|
| Act timestamps | `python {dv}/vo/build_act_timestamps.py --chapter N --markdown` |
| Teleprompter | `python {dv}/tools/build_teleprompter.py` |
| Parse VO | `python {dv}/tools/parse_vo_docs.py` |

---

## Pacing ({dv})

| Tool | Command |
|------|---------|
| Show waits | `python {dv}/tools/adjust_waits.py --chapter N --show` |
| Bulk add | `python {dv}/tools/adjust_waits.py --chapter N --add 2.0` |
| Set one act | `python {dv}/tools/adjust_waits.py --chapter N --act M --set 6.2` |
| Extend holds | `python {dv}/tools/extend_act_holds.py --apply --concat` |

---

## Layout QA ({dv})

```bash
python {dv}/tools/extract_act_frames.py --scene sceneN_actM
```

---

## Prompter ({dv})

```bash
python {dv}/tools/serve.py
# → http://127.0.0.1:8765/prompter.html
```

---

## Audio + final assembly ({dv})

| Tool | Role |
|------|------|
| `process_vo_audio.py` | Clean phone clips; `--transcribe` for Whisper |
| `sync_vo_alignment.py` | Write hold/wait configs from transcripts |
| `mux_chapter_vo.py` | VO mux + `--banner` |
| `build_full_film.py` | Concat all chapter `_vo` exports |
| `chapter_banners.py` | 2s chapter title cards |
| `vo_video_fit.py` | Hold-frame logic (imported by mux) |

**Venv:** `{dv}/.venv` — Whisper + Pillow.

---

## Short-form / music (Aura 60s)

```bash
{repo}/.venv/bin/python Aura/manim/build_60s.py
{repo}/.venv/bin/python Aura/manim/add_music.py --music ... --volume 0.10
```

---

## Celestia stitch helper

```bash
cd celestia_presentation
uv run python build_scene1.py
```

---

## Dependencies

| Package | Where | For |
|---------|-------|-----|
| manim | repo `.venv` | All renders |
| ffmpeg | system | Video/audio |
| openai-whisper | project `.venv` | Transcription |
| pillow | project `.venv` | Banners |
