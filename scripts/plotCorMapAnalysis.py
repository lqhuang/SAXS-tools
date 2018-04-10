import os
import sys
import re
import glob
import argparse

from matplotlib.pyplot import close

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from CorMapAnalysis import ScatterAnalysis
from saxsio import dat
from utils import find_common_string_from_list, print_arguments, str2bool


def plot_CorMapAnalysis(root_directory,
                        skip=0,
                        buffer_dat=None,
                        scale=False,
                        ref_dat=None,
                        scale_qmin=0.0,
                        scale_qmax=-1.0,
                        crop=False,
                        crop_qmin=0.0,
                        crop_qmax=-1.0,
                        display=False,
                        save_figures=True,
                        fig_format='png',
                        figures_directory=None):
    # check Frames directory
    exists_frames_directory = os.path.exists(
        os.path.join(root_directory, 'Processed'))
    exists_valid_frames_directory = os.path.exists(
        os.path.join(root_directory, 'Averaged'))
    if exists_frames_directory:
        file_location = os.path.join(root_directory, 'Processed')
    elif not exists_frames_directory and exists_valid_frames_directory:
        file_location = os.path.join(root_directory, 'Averaged')
    else:
        raise ValueError('Do not exist frames directory')
    # glob files
    file_list = sorted(glob.glob(os.path.join(file_location, '*')))
    buffer_dat_list = list()
    data_dat_list = list()
    frame_num_list = list()
    for fname in file_list:
        if 'buffer' in fname.lower():
            buffer_dat_list.append(fname)
        else:
            data_dat_list.append(fname)
            frame_num = re.findall(r'\d+', fname)[-1]
            frame_num_list.append(float(frame_num))
    assert sorted(
        frame_num_list) == frame_num_list  # check sequence of frame_num
    # scale and subtract
    if not buffer_dat:
        if len(buffer_dat_list) < 1:
            raise NotImplementedError(
                'Do not exist buffer, please specify a buffer file')
        elif len(buffer_dat_list) == 1:
            buffer_dat = buffer_dat_list[0]
        else:
            pass
            # buffer_dat = dat.average_curves(buffer_dat_list, skip=skip)
    ref_dat = data_dat_list[0 + skip]
    data_dat_list = data_dat_list[0 + skip:]
    print(r'ref dat file: ', ref_dat.split(os.path.sep)[-1])
    print(r'buffer dat file:', buffer_dat.split(os.path.sep)[-1])
    subtract_directory = os.path.join(root_directory, 'Subtract')
    subtract_dat_list = dat.subtract_curves(
        data_dat_list,
        buffer_dat,
        subtract_directory,
        prefix='data',
        scale=scale,
        ref_dat=ref_dat,
        scale_qmin=scale_qmin,
        scale_qmax=scale_qmax,
        crop=crop,
        crop_qmin=crop_qmin,
        crop_qmax=crop_qmax)
    # plot CorMap
    subtract_dat_location = find_common_string_from_list(subtract_dat_list)
    scat_obj = ScatterAnalysis.from_1d_curves(subtract_dat_location + '*')
    if not figures_directory:
        figures_directory = os.path.join(root_directory, 'Figures')
    exp_prefix = os.path.basename(root_directory)
    scat_obj.plot_cormap(
        display=display,
        save=save_figures,
        filename=exp_prefix + '_cormap.' + fig_format,
        directory=figures_directory)
    scat_obj.plot_heatmap(
        display=display,
        save=save_figures,
        P_values=True,
        filename=exp_prefix + '_heatmap_P_values.' + fig_format,
        directory=figures_directory)
    scat_obj.plot_heatmap(
        display=display,
        save=save_figures,
        P_values=False,
        filename=exp_prefix + '_heatmap_C_values.' + fig_format,
        directory=figures_directory)

    close('all')


def main():
    # create an argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-r', '--root_directory', help='Root directory for EXPERIMENTS data')
    parser.add_argument(
        '-f',
        '--figures_directory',
        help=
        'Figures directory in root directory for CorMap Analysis (default=Figures)',
        type=str,
        default='Figures')
    parser.add_argument(
        '--skip',
        help='Frames need to be skipped (default=1)',
        type=int,
        default=0)
    parser.add_argument(
        '--crop',
        help='Whether to crop curves (default=False)',
        type=str2bool,
        default=False)
    parser.add_argument(
        '--crop_qmin', help='min q for cropping', type=float, default=0.0)
    parser.add_argument(
        '--crop_qmax', help='max q for cropping', type=float, default=-1.0)
    parser.add_argument(
        '--scale',
        help='Whether to scale curves (default=False)',
        type=str2bool,
        default=False)
    parser.add_argument(
        '--scale_qmin', help='min q for scaling', type=float, default=0.0)
    parser.add_argument(
        '--scale_qmax', help='max q for scaling', type=float, default=-1.0)

    # parse arguments
    args = parser.parse_args()
    print_arguments(args.__dict__)

    root_directory = os.path.realpath(args.root_directory)
    figures_directory = os.path.join(root_directory, args.figures_directory)
    skip = args.skip

    scale = args.scale
    scale_qmin = args.scale_qmin
    scale_qmax = args.scale_qmax

    crop = args.crop
    crop_qmin = args.crop_qmin
    crop_qmax = args.crop_qmax

    # run
    plot_CorMapAnalysis(
        root_directory,
        skip=skip,
        scale=scale,
        scale_qmin=scale_qmin,
        scale_qmax=scale_qmax,
        crop=crop,
        crop_qmin=crop_qmin,
        crop_qmax=crop_qmax,
        save_figures=True,
        figures_directory=figures_directory)


if __name__ == '__main__':
    main()
