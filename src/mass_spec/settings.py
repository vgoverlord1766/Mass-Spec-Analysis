CHANNELS = None
SAMPLES = None
METADATA_COLS = None
LOG2FC_PAIR = None
VOLCANO_LABELS = None


def init(config):
    global CHANNELS, SAMPLES, METADATA_COLS, LOG2FC_PAIR, VOLCANO_LABELS
    CHANNELS = config["channels"]
    SAMPLES = config["samples"]
    METADATA_COLS = config["metadata_cols"]
    LOG2FC_PAIR = config["log2fc_pair"]
    VOLCANO_LABELS = config["volcano_labels"]

