import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from adjustText import adjust_text
from mass_spec.analysis.log2FC import main_log2fc as log2fc


def main(analysis_output_path, plots_output_path, final_py, final_pst, final_global):
    log2fc_py, log2fc_pst, log2fc_global = log2fc(analysis_output_path, final_py, final_pst, final_global)
    log2fc_py.attrs['run'] = 'pY'
    log2fc_pst.attrs['run'] = 'pST'
    log2fc_global.attrs['run'] = 'global'

    global_data = log2fc_global[['gene_name', 'log2FC']].rename(columns={'log2FC': 'global_log2fc'})

    py_global_plot = plot_comp_log2fc(log2fc_py, global_data)
    pst_global_plot = plot_comp_log2fc(log2fc_pst, global_data)

    py_global_plot.savefig(plots_output_path / 'pY_global_comp.png')
    pst_global_plot.savefig(plots_output_path / 'pST_global_comp.png')

    plt.show()


def plot_comp_log2fc(p_data, global_data):
    data = pd.merge(global_data, p_data, on='gene_name', how='left').replace([np.inf, -np.inf], np.nan).dropna()

    # Process Data
    x_col = 'global_log2fc'
    y_col = 'log2FC'

    x = np.array(data[x_col].tolist())
    y = np.array(data[y_col].tolist())
    [m, b] = np.polyfit(x, y, 1)    # Find the trendline

    # Calculate the distance of each point from the trendline
    data['distance'] = np.abs(m * data[x_col] - data[y_col] + b) / np.sqrt(m**2 + 1)

    far_points = data.sort_values(by='distance').tail(30)

    # Generate Plot
    fig, ax = plt.subplots(figsize=(9, 5))

    ax.scatter(
        x, y,
        s=8,
        color='lightsteelblue'
    )
    ax.scatter(
        far_points[x_col], far_points[y_col],     # Highlight far points in a different color
        s=9,
        color='steelblue'
    )

    texts = []
    for idx, row in far_points.iterrows():
        mods = str(row['Modifications']).split(', ')
        mods_2 = []
        for mod in mods:
            if mod[0] in ['Y', 'S', 'T']:
                mods_2.append(mod)
        label_text = str(row['gene_name']).strip() + '(' + ", ".join(mods_2) + ')'

        # Create the text object on the plot axis
        t = ax.text(
            row[x_col],
            row[y_col],
            label_text,
            fontsize=7.5,
            fontweight=545,
            ha='right',
            va='center'
        )
        texts.append(t)
    # Prevent text from overlapping
    adjust_text(
        texts,
        target_x=far_points[x_col].values,
        target_y=far_points[y_col].values,

        x=far_points[x_col].values,
        y=far_points[y_col].values,

        only_move={
            'text': 'xy',
            'objects': 'xy',
            'points': 'y',
            'explode': 'y'
        },

        force_points=0.4,
        force_text=0.5,

        expand_points=(1.10, 1.10),
        expand_text=(1.20, 1.20),

        max_move=3,

        iter_lim=100,
        arrowprops=None
    )
    # Add arrows from text to points
    for t, (_, row) in zip(texts, far_points.iterrows()):
        px = row[x_col]
        py = row[y_col]

        tx, ty = t.get_position()

        ax.plot(
            [tx, px],
            [ty, py],
            color='gray',
            lw=0.75,
            alpha=0.75,
            zorder=1
        )

    ax.set_xlim(1.2 * min(x), 1.2 * max(x))
    ax.set_ylim(1.2 * min(y), 1.2 * max(y))

    plt.plot(x, m*x + b, color='red', linestyle='-', label='Trendline')     # Add trendline
    plt.xlabel('log2FC of EV/Cell in GLobal Data')
    plt.ylabel('log2FC of EV/Cell in ' + p_data.attrs['run'] + ' Data')

    return plt
