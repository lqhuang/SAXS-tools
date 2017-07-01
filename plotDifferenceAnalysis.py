import os.path
import argparse

from matplotlib import pyplot as plt

from DifferenceAnalysis import DifferenceAnalysis
from utils import print_arguments, str2bool


def plot_DifferenceAnalysis(root_directory, from_average=False, log_intensity=True,
                            save_figures=True, fig_format='png', legend_loc='left',
                            figures_directory=None, display=False,
                            baseline_index=1, smooth=False,
                            scale=False, scale_qmin=0.0, scale_qmax=-1.0,
                            crop=False, crop_qmin=0.0, crop_qmax=-1.0,
                            dash_line_index=(None,)):
    # read curves
    file_location = os.path.join(root_directory, 'Simple_Results')
    if from_average:
        seq_obj = DifferenceAnalysis.from_average_dats(
            os.path.join(file_location, 'A_*'), smooth=smooth,
            scale=scale, ref_dat=None, scale_qmin=scale_qmin, scale_qmax=scale_qmax)
    else:
        try:
            seq_obj = DifferenceAnalysis.from_subtracted_dats(os.path.join(file_location, 'S_*'),
                                                              smooth=smooth)
        except FileNotFoundError:
            print('Warning: Do not find subtracted curves, try to read data from average curves.')
            seq_obj = DifferenceAnalysis.from_average_dats(
                os.path.join(file_location, 'A_*'), smooth=smooth,
                scale=scale, ref_dat=None, scale_qmin=scale_qmin, scale_qmax=scale_qmax)

    kwargs = {'display': display, 'save': save_figures, 'directory': figures_directory,
              'legend_loc': legend_loc, 'dash_line_index': dash_line_index}

    # save figures
    if not figures_directory:
        figures_directory = os.path.join(root_directory, 'Figures')
    if not os.path.exists(figures_directory):
        os.makedirs(figures_directory)
    exp_prefix = os.path.basename(root_directory)

    # general
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(8, 5))
    seq_obj.plot_profiles(log_intensity=log_intensity, axes=axes[0, 0], **kwargs)
    seq_obj.plot_analysis('guinier', axes=axes[0, 1], **kwargs)
    seq_obj.plot_analysis('kratky', axes=axes[1, 0], **kwargs)
    seq_obj.plot_analysis('porod', axes=axes[1, 1], **kwargs)
    lgd = fig.legend(axes[0, 0].get_lines(), seq_obj.data_dict_label(),
                     loc='center left', bbox_to_anchor=(0.95, 0.5), frameon=False)
    # fig.subplots_adjust()
    fig.tight_layout()
    fig_path = os.path.join(figures_directory, exp_prefix+'_saxs_general_analysis.'+fig_format)
    try:
        fig.savefig(fig_path, dpi=seq_obj.DPI, bbox_extra_artists=(lgd,), bbox_inches='tight')
    except Exception as error:
        print('Exception Information:', error.__doc__)
    if display:
        plt.show()

    # difference
    # fig, axes = plt.subplots(nrows=2, ncols=1, sharex=True)
    # seq_obj.plot_difference('relative', axes=axes[0],
    #                         baseline_index=baseline_index, **kwargs)
    # seq_obj.plot_difference('absolute', axes=axes[1],
    #                         baseline_index=baseline_index, **kwargs)
    # axes[0].set_title(None)
    # axes[1].set_title([])
    # lgd = fig.legend(axes[0].get_lines(), seq_obj.data_dict_label(),
    #                  loc='center left', bbox_to_anchor=(0.95, 0.5), frameon=False)
    # fig_path = os.path.join(figures_directory, exp_prefix+'_saxs_difference_analysis.'+fig_format)
    # if display:
    #     plt.show()

    # single analysis
    seq_obj.plot_profiles(log_intensity=True,
                          crop=crop, crop_qmin=crop_qmin, crop_qmax=crop_qmax,
                          filename=exp_prefix+'_saxs_profiles_log_scale.'+fig_format,
                          **kwargs)
    seq_obj.plot_profiles(log_intensity=False,
                          crop=crop, crop_qmin=crop_qmin, crop_qmax=crop_qmax,
                          filename=exp_prefix+'_saxs_profiles.'+fig_format,
                          **kwargs)
    # seq_obj.plot_analysis('guinier',
    #                       filename=exp_prefix+'_saxs_guinier_analysis.'+fig_format,
    #                       **kwargs)
    seq_obj.plot_analysis('kratky',
                          filename=exp_prefix+'_saxs_kratky_analysis.'+fig_format,
                          **kwargs)
    # seq_obj.plot_analysis('porod',
    #                       filename=exp_prefix+'_saxs_porod_analysis.'+fig_format,
    #                       **kwargs)
    seq_obj.plot_difference('relative',
                            baseline_index=baseline_index,
                            crop=crop, crop_qmin=crop_qmin, crop_qmax=crop_qmax,
                            filename=exp_prefix+'_relative_ratio.'+fig_format,
                            **kwargs)
    seq_obj.plot_difference('absolute',
                            baseline_index=baseline_index,
                            crop=crop, crop_qmin=crop_qmin, crop_qmax=crop_qmax,
                            filename=exp_prefix+'_absolute_diff.'+fig_format,
                            **kwargs)
    plt.close('all')

    try:
        seq_obj.plot_pair_distribution(output_dir=os.path.join(root_directory, 'Gnom_output'),
                                       filename=exp_prefix+'_pair_distribution.'+fig_format,
                                       **kwargs)
    except AssertionError:
        print('Warning: couldn\'t find radius of gyration for some dat files')
    except Exception as error:
        print('Exception Information:', error.__doc__)
        raise(error)
    finally:
        plt.close('all')
    try:
        seq_obj.plot_guinier_fitting(display=display, save=True,
                                     directory=os.path.join(figures_directory, 'guinier_fitting'))
    except Exception as error:
        print('Exception Information:', error.__doc__)
        raise(error)
    finally:
        plt.close('all')


