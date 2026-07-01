"""
Chapter 0 — FULL ASSEMBLY (not built yet)

After each act file is approved:
  scene0_act1.py … scene0_act6.py  →  import motion into one Scene here.

──────────────────────────────────────────────────────────────────────────────
Cross-act reuse (do this as acts accumulate)

  Per-act files (`scene0_actN.py`)
    · Own PLAY checklist + Scene0ActNLayout + Scene0ActN
    · Act-specific layout only (what’s new this beat)

  Shared components (`components/`)
    · Introduced when act 2+ needs the same Mobject again
    · Example: `components/team.py` — TEAM roster, team_grid (act 2), lane (act 3)

  Do NOT import whole previous Scene classes — import **builders**:
    from components.team import team_grid, team_contribution_lane

  Optional continuity animation (when you want it):
    grid = team_grid()
    lane = team_contribution_lane()
    self.play(Transform(grid, lane))   # same four people, new metaphor

  `scene0_full.py` only concatenates approved act motions — no new visuals.
"""

# from scenes.scene0_act1 import ...  (wire when act 1 locked)
