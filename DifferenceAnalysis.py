import os
import glob
import numpy as np
from matplotlib import pyplot as plt
# import matplotlib as mpl
from saxsio import dat


def get_data_dict(dat_file, smooth=False, crop=False,
                  crop_qmin=0.0, crop_qmax=-1.0):
    data_dict = dict()
    filename = dat_file.split(os.path.sep)[-1]
    data_dict['filename'] = filename
    if 'A_' in filename[0:2]:
        start = 0
    elif 'S_A_' in filename[0:4]:
        start = 2
    else:
        start = -2
    data_dict['label'] = filename[start+2:].replace('.dat', '').replace('_', ' ')
    q, intensity, error = dat.load_RAW_dat(dat_file)
    if crop:
        q, intensity, error = dat.crop_curve((q, intensity, error),
                                             qmin=crop_qmin, qmax=crop_qmax)
    data_dict['q'] = q
    if smooth:
        data_dict['I'] = dat.smooth_curve(intensity)
    else:
        data_dict['I'] = intensity
    data_dict['E'] = error
    return data_dict

def subtract_data_dict(data_dict_list, buffer_dict, smooth=False,
                       crop=False, crop_qmin=0.0, crop_qmax=-1.0,
                       scale=False, ref_dat=None, scale_qmin=0.0, scale_qmax=-1.0):
    assert len(data_dict_list[0]['q']) == len(buffer_dict['q'])
    if ref_dat:
        ref_q, ref_I, _ = dat.load_RAW_dat(ref_dat)
        assert len(ref_q) == len(buffer_dict['q'])
    else:
        ref_q = data_dict_list[0]['q']
        ref_I = data_dict_list[0]['I']
    for data_dict in data_dict_list:
        data_dict['filename'] = 'S_' + data_dict['filename']
        data_dict['buffer'] = buffer_dict['filename']
        if scale:
            data_dict['I'] = dat.scale_curve((data_dict['q'], data_dict['I']),
                                             (ref_q, ref_I), qmin=scale_qmin, qmax=scale_qmax)
        data_dict['I'] -= buffer_dict['I']
        if smooth:
            data_dict['I'] = dat.smooth_curve(data_dict['I'])
        if crop:
            data_dict['q'], data_dict['I'], data_dict['E'] = \
                dat.crop_curve((data_dict['q'], data_dict['I'], data_dict['E']),
                               qmin=crop_qmin, qmax=crop_qmax)
    return data_dict_list


