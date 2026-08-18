import seaborn as sns
from mass_spec import settings
from mass_spec.analysis.z_score import z_score_main
import matplotlib.pyplot as plt


def cluster_map(analysis_output_path, plots_output_path, final_py, final_pst, final_global):
    z_py, z_pst, z_global = z_score_main(analysis_output_path, final_py, final_pst, final_global)
    z_py.attrs['run'] = 'pY'
    z_pst.attrs['run'] = 'pST'
    z_global.attrs['run'] = 'global'

    [py_cluster_map, pst_cluster_map, global_cluster_map] = [calculate_cluster_map(data) for data
                                                             in [z_py, z_pst, z_global]]

    py_cluster_map.savefig((plots_output_path / 'pY_clustermap.png'), bbox_inches='tight')
    pst_cluster_map.savefig((plots_output_path / 'pY_clustermap.png'), bbox_inches='tight')
    global_cluster_map.savefig((plots_output_path / 'pY_clustermap.png'), bbox_inches='tight')

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
