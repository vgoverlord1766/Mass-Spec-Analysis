from pathlib import Path
from mass_spec.io import load_config

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
CONFIG_PATH = PROJECT_ROOT / 'configs' / '20260713.yaml'
OUTPUT_PATH = PROJECT_ROOT / 'outputs' / '20260713.yaml'

config = load_config(CONFIG_PATH)

