import seaborn as sns
import matplotlib.pyplot as plt
from mass_spec import settings


def cluster_map(plots_output_path, data_zscore):
    samples = settings.SAMPLES
    plt.close('all')

    g = sns.clustermap(
        data_zscore[samples],
        yticklabels=False,
        cmap='vlag',
        figsize=(8, 7),
        cbar_pos=(0.02, 0.85, 0.08, 0.12)
    )

    g.figure.suptitle(
        data_zscore.attrs['run'],
        fontsize=12,
        y=0.997
    )

    g.savefig(
        plots_output_path / (data_zscore.attrs['run'] + '_clustermap.png'),
        bbox_inches='tight'
    )

    plt.show()
    return
