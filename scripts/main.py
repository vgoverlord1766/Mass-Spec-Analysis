from pathlib import Path
from mass_spec import load_config, import_data, process_data
import pandas as pd


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
CONFIG_PATH = PROJECT_ROOT / 'configs' / '20260713.yaml'

config = load_config(CONFIG_PATH)

input_path = config['paths']['inputs']
output_path = config['paths']['outputs']

channels = config['channels']
samples = config['samples']

py_data, pst_data, global_data, sup_data, py_pep_data, pst_pep_data = import_data(str(PROJECT_ROOT / Path(input_path)))

final_py, final_pst, final_global = process_data(py_data, pst_data, global_data, sup_data, py_pep_data, pst_pep_data,
                                                 config)
print(type(final_py))

final_py.to_csv('final_py.csv', index=False)
