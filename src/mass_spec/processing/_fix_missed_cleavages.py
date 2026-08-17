from mass_spec import settings


def main(df):
    samples = settings.SAMPLES
    to_drop = set()
    dropped = []
    unmatched = []
    for i in range(len(df)):
        if df.loc[i, 'Number of Missed Cleavages'] == 0:
            continue
        seq_i = df.loc[i, 'Annotated Sequence']
        if seq_i[0] in ('y', 'Y'):
            continue
        matched = False
        for j in range(len(df)):
            if i == j:
                continue
            seq_j = df.loc[j, 'Annotated Sequence']
            if seq_j[1:] in seq_i or seq_j[:-1] in seq_i:
                df.loc[j, samples] += df.loc[i, samples]
                to_drop.add(i)
                dropped.append(seq_i)
                matched = True
                break
        if not matched:
            unmatched.append(seq_i)

    df = df.drop(list(to_drop)).reset_index(drop=True)
    print(f"Dropped {len(to_drop)} missed-cleavage rows")
    print(dropped)
    if unmatched:
        print(f"{len(unmatched)} missed-cleavage rows had no match:")
        print(unmatched)
    return df
