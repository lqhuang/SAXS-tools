#!/usr/bin/env python3
"""
Usage:
    RAW_dat_parser.py <dat_files>... --ref=<ref_dat> [options]

Options:
    -h --help                  Show this screen.
    --ref=<ref_dat>            Reference RAW dat file.
    --smooth=<smooth>          Whether to smooth curves by savgol filter [default: False].
    --log_I=<log_I>            plot figures in log intensity or not [default: True].
    --qmin=<qmin>              qmin to calculate scaling ratio [default: 0].
    --qmax=<qmax>              qmax to calculate scaling ratio [default: 1E10].
    --crop_qmin=<crop_qmin>    qmin to crop 1d curve [default: 0].
    --crop_qmax=<crop_qmax>    qmax to crop 1d curve [default: 1E10].
    --display=<display>        Display figures of results [default: True].
    --save=<save>              Save figures to files [default: False].
    --path=<path>              File path for saving figures [default: './'].
"""
import os
import numpy as np 
from docopt import docopt
import matplotlib.pyplot as plt
from saxsio import dat
from DifferenceAnalysis import get_data_dict


SIZE = 16
plt.rc('font', size=SIZE)  # controls default text sizes
plt.rc('text', **{'latex.unicode' : True})
# plt.style.use('classic')


def analysis_dat():
    ### parse arguments
    argv = docopt(__doc__)
    raw_dats = argv['<dat_files>']
    ref_dat = argv['--ref']
    log_I = bool(argv['--log_I'])
    smooth = bool(argv['--smooth'])
    scale_qmin = float(argv['--qmin'])
    scale_qmax = float(argv['--qmax'])
    crop_qmin = float(argv['--crop_qmin'])
    crop_qmax = float(argv['--crop_qmax'])
    display = bool(argv['--display'])
    save = bool(argv['--save'])
    path = str(argv['--path'])

    ### load data dict
    ref_data_dict = get_data_dict(ref_dat, smooth=smooth, crop=False)
    data_list = list()
    for raw_dat in raw_dats:
        data_dict = get_data_dict(raw_dat, smooth=smooth, crop=False)
        # scale intensity
        data_dict['scaling_I'], data_dict['scaling_factor'] \
            = dat.scale_curve((data_dict['q'], data_dict['I']), (ref_data_dict['q'], ref_data_dict['I']),
                              qmin=scale_qmin, qmax=scale_qmax,
                              inc_factor=True)
        # calculate relative difference
        data_dict['relative_diff'] = (data_dict['scaling_I'] - ref_data_dict['I']) / ref_data_dict['I']
        data_dict['relative_diff'] *= 100
        data_list.append(data_dict)

    # crop
    for data_dict in data_list:
        crop_idx = np.logical_and(data_dict['q'] >= crop_qmin, data_dict['q'] < crop_qmax)
        data_dict['q'] = data_dict['q'][crop_idx]
        data_dict['I'] = data_dict['I'][crop_idx]
        data_dict['scaling_I'] = data_dict['scaling_I'][crop_idx]
        data_dict['relative_diff'] = data_dict['relative_diff'][crop_idx]

    ### making plots
    fig, ax = plt.subplots(ncols=2, figsize=(16, 6))
    ax0, ax1 = ax[0], ax[1]

    # subtracted profiles
    if log_I:
        for data in data_list:
            data['scaling_I'] = np.log(data['scaling_I'])
        for data in data_list:
            ax0.plot(data['q'], data['scaling_I'], label=data['filename'].replace('_', ' '), linewidth=1.5, linestyle='-')
    lgd = ax0.legend(loc=0, frameon=False, prop={'size':14})
    ax0.set_xlabel(r'Scattering Vector, q ($\AA^{-1}$)')
    if log_I:
        ax0.set_ylabel('Intensity (arb. unit in log scale)')
    else:
        ax0.set_ylabel('Intensity (arb. unit)')
    ax0.set_title('SAXS Profiles')

    for data in data_list:
        ax1.plot(data['q'], data['relative_diff'], label=data['filename'].replace('_', ' '), linewidth=1.5, linestyle='-')
    ax1.set_xlabel(r'Scattering Vector, q ($\AA^{-1}$)')
    ax1.set_ylabel('Relative Difference Ratio (%)')
    ymin, ymax = ax1.get_ylim()
    if ymax < 10.0:
        ax1.set_ylim([ymin, 10])
    ymin, ymax = ax1.get_ylim()
    if ymin > -5.0:
        ax1.set_ylim([-5.0, ymax])
    ax1.set_title('Relative Difference Analysis')

    # plt.savefig(os.path.join(save_prefix, fig_prefix+'_relative_difference_ratio.png'), dpi=600)
    if display:
        fig.tight_layout()
        plt.show()

if __name__ == '__main__':
    analysis_dat()
