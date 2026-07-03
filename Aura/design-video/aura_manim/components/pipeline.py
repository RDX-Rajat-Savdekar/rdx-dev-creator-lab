"""Full dual-pipeline diagram — chapter 3 (extends ``workflow``)."""

from __future__ import annotations

from manim import Mobject, VGroup

from components.workflow import aura_capture_pipeline


def dual_pipeline_group() -> dict[str, Mobject]:
    """Mic tap → Speech + SoundAnalysis → queue → UI — same topology as ch 2 teaser."""
    bits = aura_capture_pipeline()
    return {
        "diagram": bits["diagram"],
        "stages": bits["stages"],
        "edges": bits["edges"],
        "stage_columns": bits["stage_columns"],
        "headers": bits["headers"],
    }
