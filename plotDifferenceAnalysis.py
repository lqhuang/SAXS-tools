import os
import argparse
from saxsio import dat
from DifferenceAnalysis import DifferenceAnalysis
from matplotlib.pyplot import close

def plot_DifferenceAnalysis(root_directory, from_average=False,
                            save_figures=True, fig_format='png', legend_loc='left',
                            figures_directory=None, display=False,
                            smooth=False,
                            scale=False, scale_qmin=0.0, scale_qmax=-1.0,
                            crop=False, crop_qmin=0.0, crop_qmax=-1.0,
                            dash_line_index=(None,)):
    # read curves
    file_location = os.path.join(root_directory, 'Simple_Results')
    if from_average:
        scat_obj = DifferenceAnalysis.from_average_dats(os.path.join(file_location, '*'),
                                                        smooth=smooth,
                                                        scale=scale, ref_dat=None,
                                                        scale_qmin=scale_qmin, scale_qmax=scale_qmax,
                                                        crop=crop, crop_qmin=crop_qmin, crop_qmax=crop_qmax)
    else:
        scat_obj = DifferenceAnalysis.from_subtracted_dats(os.path.join(file_location, '*'),
                                                           smooth=smooth,
                                                           crop=crop, crop_qmin=crop_qmin, crop_qmax=crop_qmax)
    # save figures
    if not figures_directory:
        figures_directory = os.path.join(root_directory, 'Figures')
    EXP_prefix = os.path.basename(root_directory)
    kwargs = {'display': display, 'save': save_figures, 'directory': figures_directory,
              'legend_loc': legend_loc, 'dash_line_index': dash_line_index}
    scat_obj.plot_relative_diff(filename=EXP_prefix+'_relative_ratio.'+fig_format,
                                **kwargs)
    scat_obj.plot_profiles(log_intensity=True, filename=EXP_prefix+'_saxs_profiles.'+fig_format,
                           **kwargs)
    close('all')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--root_directory', help='Root directory for EXPERIMENTS data')

    parser.add_argument('-f', '--figures_directory',
                        help='Figures directory in root directory for Difference Analysis (default=Figures)',
                        default='Figures')
    parser.add_argument('--display', type=bool, default=False)

    parser.add_argument('--smooth', type=bool, default=True)

    parser.add_argument('--scale', type=bool, default=False)
    parser.add_argument('--scale_qmin', type=float, default=0.0)
    parser.add_argument('--scale_qmax', type=float, default=-1.0)
    
    parser.add_argument('--crop', type=bool, default=True)
    parser.add_argument('--crop_qmin', type=float, default=0.0)
    parser.add_argument('--crop_qmax', type=float, default=0.099)
    
    parser.add_argument('--dash_line_index', help='Index starts with 1',
                        type=str, default=None)

    args = parser.parse_args()
    print(args)
    root_directory = args.root_directory
    figures_directory = os.path.join(root_directory, args.figures_directory)
    display = args.display

    smooth = args.smooth

    crop = args.crop
    crop_qmin = args.crop_qmin
    crop_qmax = args.crop_qmax
    
    scale = args.scale
    scale_qmin = args.scale_qmin
    scale_qmax = args.scale_qmax

    try:
        dash_line_index = args.dash_line_index.split(',')
        dash_line_index = [int(idx) for idx in dash_line_index]
        print('dash line index:', dash_line_index)
    except AttributeError:
        dash_line_index = (None,)

    plot_DifferenceAnalysis(root_directory, 
                            save_figures=True, figures_directory=figures_directory, display=display,
                            smooth=smooth,
                            scale=scale, scale_qmin=scale_qmin, scale_qmax=scale_qmax,
                            crop=crop, crop_qmin=crop_qmin, crop_qmax=crop_qmax,
                            dash_line_index=dash_line_index)
