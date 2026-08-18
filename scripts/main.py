from pathlib import Path
from mass_spec import load_config, import_data, process_data_main, z_score_main, pca
from mass_spec import settings


run_name = '20260713_PANC1_data'   # *** need to update per experiment ***

'''
Initialization
'''
# Import and globally load configs
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
CONFIG_PATH = PROJECT_ROOT / 'configs' / (run_name + '.yaml')

config = load_config(CONFIG_PATH)
settings.init(config)

input_path = PROJECT_ROOT / 'data' / run_name
processed_output_path = PROJECT_ROOT / 'outputs' / run_name / 'post_processing'
analysis_output_path = PROJECT_ROOT / 'outputs' / run_name / 'post_analysis'
plots_output_path = PROJECT_ROOT / 'outputs' / run_name / 'plots'

# Import all data from csv to dataframes
py_data, pst_data, global_data, sup_data, py_pep_data, pst_pep_data = import_data(str(PROJECT_ROOT / Path(input_path)))

'''
Filter and clean data
'''
final_py, final_pst, final_global = process_data_main(processed_output_path, py_data, pst_data, global_data, sup_data,
                                                      py_pep_data, pst_pep_data)
print('b')
'''
Data analysis
'''
z_py, z_pst, z_global = z_score_main(analysis_output_path, final_py, final_pst, final_global)
z_py.attrs['run'] = 'pY'
z_pst.attrs['run'] = 'pST'
z_global.attrs['run'] = 'global'

print('a')
'''
Plotting
'''
[pca(plots_output_path, x) for x in [z_py, z_pst, z_global]]
