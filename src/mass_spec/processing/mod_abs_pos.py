def main(df, pep_data):
    pep_data = pep_data.drop_duplicates(subset=['Annotated Sequence'])

    df['Positions in Master Proteins'] = df['Sequence'].map(
        pep_data.set_index('Sequence')['Positions in Master Proteins']
    )

    print(pep_data['Positions in Master Proteins'])
    print(df['Positions in Master Proteins'])
    df['Modifications'] = df.apply(reindex_mods, axis=1)

    return df