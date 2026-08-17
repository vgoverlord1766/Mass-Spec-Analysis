from pathlib import Path
from mass_spec.io.config import load_config


def main(data, run):
    if run == 'global':
        data = data[(data["Ions Score"] > 20) & (data["Search Engine Rank"] == 1)].copy()
    if run == 'pY':
        data = data[(data["Ions Score"] > 20) &
                (data["Search Engine Rank"] == 1) &
                (data["Modifications"].str.contains(r'Y\d+\(Phospho\)', regex=True, na=False))
                ].copy()
    if run == 'pST':
        data = data[(data["Ions Score"] > 20) &
                (data["Search Engine Rank"] == 1) &
                (data["Modifications"].str.contains('Phospho'))
                ].copy()
    if run == 'corr':
        df = df[(df["Ions Score"] > 20) &
                (df["Search Engine Rank"] == 1)
                ].copy()
        df = df.dropna(subset=channels)

    data = data.dropna(subset=channels, how='all')  # Remove any rows with all empty channels
    for channel in channels:     # Fill any empty channels with 0
        data[channel] = data[channel].fillna(0)
    return data