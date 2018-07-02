#!/usr/bin/env python3
"""
Usage:
    RAW_dat_parser.py <dat_files>... [options]

Options:
    -h --help                  Show this screen.
    --ref=<ref_dat>            Reference RAW dat file [default: None]. Default to use the first dat file.
    --smooth=<smooth>          Whether to smooth curves by savgol filter [default: False].
    --log_I=<log_I>            plot figures in log intensity or not [default: True].
    --qmin=<qmin>              qmin to calculate scaling ratio [default: 0].
    --qmax=<qmax>              qmax to calculate scaling ratio [default: 1E10].
    --crop_qmin=<crop_qmin>    qmin to crop 1d curve [default: 0].
    --crop_qmax=<crop_qmax>    qmax to crop 1d curve [default: 1E10].
    --display=<display>        Display figures of results [default: True].
    --save=<save>              Save figures to files [default: False].
    --path=<path>              File path for saving figures [default: ./].
    --dash_line_index=<idx>    plot specific line under dash style (seperate with comma) [default: None].
"""
import os
from docopt import docopt
import matplotlib.pyplot as plt
from DifferenceAnalysis import DifferenceAnalysis
from utils import str2bool


def analysis_dat():
    ### parse arguments
    argv = docopt(__doc__)
    raw_dats = argv['<dat_files>']
    ref_dat = argv['--ref']
    log_intensity = str2bool(argv['--log_I'])
    smooth = str2bool(argv['--smooth'])
    scale_qmin = float(argv['--qmin'])
    scale_qmax = float(argv['--qmax'])
    crop_qmin = float(argv['--crop_qmin'])
    crop_qmax = float(argv['--crop_qmax'])
    display = str2bool(argv['--display'])
    save = str2bool(argv['--save'])
    path = os.path.realpath(argv['--path'])
    if argv['--dash_line_index'] != 'None':
        try:
            dash_line_index = argv['--dash_line_index'].split(',')
            dash_line_index = [int(idx) for idx in dash_line_index]
        except AttributeError:
            dash_line_index = (None, )
    else:
        dash_line_index = (None, )

    if ref_dat == 'None':
        ref_dat = None

    ### load data dict
    seq_obj = DifferenceAnalysis.from_dats_list(
        raw_dats,
        smooth=smooth,
        scale=True,
        ref_dat=ref_dat,
        scale_qmin=scale_qmin,
        scale_qmax=scale_qmax,
    )

    ### make plots
    plot_args = dict(
        crop=True,
        crop_qmin=crop_qmin,
        crop_qmax=crop_qmax,
        dash_line_index=dash_line_index,
    )
    fig, ax = plt.subplots(ncols=2, figsize=(16, 6))
    # subtracted profiles
    seq_obj.plot_profiles(log_intensity=log_intensity, axes=ax[0], **plot_args)
    ax[0].legend(loc=0, frameon=False, prop={'size': seq_obj.LEGEND_SIZE})
    # relative difference
    seq_obj.plot_difference(
        'relative', baseline_dat=ref_dat, axes=ax[1], **plot_args)
    fig.tight_layout()

    if save:
        plt.savefig(os.path.join(path, 'figure.png'), dpi=seq_obj.DPI)
    if display:
        plt.show()


if __name__ == '__main__':
    analysis_dat()
