from mass_spec import settings
from mass_spec.analysis.log2FC import main_log2fc as log2fc
import numpy as np
import matplotlib.pyplot as plt


def main(analysis_output_path, plots_output_path, final_py, final_pst, final_global):
    log2fc_py, log2fc_pst, log2fc_global = log2fc(analysis_output_path, final_py, final_pst, final_global)
    log2fc_py.attrs['run'] = 'pY'
    log2fc_pst.attrs['run'] = 'pST'
    log2fc_global.attrs['run'] = 'Global'

    wf_py, wf_pst, wf_global = [calc_waterfall(data) for data in [log2fc_py, log2fc_pst, log2fc_global]]

    plt.show()

    return


def calc_waterfall(data):
    numer = settings.LOG2FC_PAIR[0]
    subset_labels = settings.SUBSET_LABELS
    run = data.attrs['run']

    target_indices = data.index[data['gene_name'].isin(subset_labels)].tolist()
    wanted_original_indices = target_indices

    # Sort data by EV abundance
    numer_sorted_data = data.sort_values(by=numer + '_mean')
    numer_sorted_data = numer_sorted_data.reset_index(drop=False)

    # x = sorted index
    # y = abundance
    x = np.array(numer_sorted_data.index.tolist())
    y = np.array(numer_sorted_data[numer + '_mean'].tolist())

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.scatter(
        x, y,
        s=1,
        color='tab:blue',
        alpha=0.5
    )
    target_points = []

    for sorted_y_idx, row in numer_sorted_data.iterrows():

        original_idx = row['index']

        if original_idx in wanted_original_indices:

            gene_name = row['gene_name']

            if run == 'pY' or run == 'pST':

                mods = str(row['Modifications']).split(';')
                mod_subset = []

                for mod in mods:
                    mod = mod.lstrip()

                    if mod and mod[0] in ['S', 'T', 'Y']:
                        mod_subset.append(
                            mod.split('(')[0]
                        )

                label_text = gene_name + '(' + ", ".join(mod_subset) + ')'

            else:
                label_text = gene_name

            target_points.append({
                'x': float(sorted_y_idx),
                'y': row[numer + '_mean'],
                'label': label_text
            })
    n_labels = len(target_points)

    x_min = min(x)
    x_max = max(x)
    x_range = x_max - x_min

    y_min = min(y)
    y_max = max(y)
    y_range = y_max - y_min

    # Put labels to the right of the data
    label_x = x_max + 0.11 * x_range

    # Evenly space labels starting from the top
    label_spacing = y_range * 0.06

    label_ys = (
            y_max * 0.95
            - label_spacing
            - np.arange(n_labels) * label_spacing
    )

    target_points = sorted(
        target_points,
        key=lambda p: p['y'],
        reverse=True
    )

    for point, label_y in zip(target_points, label_ys):
        if label_y - point['y'] > 5: label_y -= 5
        # Connecting line
        ax.plot(
            [point['x'], label_x],
            [point['y'], label_y],
            color='black',
            linewidth=0.5,
            alpha=0.5
        )

        # Label
        ax.text(
            label_x,
            label_y,
            point['label'],
            fontsize=9,
            ha='left',
            va='center'
        )
    # Give labels room on the right
    ax.set_xlim(
        x_min,
        x_max + x_range * 0.1
    )

    # Start at zero and go to maximum abundance
    ax.set_ylim(
        0,
        y_max * 1.05
    )

    ax.set_ylabel('Mean Log2 of EV Abundance')
    ax.set_title(run + ' Data Sorted')

    return plt
