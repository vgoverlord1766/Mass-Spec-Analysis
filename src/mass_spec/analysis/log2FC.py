import numpy as np
import pandas as pd
from scipy.stats import stats, false_discovery_control
from mass_spec import settings
from pathlib import Path


def main_log2fc(analysis_output_path, final_py, final_pst, final_global):
    pair = settings.LOG2FC_PAIR
    samples = settings.SAMPLES
    if not Path(analysis_output_path / 'log2fc_pY.csv').is_file():
        analysis_output_path.mkdir(parents=True, exist_ok=True)
        log2fc_py, log2fc_pst, log2fc_global = [calc_log2fc(df, pair, samples) for df in [final_py, final_pst,
                                                                                          final_global]]
        log2fc_py.to_csv(analysis_output_path / 'log2fc_pY.csv', index=False)
        log2fc_pst.to_csv(analysis_output_path / 'log2fc_pst.csv', index=False)
        log2fc_global.to_csv(analysis_output_path / 'log2fc_global.csv', index=False)
    else:
        log2fc_py = pd.read_csv(analysis_output_path / 'log2fc_pY.csv')
        log2fc_pst = pd.read_csv(analysis_output_path / 'log2fc_pst.csv')
        log2fc_global = pd.read_csv(analysis_output_path / 'log2fc_global.csv',)

    return log2fc_py, log2fc_pst, log2fc_global


def calc_log2fc(data, pair, samples):
    data = data.replace(0, 100)
    data = data.rename(columns={
        col: col.split(' ')[1]
        for col in samples
    })

    numer = pair[0]  # numerator for log2fc
    denom = pair[1]  # denominator for log2fc

    data['log2FC'] = np.log2(data[numer].mean(axis=1) / data[denom].mean(axis=1))
    data[numer + '_mean'] = np.log2(data[numer].mean(axis=1))
    data[denom + '_mean'] = np.log2(data[denom].mean(axis=1))

    p_values = []
    for index, row in data.iterrows():
        denom_data = np.log2(row[denom].values.astype(np.float64))
        numer_data = np.log2(row[numer].values.astype(np.float64))

        res = stats.ttest_ind(numer_data, denom_data, equal_var=False)
        p_val = float(res.pvalue)
        if np.isnan(p_val):
            p_val = 1.0

        p_values.append(p_val)

    adjusted_p = false_discovery_control(p_values, method='bh')

    data['p_value'] = adjusted_p
    data['p_value'] = data['p_value'].fillna(1.0)
    data['-log10_p'] = np.where(data['p_value'] > 0, -np.log10(data['p_value']), 0)

    return data
