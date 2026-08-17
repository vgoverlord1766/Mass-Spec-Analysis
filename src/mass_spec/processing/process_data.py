from mass_spec.processing import *
from mass_spec import settings
import pandas as pd


def process_data(raw_py, raw_pst, raw_global, raw_corr, py_pep_data, pst_pep_data):
    samples = settings.SAMPLES
    filtered_corr = filtering(raw_corr, 'corr')
    summed_corr = summing(filtered_corr)
    corrections = calc_corrections(summed_corr)

    # pY processing
    filtered_py = filtering(raw_py, 'pY')
    summed_py = summing(filtered_py)
    fmc_py = fix_missed_cleavages(summed_py)
    final_py = mod_abs_pos(fmc_py, py_pep_data)
    final_py[samples] = final_py[samples].div(corrections, axis=1)

    # pST processing
    filtered_pst = filtering(raw_pst, 'pST')
    summed_pst = summing(filtered_pst)
    fmc_pst = fix_missed_cleavages(summed_pst)
    final_pst = mod_abs_pos(fmc_pst, pst_pep_data)
    final_pst[samples] = final_pst[samples].div(corrections, axis=1)

    # Global processing
    filtered_global = filtering(raw_global, 'global')
    final_global = global_summing(filtered_global)
    final_global[samples] = final_global[samples].div(corrections, axis=1)

    return final_py, final_pst, final_global


def process_data_main(processed_output_path, py_data, pst_data, global_data, sup_data, py_pep_data, pst_pep_data):
    if not processed_output_path.exists():
        processed_output_path.mkdir(parents=True, exist_ok=True)
        final_py, final_pst, final_global = process_data(
            py_data, pst_data, global_data, sup_data, py_pep_data, pst_pep_data
        )
        final_py.to_csv(processed_output_path / 'processed_pY.csv', index=False)
        final_pst.to_csv(processed_output_path / 'processed_pST.csv', index=False)
        final_global.to_csv(processed_output_path / 'processed_global.csv', index=False)
    else:
        final_py = pd.read_csv(processed_output_path / 'processed_pY.csv')
        final_pst = pd.read_csv(processed_output_path / 'processed_pST.csv')
        final_global = pd.read_csv(processed_output_path / 'processed_global.csv')

    return final_py, final_pst, final_global

