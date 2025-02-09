from pathlib import Path

# Backend global variables
PROJECT_PATH = Path(__file__).resolve().parents[2]
FRONT_PATH = PROJECT_PATH / "front"
TEMPLATES_PATH = PROJECT_PATH / "templates"

# Front global variables
DIST_PATH = FRONT_PATH / "dist"
ASSETS_PATH = DIST_PATH / "assets"
MANIFEST_PATH = DIST_PATH / ".vite" / "manifest.json"
VITE_DEV_SERVER = "http://localhost:5173"
