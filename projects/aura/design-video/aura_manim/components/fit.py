"""Backward compat — ch 4–5 import ``fit_center`` from here. Ch 6+: use ``components.layout``."""

from __future__ import annotations

from components.layout import fit_center

__all__ = ["fit_center"]
