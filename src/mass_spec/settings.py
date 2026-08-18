CHANNELS = None
SAMPLES = None
METADATA_COLS = None
LOG2FC_PAIR = None
SUBSET_LABELS = None
SUBSET_LABEL = None
VOLCANO_SHOW_SUBSET = None
COMP_LOG2FC_SHOW_SUBSET = None


def init(config):
    global CHANNELS, SAMPLES, METADATA_COLS, LOG2FC_PAIR, SUBSET_LABELS, SUBSET_LABEL, VOLCANO_SHOW_SUBSET, \
           COMP_LOG2FC_SHOW_SUBSET

    CHANNELS = config['channels']
    SAMPLES = config['samples']
    METADATA_COLS = config['metadata_cols']
    LOG2FC_PAIR = config['log2fc_pair']
    SUBSET_LABELS = config['subset_labels']
    SUBSET_LABEL = config['subset_label']
    COMP_LOG2FC_SHOW_SUBSET = config['comp_log2fc_show_subset']
    VOLCANO_SHOW_SUBSET = config['volcano_show_subset']
