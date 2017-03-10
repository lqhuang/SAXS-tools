import os
import argparse


def plot_RelativeRatio(root_location, scale=True, subtract=False, save_figures=True, figures_directory=None):
    
    if not figures_directory:
        figures_directory = os.path.join(root_location, 'Figures')


if __name__ == '__main__':
    working_directory = r'E:\2017\201703\20170310'
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--root_directory', help='Root directory for EXPERIMENTS data',
                        default=os.path.join(working_directory, 'EXP13'))
    args = parser.parse_args()
    root_location = args.root_directory
    plot_RelativeRatio(root_location, scale=True, subtract=True, save_figures=True)