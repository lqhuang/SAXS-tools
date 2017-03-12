import os
import argparse
from saxsio import dat
from DifferenceAnalysis import DifferenceAnalysis
from matplotlib.pyplot import close

def plot_DifferenceAnalysis(root_directory, save_figures=False, figures_directory=None):

    file_location = os.path.join(root_directory, 'Simple_Results')
    scat_obj = DifferenceAnalysis.from_subtracted_dats(os.path.join(file_location, '*'))

    if not figures_directory:
        figures_directory = os.path.join(root_directory, 'Figures')
    EXP_prefix = os.path.basename(root_directory)
    scat_obj.plot_relative_diff(display=False,
                                save=save_figures, filename=EXP_prefix+'_relative_ratio.png',
                                directory=figures_directory)
    scat_obj.plot_profiles(log_intensity=True, display=False,
                           save=save_figures, filename=EXP_prefix+'_saxs_profiles.png',
                           directory=figures_directory)

    close('all')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--root_directory', help='Root directory for EXPERIMENTS data')
    parser.add_argument('-f', '--figures_directory',
                        help='Figures directory in root directory for Difference Analysis (default=Figures)',
                        default='Figures')
    args = parser.parse_args()
    root_directory = args.root_directory
    figures_directory = os.path.join(root_directory, args.figures_directory)
    plot_DifferenceAnalysis(root_directory, save_figures=True, figures_directory=figures_directory)