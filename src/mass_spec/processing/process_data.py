from mass_spec.processing import *


def main(raw_py, raw_pst, raw_global, raw_corr, py_pep_data, pst_pep_data, samples):
    filtered_corr = filtering(raw_corr, 'corr')
    corrections = calc_corrections(filtered_corr)

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
