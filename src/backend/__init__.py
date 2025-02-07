from pathlib import Path

PROJECT_PATH = Path(__file__).resolve().parents[2]
FRONT_PATH = PROJECT_PATH / "front"
TEMPLATES_PATH = PROJECT_PATH / "templates"

DIST_PATH = FRONT_PATH / "dist"
MANIFEST_PATH = DIST_PATH / "manifest.json"
