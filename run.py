import os
import shutil
import glob
from plotCorMapAnalysis import plot_CorMapAnalysis
from plotDifferenceAnalysis import plot_DifferenceAnalysis

root = '/Users/lqhuang/Documents/CSRC/Data/SSRF-MagR-201703/Data'

depth = 2
depth_str = str(os.path.sep).join(['*' for i in range(depth)])
folders = glob.glob(os.path.join(root, depth_str))
# print('\n'.join(folders))

for exp_folder in folders:
    root_directory = exp_folder
    print('Calculating :', root_directory.split(os.path.sep)[-1], '\n')
    try:
        shutil.rmtree(os.path.join(root_directory, 'Figures'))
    except FileNotFoundError:
        print('Do not exist Figures')
    except NotADirectoryError:
        pass

    try:
        print('Try to calculating Difference Analysis')
        plot_DifferenceAnalysis(root_directory, display=False,
                                save_figures=True, fig_format='eps', figures_directory=None)
        print('Difference Analysis save successfully!')
    except Exception as error:
        print('Exception Information :', error.__doc__)
    print(' ')

    try:
        print('Try to calculating Correlation Heat Map')
        plot_CorMapAnalysis(root_directory, subtract=True, skip=0, display=False,
                            save_figures=True, fig_format='png', figures_directory=None)
        print('CorMap Analysis save successfully!')
    except Exception as error:
        print('Exception Information :', error.__doc__)
    print('---------------------------------------------------------------')
        