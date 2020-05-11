import os
from pathlib import Path

OAT_FOLDER = Path.home() / ".oat"

if not os.path.exists(OAT_FOLDER):
    OAT_FOLDER.mkdir(parents=True, exist_ok=True)
