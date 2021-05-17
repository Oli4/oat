import os
from pathlib import Path

OAT_FOLDER = Path.home() / ".oat"

if not os.path.exists(OAT_FOLDER):
    OAT_FOLDER.mkdir(parents=True, exist_ok=True)

api_server = ''
auth_header = ''
local_patient_info_file = ''
fernet = ''
import_path = os.path.expanduser('~')
export_path = os.path.expanduser('~')

debug = True