class DifferenceAnalysis(object):
    # ----------------------------------------------------------------------- #
    #                         CLASS VARIABLES                                 #
    # ----------------------------------------------------------------------- #
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
    # plt.style.use('seaborn-pastel')
    # plt.style.use('ggplot')

    plt.rcParams['mathtext.fontset'] = 'cm'
    plt.rcParams['mathtext.rm'] = 'serif'
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
    PLOT_LABEL = {'family': 'sans-serif',
                  'weight': 'normal',
                  'size': 14}
    plt.rc('font', **PLOT_LABEL)
    plt.rc('text', **{'latex.unicode': True})
    LEGEND_SIZE = 12
    PLOT_NUM = 0

    # ----------------------------------------------------------------------- #
    #                         CONSTRUCTOR METHOD                              #
    # ----------------------------------------------------------------------- #
    def __init__(self, data_dict_list, buffer_dict=None,
                 crop=False, crop_qmin=0.0, crop_qmax=-1.0):
        self.num_curves = len(data_dict_list)
        self.data_dict_list = data_dict_list
        self.keys = data_dict_list[0].keys()
        if buffer_dict:
            self.buffer_dict = buffer_dict
        self.crop = crop
        self.crop_qmin = crop_qmin
        self.crop_qmax = crop_qmax

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
                          smooth=False,
                          scale=False, ref_dat=None, scale_qmin=0.0, scale_qmax=-1.0,
                          crop=False, crop_qmin=0, crop_qmax=-1.0):
        # glob files
        file_list = glob.glob(average_dat_location)
        if len(file_list) == 0:
            raise FileNotFoundError('Do not find dat files')
        average_dat_list = [fname for fname in file_list \
                            if fname.split(os.path.sep)[-1].lower().startswith('a') \
                               and 'buffer' not in fname.split(os.path.sep)[-1].lower()]
        # read buffer
        buffer_dict = dict()
        if buffer_dat:
            buffer_dict['q'], buffer_dict['I'], buffer_dict['E'] = dat.load_RAW_dat(buffer_dat)
        else:
            buffer_dat = [fname for fname in file_list if 'buffer' in fname.lower()]
            # assert len(buffer_dat) == 1
            print('Use buffer file: ', buffer_dat[0])
            buffer_dict = get_data_dict(buffer_dat[0], crop=crop,
                                        crop_qmin=crop_qmin, crop_qmax=crop_qmax)
        # subtracting
        data_dict_list = [get_data_dict(dat_file, crop=crop,
                                        crop_qmin=crop_qmin, crop_qmax=crop_qmax) \
                          for dat_file in average_dat_list]
        # smoothing must behind subtracting, cropping after scaling.
        subtracted_data_dict_list = subtract_data_dict(data_dict_list, buffer_dict, smooth=smooth,
                                                       scale=scale, ref_dat=ref_dat,
                                                       scale_qmin=scale_qmin, scale_qmax=scale_qmax,
                                                       crop=crop, crop_qmin=crop_qmin, crop_qmax=crop_qmax)
        cls = DifferenceAnalysis(subtracted_data_dict_list, buffer_dict=buffer_dict)
        return cls

    @classmethod
    def from_subtracted_dats(self, subtracted_dat_location, smooth=False,
                             crop=False, crop_qmin=0.0, crop_qmax=-1.0,
                             from_average=True):
        # glob files
        file_list = glob.glob(subtracted_dat_location)
        if len(file_list) == 0:
            raise FileNotFoundError('Do not find dat files')
        # read data
        subtracted_dat_list = [fname for fname in file_list \
                               if fname.split(os.path.sep)[-1].lower().startswith('s')]
        if len(subtracted_dat_list) != 0:
            data_dict_list = [get_data_dict(dat_file, smooth=smooth, crop=crop,
                                            crop_qmin=crop_qmin, crop_qmax=crop_qmax) \
                              for dat_file in subtracted_dat_list]
            cls = DifferenceAnalysis(data_dict_list)
        elif from_average and len(subtracted_dat_list) == 0:
            cls = DifferenceAnalysis.from_average_dats(subtracted_dat_location, smooth=smooth,
                                                       crop=crop, crop_qmin=crop_qmin, crop_qmax=crop_qmax)
            print('Warning: Do not find any subtracted curves, read data from average curves')
        elif not from_average and len(subtracted_dat_list) == 0:
            raise ValueError('Do not exist subtracted dat files')
        return cls

    @classmethod
    def from_dats_list(self, dats_list, from_average=False):
        # glob files
        file_list = dats_list
        if len(file_list) == 0:
            raise FileNotFoundError('Do not find dat files')
        # read data
        # Notice that here is no option !
        data_dict_list = [get_data_dict(dat_file) for dat_file in file_list]
        cls = DifferenceAnalysis(data_dict_list)
        return cls

    # ----------------------------------------------------------------------- #
    #                         INSTANCE METHODS                                #
    # ----------------------------------------------------------------------- #
    def calc_log_intensity(self):
        for data_dict in self.data_dict_list:
            data_dict['log_I'] = np.log(data_dict['I'])
        self.keys = self.data_dict_list[0].keys()

    def calc_relative_diff(self, baseline_index=1, baseline_dat=None):
        if not baseline_dat:
            baseline_dict = self.data_dict_list[baseline_index-1]
        else:
            baseline_dict = get_data_dict(baseline_dat, crop=self.crop,
                                          crop_qmin=self.crop_qmin, crop_qmax=self.crop_qmax)
        for data_dict in self.data_dict_list:
            data_dict['relative_diff'] = (data_dict['I'] - baseline_dict['I']) / baseline_dict['I']
            data_dict['relative_diff'] *= 100
        self.keys = self.data_dict_list[0].keys()

    def calc_absolute_diff(self, baseline_dat=None):
        if not baseline_dat:
            baseline_dict = self.data_dict_list[0]
        else:
            baseline_dict = get_data_dict(baseline_dat, crop=self.crop,
                                          crop_qmin=self.crop_qmin, crop_qmax=self.crop_qmax)
        for data_dict in self.data_dict_list:
            data_dict['absolute_diff'] = data_dict['I'] - baseline_dict['I']
        self.keys = self.data_dict_list[0].keys()

    # ----------------------- PLOT ------------------------#
    def plot_profiles(self, log_intensity=True,
                      dash_line_index=(None,),
                      display=True, save=False, filename=None, legend_loc='left',
                      directory=None):
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
        ylim = ax.get_ylim()
        if ylim[0] >= 10.0:
            lower_lim = -5.0
        else:
            lower_lim = ylim[0]
        if ylim[1] <= 2.0:
            upper_lim = 5.0
        else:
            upper_lim = ylim[1]
        plt.ylim([lower_lim, upper_lim])
        plt.xlabel(r'Scattering Vector, $q$ ($\AA^{-1}$)', fontdict=self.PLOT_LABEL)
        if log_intensity:
            plt.ylabel(r'log(I) (arb. units.)', fontdict=self.PLOT_LABEL)
        else:
            plt.ylabel(r'Intensity (arb. units.)', fontdict=self.PLOT_LABEL)
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 1.1, box.height])
        if not log_intensity:
            lgd = ax.legend(loc=0, frameon=False, prop={'size':self.LEGEND_SIZE})
        else:
            if 'left' in legend_loc:
                lgd = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),
                                frameon=False, prop={'size':self.LEGEND_SIZE})
            elif 'down' in legend_loc:
                lgd = ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
                                frameon=False, prop={'size':self.LEGEND_SIZE})
        plt.title(r'SAXS Subtracted Profiles')

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
            ax.legend().draggable()
            # plt.tight_layout()
            plt.show(fig)

    def plot_relative_diff(self, baseline_index=0, baseline_dat=None,
                           dash_line_index=(None,),
                           display=True, save=False, filename=None, legend_loc='left',
                           directory=None):
        ###########   Relative Ratio  ####################
        self.PLOT_NUM += 1

        # ++++++++++++ CALCULATE RELATIVE DIFFERENCE RATIO ++++++++++++++ #
        self.calc_relative_diff(baseline_index=baseline_index, baseline_dat=baseline_dat)

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
        ylim = ax.get_ylim()
        if ylim[0] >= -2.0:
            lower_lim = -5.0
        else:
            lower_lim = ylim[0]
        if ylim[1] <= 2.0:
            upper_lim = 5.0
        else:
            upper_lim = ylim[1]
        plt.ylim([lower_lim, upper_lim])
        plt.xlabel(r'Scattering Vector, $q$ ($\AA^{-1}$)', fontdict=self.PLOT_LABEL)
        plt.ylabel(r'Relative Ratio (%)', fontdict=self.PLOT_LABEL)
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 1.1, box.height])
        if 'left' in legend_loc:
            lgd = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),
                            frameon=False, prop={'size':self.LEGEND_SIZE})
        elif 'down' in legend_loc:
            lgd = ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
                            frameon=False, prop={'size':self.LEGEND_SIZE})
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
            ax.legend().draggable()
            # plt.tight_layout()
            plt.show(fig)
