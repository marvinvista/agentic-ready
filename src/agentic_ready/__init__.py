"""Smoke-test B2B product surfaces for agent readiness."""

from .audit import audit_target
from .models import Report

__all__ = ["Report", "audit_target"]

__version__ = "0.1.0"
