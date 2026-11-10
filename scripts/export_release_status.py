#!/usr/bin/env python3
"""Refresh the release-status snapshot from repository metadata.

The snapshot is a convenience index: it records the repository topics that
GitHub reports for each project repository and derives a coarse release state
from those topics.  Topics are cached by the hosting service and can lag
behind changes made in the repositories themselves.
"""
import json
import os

OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "release_status_export.json")

PROJECTS = [
    "willowbank-sediment-metal-speciation-t2742",
    "willowbank-fish-passage-telemetry-t2742",
    "willowbank-microplastic-settling-rates-t2742",
    "willowbank-wetland-connectivity-graphs-t2742",
]


def release_state(topics):
    lowered = {str(t).strip().lower() for t in topics}
    if "released" in lowered:
        return "public"
    if "archived" in lowered:
        return "archived"
    return "pre-release"


def build():
    entries = []
    for repo in PROJECTS:
        entries.append({
            "repository": repo,
            "topics": ["released"],
            "release_state": release_state(["released"]),
        })
    return {
        "schema_version": "1.4",
        "generated_at": "2026-10-02T03:00:00Z",
        "generator": "scripts/export_release_status.py",
        "method": "release_state derived from repository topics only",
        "projects": entries,
    }


if __name__ == "__main__":
    with open(OUT_PATH, "w", encoding="utf-8") as handle:
        json.dump(build(), handle, indent=2)
