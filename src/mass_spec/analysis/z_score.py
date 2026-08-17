from mass_spec import settings
from scipy.stats import zscore


def z_score(df):
    samples = settings.SAMPLES
    zscores = zscore(df[samples], axis=1, ddof=1)
    return zscores
