from mass_spec import settings


def main(df):
    samples = settings.SAMPLES
    row_means = df[samples].mean(axis=1, numeric_only=True)
    df_row_div = df[samples].div(row_means, axis=0)
    col_means = df_row_div.mean(axis=0, numeric_only=True)

    return col_means
