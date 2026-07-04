"""Aura capture pipeline — thin wrapper over ``workflow.aura_capture_pipeline``."""

from __future__ import annotations

from manim import Mobject, VGroup

from components.workflow import aura_capture_pipeline as _aura_capture_pipeline


def pipeline_stub_group() -> dict[str, Mobject]:
    """Backward-compatible entry point for scene2 act 4 and future chapters."""
    bits = _aura_capture_pipeline()
    return {
        "diagram": bits["diagram"],
        "nodes": bits["stage_columns"],
        "stages": bits["stages"],
        "arrows": bits["edges"],
        "edges": bits["edges"],
        "headers": bits["headers"],
        "chips": bits["annotations"],
    }
