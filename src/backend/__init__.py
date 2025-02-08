from pathlib import Path

PROJECT_PATH = Path(__file__).resolve().parents[2]
FRONT_PATH = PROJECT_PATH / "front"
TEMPLATES_PATH = PROJECT_PATH / "templates"

DIST_PATH = FRONT_PATH / "dist"
ASSETS_PATH = DIST_PATH / "assets"
MANIFEST_PATH = DIST_PATH / ".vite" / "manifest.json"
