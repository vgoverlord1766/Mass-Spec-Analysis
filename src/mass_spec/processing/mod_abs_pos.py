def reindex_mods(row):
    modifications = row['Modifications'].split(';')
    print(row['Positions in Master Proteins'])
    global_pos = row['Positions in Master Proteins'].split('[')[1].split('-')[0]
    new_mods = []
    for mod in modifications:
        if 'TMT' in mod:
            continue
        adjusted_mod_ind = int(mod.lstrip().split('(')[0][1:]) + int(global_pos) - 1
        new_mod = mod.lstrip().split('(')[0][0] + str(adjusted_mod_ind)
        new_mods.append(new_mod)
    new_mods_list = ", ".join(new_mods)
    return new_mods_list


def main(df, pep_data):
    pep_data = pep_data.drop_duplicates(subset=['Annotated Sequence'])

    df['Positions in Master Proteins'] = df['Sequence'].map(
        pep_data.set_index('Sequence')['Positions in Master Proteins']
    )

    print(pep_data['Positions in Master Proteins'])
    print(df['Positions in Master Proteins'])
    df['Modifications'] = df.apply(reindex_mods, axis=1)

    return df
