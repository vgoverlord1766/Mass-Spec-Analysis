from pathlib import Path
from mass_spec import load_config, import_data, process_data_main, pca, cluster_map, volcano_plot, comp_log2fc
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
final_py.attrs['run'] = 'pY'
final_pst.attrs['run'] = 'pST'
final_global.attrs['run'] = 'global'

'''
Plotting
'''
pca(analysis_output_path, plots_output_path, final_py, final_pst, final_global)

cluster_map(analysis_output_path, plots_output_path, final_py, final_pst, final_global)

volcano_plot(analysis_output_path, plots_output_path, final_py, final_pst, final_global)

comp_log2fc(analysis_output_path, plots_output_path, final_py, final_pst, final_global)
