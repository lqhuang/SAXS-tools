from __future__ import print_function, division

from RAW import SASM
from RAW.RAWWrapper import RAWSimulator

# FIXME: set RAW cfg path
cfg_path = ''
raw_simulator = RAWSimulator(cfg_path)

raw_simulator.set_raw_settings()
raw_simulator.set_raw_settings(
    GnomFilePath='',
    SubtractedFilePath='',
)
