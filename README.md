# Willowbank Watershed Lab — website sources

Static sources for the lab's public website.

## Layout

```
content/publications/           one Markdown record per journal/conference entry
content/publications/workshops/ one Markdown record per workshop entry
public/publications.html        generated catalogue page (do not edit by hand)
data/release_status_export.json periodic release-status snapshot
scripts/build_catalog.py        catalogue generator
scripts/export_release_status.py release-status snapshot generator
```

## Building the catalogue

```bash
python scripts/build_catalog.py
```

The script reads the publication records and writes `public/publications.html`.
Generated files are committed so that the deployed site matches the sources.

## Release-status snapshots

`scripts/export_release_status.py` refreshes `data/release_status_export.json`
from repository metadata. The snapshot is informational; the per-project
repositories remain the place where release status is declared.
