import os
import argparse
from saxsio import dat
from DifferenceAnalysis import DifferenceAnalysis
from matplotlib.pyplot import close

def plot_DifferenceAnalysis(root_directory, display=False, dash_line_index=(None,),
                            save_figures=True, fig_format='png', figures_directory=None):

    file_location = os.path.join(root_directory, 'Simple_Results')
    scat_obj = DifferenceAnalysis.from_subtracted_dats(os.path.join(file_location, '*'))

    if not figures_directory:
        figures_directory = os.path.join(root_directory, 'Figures')
    EXP_prefix = os.path.basename(root_directory)
    scat_obj.plot_relative_diff(display=display, dash_line_index=dash_line_index,
                                save=save_figures, filename=EXP_prefix+'_relative_ratio.'+fig_format,
                                directory=figures_directory)
    scat_obj.plot_profiles(log_intensity=True, display=False, dash_line_index=dash_line_index,
                           save=save_figures, filename=EXP_prefix+'_saxs_profiles.'+fig_format,
                           directory=figures_directory)

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
