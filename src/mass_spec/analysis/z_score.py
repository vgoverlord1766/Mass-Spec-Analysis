from mass_spec import settings
from scipy.stats import zscore
import pandas as pd


def z_score(data):
    samples = settings.SAMPLES
    data[samples] = zscore(data[samples], axis=1, ddof=1)
    return data


def z_score_main(analysis_output_path, final_py, final_pst, final_global):
    if not analysis_output_path.exists():
        analysis_output_path.mkdir(parents=True, exist_ok=True)
        z_py, z_pst, z_global = [z_score(df) for df in [final_py, final_pst, final_global]]
        z_py.to_csv(analysis_output_path / 'z_pY.csv', index=False)
        z_pst.to_csv(analysis_output_path / 'z_pST.csv', index=False)
        z_global.to_csv(analysis_output_path / 'z_global.csv', index=False)
    else:
        z_py = pd.read_csv(analysis_output_path / 'z_pY.csv')
        z_pst = pd.read_csv(analysis_output_path / 'z_pST.csv')
        z_global = pd.read_csv(analysis_output_path / 'z_global.csv')

    return z_py, z_pst, z_global
