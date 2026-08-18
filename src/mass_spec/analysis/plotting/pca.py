import numpy as np
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pandas as pd
import matplotlib.pyplot as plt
from adjustText import adjust_text
from mass_spec import settings


def main(plots_output_path, data):
    gene_names = data['gene_name']
    run = data.attrs['run']

    pca, pca_plt = calc_pca(data, run)
    loadings_plt = calc_loadings(pca, gene_names, run)

    loadings_plt.savefig(plots_output_path / (run + '_pca_loadings.png'))
    pca_plt.savefig(plots_output_path / (run + '_pca.png'))

    plt.show()
    return


def calc_loadings(pca, gene_names, run):
    loadings = pca.components_.T * np.sqrt(pca.explained_variance_)

    loadings_df = pd.DataFrame(
        loadings,
        columns=['PC1', 'PC2'],
        index=gene_names
    ).reset_index(names='gene_name')

    loadings_df = loadings_df.reset_index(drop=True)

    loadings_top20 = loadings_df.sort_values(['PC1'], key=abs).tail(20)

    fig, ax = plt.subplots(figsize=(8, 6))

    ax.scatter(loadings_top20['PC1'], loadings_top20['PC2'])

    texts = []
    for idx, row in loadings_top20.iterrows():
        t = ax.text(
            row['PC1'],
            row['PC2'] - 0.0001,
            row['gene_name'],
            fontsize=7.5,
            fontweight=545,
            ha='right',
            va='center'
        )
        texts.append(t)
    adjust_text(
        texts,
        ax=ax,
        arrowprops=None
    )

    ax.set_xlabel('PC1 Loading')
    ax.set_ylabel('PC2 Loading')
    ax.set_title(run + ' PCA Loadings - Top 20 Genes')
    return fig


def calc_pca(data, run):
    samples = settings.SAMPLES
    data_t = data[samples].transpose()

    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data_t)

    pca = PCA(n_components=2)
    pca_features = pca.fit_transform(scaled_data)

    pca_df = pd.DataFrame(data=pca_features, columns=['PC1', 'PC2'])

    str_samples = [item.split(' ')[1] for item in samples]
    pca_df['target'] = str_samples
    pca_df['sample'] = samples

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(
        x='PC1', y='PC2', hue='target', palette='viridis',
        data=pca_df, s=70, ax=ax
    )

    info = pca.explained_variance_ratio_
    ax.set_xlabel(f'Principal Component 1 ({info[0] * 100:.1f}%)')
    ax.set_ylabel(f'Principal Component 2 ({info[1] * 100:.1f}%)')
    ax.set_title(run + ' PCA')
    ax.grid(True)

    return pca, fig
