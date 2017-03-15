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
    data_dict['label'] = filename.replace('.dat', '').replace('_', ' ')
    q, intensity, error = dat.load_RAW_dat(dat_file)
    q, intensity, error = dat.crop_curve((q, intensity, error), qmax=0.10)
    data_dict['q'] = q
    data_dict['I'] = intensity
    data_dict['E'] = error
    # data_dict['linestyle'] = '-'
    return data_dict

class DifferenceAnalysis(object):
    # ----------------------------------------------------------------------- #
    #                         CLASS VARIABLES                                 #
    # ----------------------------------------------------------------------- #
    # mpl.rc('font', family='sans-serif', weight='normal', size=16)
    PLOT_LABEL = {'family' : 'sans-serif', # 'sans-serif',
                  'weight' : 'normal',
                  'size' : 18}
    LABEL_SIZE = 14
    # plt.rc('font', **PLOT_LABEL)
    # print(plt.style.available)
    plt.style.use('classic')
    # plt.style.use('seaborn-bright')
    # plt.style.use('seaborn')
    # plt.style.use('seaborn-notebook')
    # plt.style.use('seaborn-white')
    # plt.style.use('seaborn-poster')
    # plt.style.use('seaborn-muted')
    # plt.style.use('seaborn-paper')
    # plt.style.use('bmh')
    # sns.set_style("whitegrid")
    # plt.style.use('seaborn-pastel')
    # plt.style.use('ggplot')

    plt.rc('text', **{'latex.unicode' : True})

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

        cls = None
        return cls

    @classmethod
    def from_average_dats(self, average_dat_location, buffer_dat=None,
                          scale=False, ref_dat=None):
        # glob files
        file_list = glob.glob(average_dat_location)
        if '*' in average_dat_location:
            location_str_list = average_dat_location.split(os.path.sep)[0:-1]
            temp_directory = os.path.sep.join(location_str_list)
        if len(file_list) == 0:
            raise FileNotFoundError('Do not find dat files')
        average_dat_list = [fname for fname in file_list \
                            if fname.split(os.path.sep)[-1].lower().startswith('a')]
        if buffer_dat:
            buffer_q, buffer_I, buffer_E = dat.load_RAW_dat(buffer_dat)
        else:
            buffer_dat = [fname for fname in file_list if 'buffer' in fname.lower()]
            assert len(buffer_dat) == 1
            buffer_q, buffer_I, buffer_E = dat.load_RAW_dat(buffer_dat[0])
        # subtract
        if scale:
            if not ref_dat:
                ref_dat = average_dat_list[0]
            raise NotImplementedError
        else:
            temp_file_list = list()
            for dat_file in average_dat_list:
                q, intensity, error = dat.load_RAW_dat(dat_file)
                intensity -= buffer_I
                subtracted_dat = os.path.join(temp_directory, \
                                                   'temp_S_' + os.path.basename(dat_file))
                temp_file_list.append(subtracted_dat)
                dat.write_dat(subtracted_dat, (q, intensity, error), extra_info=subtracted_dat)

            data_dict_list = [get_data_dict(dat_file) for dat_file in temp_file_list]
            remove = [os.remove(dat_file) for dat_file in temp_directory]
        cls = DifferenceAnalysis(data_dict_list)

        return cls

    @classmethod
    def from_subtracted_dats(self, subtracted_dat_location, from_average=True):
        # glob files
        file_list = glob.glob(subtracted_dat_location)
        if len(file_list) == 0:
            raise FileNotFoundError('Do not find dat files')
        # read data
        subtracted_dat_list = [fname for fname in file_list \
                               if fname.split(os.path.sep)[-1].lower().startswith('s')]
        if len(subtracted_dat_list) != 0:
            data_dict_list = [get_data_dict(dat_file) for dat_file in subtracted_dat_list]
            cls = DifferenceAnalysis(data_dict_list)
        elif from_average and len(subtracted_dat_list) == 0:
            cls = DifferenceAnalysis.from_average_dats(subtracted_dat_location, buffer_dat=None)
        elif not from_average and len(subtracted_dat_list) == 0:
            raise ValueError('Do not exist subtracted dat files')
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
            data_dict['relative_diff'] *= 100
        self.keys = self.data_dict_list[0].keys()

    def calc_absolute_diff(self, baseline_dat=None, crop=False):
        if not baseline_dat:
            baseline_dict = self.data_dict_list[0]
        else:
            baseline_dict = get_data_dict(baseline_dat)
        for data_dict in self.data_dict_list:
            data_dict['absolute_diff'] = data_dict['I'] - baseline_dict['I']
        self.keys = self.data_dict_list[0].keys()

    # ----------------------- PLOT ------------------------#
    def plot_profiles(self, log_intensity=True, dash_line_index=(None,),
                      display=True, save=False, filename=None, directory=None):
        ###########   SAXS Profiles  ####################
        self.PLOT_NUM += 1

        # ++++++++++++++++++++++++++++++ PLOT +++++++++++++++++++++++++++ #
        fig = plt.figure(self.PLOT_NUM)
        ax = plt.subplot(111)
        intensity_key = 'I'
        if log_intensity:
            if 'log_I' not in self.keys:
                self.calc_log_intensity()
            intensity_key = 'log_I'
        for i, data_dict in enumerate(self.data_dict_list):
            if i+1 in dash_line_index:
                linestyle = '--'
            else:
                linestyle = '-'
            plt.plot(data_dict['q'], data_dict[intensity_key],
                     label=data_dict['label'],
                     linestyle=linestyle, linewidth=1)
        plt.xlabel(r'Scattering Vector, q ($nm^{-1}$)', fontdict=self.PLOT_LABEL)
        if log_intensity:
            plt.ylabel(r'log(I) (arb. units.)', fontdict=self.PLOT_LABEL)
        else:
            plt.ylabel(r'Intensity (arb. units.)', fontdict=self.PLOT_LABEL)
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 1.1, box.height])
        lgd = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),
                        frameon=False, prop={'size':self.LABEL_SIZE})
        plt.title(r'SAXS Subtracted Profiles')
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
            plt.savefig(fig_path, dpi=600, bbox_extra_artists=(lgd,), bbox_inches='tight')
        if display:
            plt.show(fig)

    def plot_relative_diff(self, baseline_dat=None, dash_line_index=(None,),
                           display=True, save=False, filename=None, directory=None):
        ###########   Relative Ratio  ####################
        self.PLOT_NUM += 1

        # ++++++++++++ CALCULATE RELATIVE DIFFERENCE RATIO ++++++++++++++ #
        self.calc_relative_diff(baseline_dat=baseline_dat)

        # ++++++++++++++++++++++++++++++ PLOT +++++++++++++++++++++++++++ #
        fig = plt.figure(self.PLOT_NUM)
        ax = plt.subplot(111)
        for i, data_dict in enumerate(self.data_dict_list):
            if i+1 in dash_line_index:
                linestyle = '--'
            else:
                linestyle = '-'
            plt.plot(data_dict['q'], data_dict['relative_diff'],
                     label=data_dict['label'],
                     linestyle=linestyle, linewidth=1)
        plt.xlabel(r'Scattering Vector, q ($nm^{-1}$)', fontdict=self.PLOT_LABEL)
        plt.ylabel(r'Relative Ratio (%)', fontdict=self.PLOT_LABEL)
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 1.1, box.height])
        lgd = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),
                        frameon=False, prop={'size':self.LABEL_SIZE})
        # lgd = ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
        #                 frameon=False, prop={'size':self.LABEL_SIZE})
        if display:
            ax.legend().draggable()
        plt.title(r'Relative Difference Ratio Analysis')

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
            plt.savefig(fig_path, dpi=600, bbox_extra_artists=(lgd,), bbox_inches='tight')
        if display:
            plt.show(fig)
