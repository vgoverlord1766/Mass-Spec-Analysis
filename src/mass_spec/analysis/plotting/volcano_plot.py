from mass_spec.analysis.log2FC import main_log2fc as log2fc
from mass_spec import settings
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from adjustText import adjust_text


def main(analysis_output_path, plots_output_path, final_py, final_pst, final_global):
    pair = settings.LOG2FC_PAIR

    log2fc_py, log2fc_pst, log2fc_global = log2fc(analysis_output_path, final_py, final_pst, final_global)
    log2fc_py.attrs['run'] = 'pY'
    log2fc_pst.attrs['run'] = 'pST'
    log2fc_global.attrs['run'] = 'Global'

    data_info = subset_data([log2fc_py, log2fc_pst, log2fc_global], pair)
    py_plot, pst_plot, global_plot = [volcano_plot(data, data_info, data.attrs['run'], pair) for data in
                                      [log2fc_py, log2fc_pst, log2fc_global]]

    py_plot.savefig(plots_output_path / 'pY_volcano_plot.png', dpi=500, bbox_inches='tight')
    pst_plot.savefig(plots_output_path / 'pST_volcano_plot.png', dpi=500, bbox_inches='tight')
    global_plot.savefig(plots_output_path / 'global_volcano_plot.png', dpi=500, bbox_inches='tight')

    plt.show()
    return


def volcano_plot(data, data_info, run, pair):
    subset_labels = settings.SUBSET_LABELS
    subset_label = settings.SUBSET_LABEL
    volcano_show_subset = settings.VOLCANO_SHOW_SUBSET

    fc_thresh = 1.0
    p_thresh = 0.05

    [top_fc_ind, top_numer_ind] = data_info[run]
    [numer, denom] = pair

    # Create the volcano plot
    plt.figure(figsize=(7, 4))

    sns.scatterplot(
        data=data,
        x='log2FC',
        y='-log10_p',
        alpha=0.7,
        edgecolor=None,
        color='lightsteelblue',
        s=20
    )
    if not volcano_show_subset:
        target_indices = list(set(top_fc_ind.append(top_numer_ind)))
        sns.scatterplot(
            data=data.loc[top_fc_ind],
            x='log2FC',
            y='-log10_p',
            color='steelblue',
            edgecolor=None,
            s=25,
            label='Top 20 log2FC'
        )
        sns.scatterplot(
            data=data.loc[top_numer_ind],
            x='log2FC',
            y='-log10_p',
            color='sandybrown',
            edgecolor=None,
            s=25,
            label='Top 20 ' + numer + ' abundance'
        )
    else:
        target_indices = data.index[data['gene_name'].isin(subset_labels)].tolist()
        sns.scatterplot(
            data=data.loc[target_indices],
            x='log2FC',
            y='-log10_p',
            color='sandybrown',
            edgecolor=None,
            s=25,
            label=subset_label
        )

    ax = plt.gca()
    ax.set_xlim(right=12)

    subset_df = data.loc[target_indices].copy()
    subset_df = subset_df.dropna(subset=['gene_name', 'log2FC', '-log10_p'])
    texts = []
    for idx, row in subset_df.iterrows():
        gene_name = str(row['gene_name']).strip()
        if run == 'pY' or run == 'pST':
            mods = str(row['Modifications']).split(';')
            mod_subset = []
            for mod in mods:
                mod = mod.lstrip()
                if mod[0] == 'S' or mod[0] == 'T' or mod[0] == 'Y':
                    mod_subset.append(mod.lstrip().split('(')[0])

            label_text = gene_name + '(' + ", ".join(mod_subset) + ')'
        else:
            label_text = gene_name

        # Create the text object on the plot axis
        if volcano_show_subset:
            text_size = 8
        else:
            text_size = 6

        t = ax.text(
            row['log2FC'],
            row['-log10_p'],
            label_text,
            fontsize=text_size,
            weight='semibold'
        )
        texts.append(t)

    # Prevent overlapping labels
    adjust_text(
        texts,
        x=subset_df['log2FC'].values,
        y=subset_df['-log10_p'].values,
        arrowprops=dict(arrowstyle="-", color='gray', lw=0.5, alpha=0.6),
        only_move={'points': 'y', 'text': 'xy'},
        force_points=0.2,
        force_text=0.3,
        expand_points=(1.02, 1.02),
        expand_text=(1.03, 1.07)
    )

    # Add threshold lines
    plt.axvline(x=fc_thresh, color='gray', linestyle='--', linewidth=0.8)
    plt.axvline(x=-fc_thresh, color='gray', linestyle='--', linewidth=0.8)
    plt.axhline(y=-np.log10(p_thresh), color='gray', linestyle='--', linewidth=0.8)

    # Add labels
    plt.title(run + ' ' + numer + "/" + denom, fontsize=12, weight='bold')
    plt.xlabel('Log2 Fold Change', fontsize=10)
    plt.ylabel('-Log10 (p-value)', fontsize=10)
    ax.legend(loc='lower right')
    plt.tight_layout()

    return plt


def subset_data(datasets, pair):
    data_info = {}
    for data in datasets:
        run_name = data.attrs['run']
        [numer, denom] = pair
        sig_data = data[data['p_value'] < 0.05]
        sig_data_numer_higher = sig_data[sig_data['log2FC'] > 1]
        sig_data_denom_higher = sig_data[sig_data['log2FC'] < 1]

        top_fc = data.nlargest(40, 'log2FC')
        top_numer = data.nlargest(20, numer + '_mean')

        top_fc_ind = top_fc.index
        top_numer_ind = top_numer.index

        print(run_name + ':')
        print("Top 20 log2fc:")
        print(top_fc['gene_name'].tolist())
        print("Top 20 " + numer + " significantly higher than " + denom + ":")
        print(top_numer['gene_name'].tolist())

        data_info[run_name] = [top_fc_ind, top_numer_ind]

    return data_info
