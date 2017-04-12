import os
import argparse
from saxsio import dat
from DifferenceAnalysis import DifferenceAnalysis
from matplotlib.pyplot import close

def plot_DifferenceAnalysis(root_directory, from_average=False,
                            smooth=False, crop=False, scale=False,
                            display=False,
                            dash_line_index=(None,),
                            save_figures=True, fig_format='png', legend_loc='left',
                            figures_directory=None):

    file_location = os.path.join(root_directory, 'Simple_Results')
    if from_average:
        scat_obj = DifferenceAnalysis.from_average_dats(os.path.join(file_location, '*'),
                                                        smooth=smooth, crop=crop, scale=scale,
                                                        ref_dat=None, qmin=0.13, qmax=0.18)
    else:
        scat_obj = DifferenceAnalysis.from_subtracted_dats(os.path.join(file_location, '*'),
                                                           smooth=smooth, crop=crop)

    if not figures_directory:
        figures_directory = os.path.join(root_directory, 'Figures')
    EXP_prefix = os.path.basename(root_directory)
    kwargs = {'dash_line_index':dash_line_index,
              'display':display, 'save':save_figures, 'directory':figures_directory}
    scat_obj.plot_relative_diff(filename=EXP_prefix+'_relative_ratio.'+fig_format, legend_loc=legend_loc,
                                **kwargs)
    scat_obj.plot_profiles(log_intensity=True, filename=EXP_prefix+'_saxs_profiles.'+fig_format, legend_loc=legend_loc,
                           **kwargs)
    close('all')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--root_directory', help='Root directory for EXPERIMENTS data')
    parser.add_argument('-f', '--figures_directory',
                        help='Figures directory in root directory for Difference Analysis (default=Figures)',
                        default='Figures')
    parser.add_argument('--display', type=bool)
    parser.add_argument('--dash_line_index', help='Index starts with 1', type=str, default=None)
    args = parser.parse_args()
    print(args)
    root_directory = args.root_directory
    figures_directory = os.path.join(root_directory, args.figures_directory)
    try:
        dash_line_index = args.dash_line_index.split(',')
        dash_line_index = [int(idx) for idx in dash_line_index]
        print('dash line index:', dash_line_index)
    except AttributeError:
        dash_line_index = (None,)
    display = args.display
    plot_DifferenceAnalysis(root_directory, dash_line_index=dash_line_index,
                            display=display,
                            save_figures=True,figures_directory=figures_directory)
