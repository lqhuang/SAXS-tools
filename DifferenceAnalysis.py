import os
import glob
import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl
from saxsio import dat


def get_data_dict(dat_file):
    data_dict = dict()
    filename = dat_file.split(os.path.sep)[-1]
    data_dict['filename'] = filename
    data_dict['label'] = filename.replace('.dat', '').replace('_', '')
    q, intensity, error = dat.load_RAW_dat(dat_filef)
    data_dict['q'] = q
    data_dict['I'] = intensity
    data_dict['E'] = error
    data_dict['linestyle'] = '-'
    return data_dict

class DifferenceAnalysis(object):

    # ----------------------------------------------------------------------- #
    #                         CLASS VARIABLES                                 #
    # ----------------------------------------------------------------------- #
    mpl.rc('font', family='serif', weight='normal', size=12)
    PLOT_LABEL = {'family': 'serif',
                  'weight': 'normal',
                  'size': 16}
    LABEL_SIZE = 14
    plt.rc('font', PLOT_LABEL)

    PLOT_NUM = 0

    # ----------------------------------------------------------------------- #
    #                         CONSTRUCTOR METHOD                              #
    # ----------------------------------------------------------------------- #
    def __init__(self, data_dict_list):
        self.num_curves = len(data_dict_list)
        self.data_dict_list = data_dict_list
        self.keys = data_dict_list[0].keys()

    # ----------------------------------------------------------------------- #
    #                          CLASS METHODS                                  #
    # ----------------------------------------------------------------------- #
    @classmethod
    def from_1d_curves(self, root_directory, buffer_dat, subtract=False,
                       scale=False, ref_dat=None, scale_qmin=None, scale_qmax=None,
                       baseline_dat=None, crop=False):
        # glob files
        file_location = os.path.join(root_directory, 'Simple_Results')
        file_list = glob.glob(file_location)
        # read data
        buffer_dat_list = list()
        average_dat_list = list()
        subtracted_dat_list = list()
        for fname in file_list:
            if 'buffer' in fname.lower():
                buffer_dat_list.append(fname)
            elif fname.lower().startswith('a'):
                average_dat_list.append(fname)
            elif fname.lower().startswith('s'):
                subtracted_dat_list.append(fname)
        # scale and subtract
        buffer = dict()
        if buffer_dat:
            buffer['q'], buffer['I'], buffer['E'] = dat.load_RAW_dat(buffer_dat)
        else:
            if len(buffer_dat_list) < 1:
                raise ValueError('Do not exist buffer, please specify a buffer file')
            elif len(buffer_dat_list) == 1:
                buffer['q'], buffer['I'], buffer['E'] = dat.load_RAW_dat(buffer_dat_list[0])
            else:
                pass
                # buffer_dat = dat.average_curves(buffer_dat_list, skip=skip)

        if subtract:
            pass
        else:
            if baseline_dat:
                baseline_dict = get_data_dict(baseline_dat)
            else:
                baseline_dict = get_data_dict(subtracted_dat_list[0])

        cls = None
        return cls

    @classmethod
    def from_subtracted_dats(self, subtracted_dat_location):
        # glob files
        file_list = glob.glob(subtracted_dat_location)
        # read data
        subtracted_dat_list = [fname for fname in file_list \
                               if fname.lower().startswith('s')]
        data_dict_list = [get_data_dict(dat_file) for dat_file in subtracted_dat_list]

        cls = DifferenceAnalysis(data_dict_list)
        return cls

    # ----------------------------------------------------------------------- #
    #                         INSTANCE METHODS                                #
    # ----------------------------------------------------------------------- #
    def calc_log_intensity(self):
        for data_dict in self.data_dict_list:
            data_dict['log_I'] = np.log(data_dict['I'])
        self.keys = self.data_dict_list[0].keys()

    def calc_relative_diff(self, baseline_dat=None, crop=False):
        if not baseline_dat:
            baseline_dict = self.data_dict_list[0]
        else:
            baseline_dict = get_data_dict(baseline_dat)
        for data_dict in self.data_dict_list:
            data_dict['relative_diff'] = (data_dict['I'] - baseline_dict['I']) / baseline_dict['I']
        self.keys = self.data_dict_list[0].keys()

    def calc_absolute_diff(self, baseline_dat=None, crop=False):
        if not baseline_dat:
            baseline_dict = self.data_dict_list[0]
        else:
            baseline_dict = get_data_dict(baseline_dat)
        for data_dict in self.data_dict_list:
            data_dict['absolute_diff'] = (data_dict['I'] - baseline_dict['I']) / baseline_dict['I']
        self.keys = self.data_dict_list[0].keys()

    # ----------------------- PLOT ------------------------#
    def plot_profiles(self, log_intensity=True,
                      display=True, save=False, filename=None, directory=None):
        ###########   SAXS Profiles  ####################
        self.PLOT_NUM += 1

        # ++++++++++++++++++++++++++++++ PLOT +++++++++++++++++++++++++++ #
        fig = plt.figure(self.PLOT_NUM)
        intensity_key = 'I'
        if log_intensity:
            if 'log_I' not in self.keys():
                self.calc_log_intensity()
            intensity_key = 'log_I'
        for data_dict in self.data_dict_list:
            plt.plot(data_dict['q'], data_dict[intensity_key],
                     label=data_dict['label'],
                     linestyle=data_dict['linestyle'], linewidth=1.5)
        plt.legend(loc='upper right', frameon=False, prop={'size':self.LABEL_SIZE})
        plt.xlabel(r'Scattering Vector, q ($nm^{-1}$)')
        if log_intensity:
            plt.ylabel('log(I) (arb. units.)', fontdict=self.PLOT_LABEL)
        else:
            plt.ylabel('Intensity (arb. units.)', fontdict=self.PLOT_LABEL)
        plt.title('SAXS Subtracted Profiles')
        # plt.tight_layout()

        # +++++++++++++++++++++ SAVE AND/OR DISPLAY +++++++++++++++++++++ #
        if filename:
            pass
        else:
            filename = 'saxs_profiles.png'
        if save:
            if directory:
                if not os.path.exists(directory):
                    os.mkdir(directory)
                fig_path = os.path.join(directory, filename)
            else:
                fig_path = filename
            plt.savefig(fig_path, dpi=600)
        if display:
            plt.show()

    def plot_relative_diff(self, baseline_dat=None,
                           display=True, save=False, filename=None, directory=None):
        ###########   Relative Ratio  ####################
        self.PLOT_NUM += 1

        # ++++++++++++ CALCULATE RELATIVE DIFFERENCE RATIO ++++++++++++++ #
        if baseline_dat:
            baseline_dict = get_data_dict(baseline_dat)
        else:
            baseline_dict = self.data_dict_list[0]
            self.calc_relative_diff(self, baseline_dict)

        # ++++++++++++++++++++++++++++++ PLOT +++++++++++++++++++++++++++ #
        plt.figure(self.PLOT_NUM)
        for data_dict in self.data_dict_list:
            plt.plot(data_dict['q'], data_dict['relative_diff'],
                     label=data_dict['filename'],
                     linestyle=data_dict['linestyle'], linewidth=1.5)
        plt.xlabel(r'Scattering Vector, q ($nm^{-1}$)', fontdict=self.PLOT_LABEL)
        plt.ylabel('Relative Ratio', fontdict=self.PLOT_LABEL)
        plt.legend(loc='upper right', frameon=False, prop={'size':self.LABEL_SIZE})
        plt.title('Relative Difference Ratio Analysis')
        # plt.tight_layout()

        # +++++++++++++++++++++ SAVE AND/OR DISPLAY +++++++++++++++++++++ #
        if filename:
            pass
        else:
            filename = 'relative_ratio.png'
        if save:
            if directory:
                if not os.path.exists(directory):
                    os.mkdir(directory)
                fig_path = os.path.join(directory, filename)
            else:
                fig_path = filename
            plt.savefig(fig_path, dpi=600)
        if display:
            plt.show()