def main():
    # create an argument parser
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-r', '--root_directory', help='Root directory for EXPERIMENTS data')
    parser.add_argument('-a', '--from_average', help='Process curves from average dats',
                        type=str2bool, default=False)
    parser.add_argument('-f', '--figures_directory',
                        help='Figures directory in root directory for Difference Analysis (default=Figures)',
                        type=str, default='Figures')
    parser.add_argument('--display', help='Display figures or not. (default=False)',
                        type=str2bool, default=False)
    parser.add_argument('--log_intensity', help='Plot profiles with log intensity or not. (default=False)',
                        type=str2bool, default=True)
    parser.add_argument('--baseline_index', help='Index for baseline starts from 1 (default=1)',
                        type=int, default=1)
    parser.add_argument('--smooth', help='Smooth curves by savgol filter (default=True)', type=str2bool, default=False)
    parser.add_argument('--scale', help='Whether to scale curves (default=False)', type=str2bool, default=False)
    parser.add_argument('--scale_qmin', help='min q for scaling', type=float, default=0.0)
    parser.add_argument('--scale_qmax', help='max q for scaling', type=float, default=-1.0)
    parser.add_argument('--crop', help='Whether to crop curves (default=True)', type=str2bool, default=True)
    parser.add_argument('--crop_qmin', help='min q for cropping', type=float, default=0.0)
    parser.add_argument('--crop_qmax', help='max q for cropping', type=float, default=-1.0)
    parser.add_argument('--dash_line_index', help='Index for dash line starts from 1, eg: 1,2,3. (default=None)',
                        type=str, default=None)

    # parse arguments
    args = parser.parse_args()
    args_dict = args.__dict__
    print_arguments(args_dict)

    root_directory = os.path.realpath(args.root_directory)
    figures_directory = os.path.join(root_directory, args.figures_directory)
    display = args.display

    from_average = args.from_average
    log_intensity = args.log_intensity
    smooth = args.smooth
    baseline_index = args.baseline_index

    crop = args.crop
    crop_qmin = args.crop_qmin
    crop_qmax = args.crop_qmax

    scale = args.scale
    scale_qmin = args.scale_qmin
    scale_qmax = args.scale_qmax

    try:
        dash_line_index = args.dash_line_index.split(',')
        dash_line_index = [int(idx) for idx in dash_line_index]
    except AttributeError:
        dash_line_index = (None,)

    # run
    plot_DifferenceAnalysis(root_directory, from_average=from_average,
                            log_intensity=log_intensity,
                            save_figures=True, figures_directory=figures_directory, display=display,
                            baseline_index=baseline_index, smooth=smooth,
                            scale=scale, scale_qmin=scale_qmin, scale_qmax=scale_qmax,
                            crop=crop, crop_qmin=crop_qmin, crop_qmax=crop_qmax,
                            dash_line_index=dash_line_index)


if __name__ == '__main__':
    main()
