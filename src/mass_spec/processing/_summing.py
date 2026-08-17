from mass_spec import settings


def global_summing(df):
    samples = settings.SAMPLES
    channels = settings.CHANNELS
    metadata_cols = settings.METADATA_COLS

    all_abundance_cols = df.filter(like='Abundance').columns.tolist()   # Remove any unwanted channels
    not_channels = [col for col in all_abundance_cols if col not in channels]
    df = df.drop(columns=not_channels)

    df.rename(columns=dict(zip(channels, samples)), inplace=True)   # Rename channels with sample names

    df['Annotated Sequence'] = df['Annotated Sequence'].str.replace('m', 'M')
    df['Annotated Sequence'] = df['Annotated Sequence'].str.split('.').str[1]
    gene_names = df['Master Protein Descriptions'].str.extract(r'GN=(\S+)', expand=False)
    df['gene_name'] = gene_names

    unique_df = (
        df[['gene_name'] + metadata_cols]
        .drop_duplicates(subset='gene_name')
    )
    summed_df = df.groupby('gene_name', as_index=False)[samples].sum()
    summed_df.to_csv("asldkjfhasd.csv")
    final_df = unique_df.merge(summed_df, on='gene_name')

    return final_df


def summing(df):
    samples = settings.SAMPLES
    channels = settings.CHANNELS
    metadata_cols = settings.METADATA_COLS

    print("Asdfalsdkjfhsalkfdjh")
    all_abundance_cols = df.filter(like='Abundance').columns.tolist()  # Remove any unwanted channels
    not_channels = [col for col in all_abundance_cols if col not in channels]
    df = df.drop(columns=not_channels)

    df.rename(columns=dict(zip(channels, samples)), inplace=True)  # Rename channels with sample names
    df['Annotated Sequence'] = df['Annotated Sequence'].str.replace('m', 'M')
    df['Annotated Sequence'] = df['Annotated Sequence'].str.split('.').str[1]

    unique_df = df[metadata_cols].drop_duplicates(subset=['Annotated Sequence'])   # Get with all unique sequences
    summed_df = df.groupby('Annotated Sequence')[samples].sum().reset_index()  # Sum identical sequences

    final_df = unique_df.merge(summed_df, on='Annotated Sequence')
    gene_names = final_df['Master Protein Descriptions'].str.extract(r'GN=(\S+)', expand=False)
    final_df['gene_name'] = gene_names

    return final_df
