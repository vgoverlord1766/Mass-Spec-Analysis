CHANNELS = None
SAMPLES = None
METADATA_COLS = None


def init(config):
    global CHANNELS, SAMPLES, METADATA_COLS
    CHANNELS = config["channels"]
    SAMPLES = config["samples"]
    METADATA_COLS = config["metadata_cols"]
