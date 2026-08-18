import seaborn as sns
from mass_spec import settings
from mass_spec.analysis.z_score import main_zscore
import matplotlib.pyplot as plt


def cluster_map(analysis_output_path, plots_output_path, final_py, final_pst, final_global):
    z_py, z_pst, z_global = main_zscore(analysis_output_path, final_py, final_pst, final_global)
    z_py.attrs['run'] = 'pY'
    z_pst.attrs['run'] = 'pST'
    z_global.attrs['run'] = 'Global'

    [py_cluster_map, pst_cluster_map, global_cluster_map] = [calculate_cluster_map(data) for data
                                                             in [z_py, z_pst, z_global]]

    py_cluster_map.savefig((plots_output_path / 'pY_clustermap.png'), bbox_inches='tight', dpi=300)
    pst_cluster_map.savefig((plots_output_path / 'pY_clustermap.png'), bbox_inches='tight', dpi=300)
    global_cluster_map.savefig((plots_output_path / 'pY_clustermap.png'), bbox_inches='tight', dpi=300)

    plt.show()
    return


def calculate_cluster_map(data):
    samples = settings.SAMPLES

    g = sns.clustermap(
        data[samples],
        yticklabels=False,
        cmap='vlag',
        figsize=(8, 7),
        cbar_pos=(0.02, 0.85, 0.08, 0.12)
    )

    g.figure.suptitle(
        data.attrs['run'],
        fontsize=12,
        y=0.997
    )

    return g
