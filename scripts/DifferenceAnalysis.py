import os
import sys
import glob
import copy
# import platform
# if platform.system() == 'Windows':
#     FIXME: DO SOMETHING with os.path.sep

# from cycler import cycler
import numpy as np
from matplotlib import pyplot as plt

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from saxsio import dat, gnom
from utils import run_system_command


def get_data_dict(dat_file, smooth=False):
    data_dict = dict()
    filename = dat_file.split(os.path.sep)[-1]
    data_dict['filepath'] = dat_file
    data_dict['filename'] = filename
    if 'A_' in filename[0:2]:
        start = 0
    elif 'S_A_' in filename[0:4]:
        start = 2
    else:
        start = -2
    data_dict['label'] = filename[start+2:].replace('.dat', '').replace('_', ' ')
    data_dict['linestyle'] = '-'
    try:
        q, intensity, error = dat.load_RAW_dat(dat_file)
    except NotImplementedError:
        q, intensity, error = dat.load_dat(dat_file)
    data_dict['q'] = q
    if smooth:
        data_dict['I'] = dat.smooth_curve(intensity, window_length=25, polyorder=5)
        data_dict['err'] = dat.smooth_curve(error, window_length=25, polyorder=5)
    else:
        data_dict['I'] = intensity
        data_dict['err'] = error
    return data_dict


def subtract_data_dict(data_dict_list, buffer_dict, smooth=False,
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
            # data_dict['I'] = dat.scale_curve((data_dict['q'], data_dict['I']),
            #                                  (ref_q, ref_I), qmin=scale_qmin, qmax=scale_qmax)
            data_dict['I'], data_dict['scaling_factor'] = \
                dat.scale_curve((data_dict['q'], data_dict['I']),
                                (ref_q, ref_I), qmin=scale_qmin, qmax=scale_qmax,
                                inc_factor=True)
            print('For {0} file, the scaling factor is {1}.'.format(
                data_dict['filename'], data_dict['scaling_factor']))
        data_dict['I'] -= buffer_dict['I']
        if smooth:
            data_dict['I'] = dat.smooth_curve(data_dict['I'])
    return data_dict_list


class DifferenceAnalysis(object):
    # ----------------------------------------------------------------------- #
    #                         CLASS VARIABLES                                 #
    # ----------------------------------------------------------------------- #
    # print(plt.style.available)
    # plt.style.use('classic')
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
    # plt.rcParams['axes.formatter.limits'] = (-3, 4)
    # plt.rcParams['xtick.direction'] = 'in'
    # plt.rcParams['ytick.direction'] = 'in'
    # plt.rcParams['axes.autolimit_mode'] = 'round_numbers'
    # plt.rcParams['axes.xmargin'] = 0
    # plt.rcParams['axes.ymargin'] = 0
    # plt.rcParams['axes.prop_cycle'] = cycler(color='bgrcmyk')

    PLOT_LABEL = {'family': 'sans-serif',
                  'weight': 'normal',
                  'size': 14}
    plt.rc('font', **PLOT_LABEL)
    plt.rc('text', **{'latex.unicode': True})

    LEGEND_SIZE = 12
    DPI = 300
    PLOT_NUM = 0

    XLABEL = dict()
    XLABEL['q'] = r'Scattering Vector, $q$ $(\mathrm{\AA^{-1}})$'
    XLABEL['guinier'] = r'$q^2$ $(\mathrm{\AA^{-2}})$'
    XLABEL['kratky'] = r'Scattering Vector, $q$ $(\mathrm{\AA^{-1}})$'
    XLABEL['porod'] = r'$q^4$ $(\mathrm{\AA^{-4}})$'
    YLABEL = dict()
    YLABEL['I'] = r'Intensity (arb. units.)'
    YLABEL['err'] = r'Error of Intensity (arb. units.)'
    YLABEL['log_I'] = r'$\log(I)$'
    YLABEL['guinier'] = r'$\ln(I(q))$'
    YLABEL['kratky'] = r'$I(q) \cdot q^2$'
    YLABEL['porod'] = r'$I(q) \cdot q^4$'
    YLABEL['relative_diff'] = r'Relative Ratio (%)'
    YLABEL['absolute_diff'] = r'Absolute Difference (arb. units.)'
    YLABEL['err_relative_diff'] = r'Relative Ratio (%)'
    YLABEL['err_absolute_diff'] = r'Absolute Difference (arb. units.)'

    # ----------------------------------------------------------------------- #
    #                         CONSTRUCTOR METHOD                              #
    # ----------------------------------------------------------------------- #
    def __init__(self, data_dict_list, buffer_dict=None,
                 file_list=None):
        self.file_list = file_list
        self.num_curves = len(data_dict_list)
        self.data_dict_list = data_dict_list
        if buffer_dict:
            self.buffer_dict = buffer_dict

    # ----------------------------------------------------------------------- #
    #                          CLASS METHODS                                  #
    # ----------------------------------------------------------------------- #
    @classmethod
    def from_1d_curves(cls, root_directory, buffer_dat, subtract=False,
                       scale=False, ref_dat=None, scale_qmin=None, scale_qmax=None,
                       baseline_dat=None, crop=False):
        # glob files
        file_location = os.path.join(root_directory, 'Simple_Results')
        file_list = glob.glob(file_location)
        file_list.sort()
        # read data
        return None

    @classmethod
    def from_average_dats(cls, average_dat_location, buffer_dat=None,
                          smooth=False,
                          scale=False, ref_dat=None, scale_qmin=0.0, scale_qmax=-1.0):
        # glob files
        file_list = glob.glob(average_dat_location)
        file_list.sort()
        if not file_list:
            raise FileNotFoundError('Do not find dat files.')
        average_dat_list = [fname for fname in file_list \
                            if 'buffer' not in fname.split(os.path.sep)[-1].lower()]
        if not average_dat_list:
            raise FileNotFoundError('Do not find any average dats.')
        # read buffer
        buffer_dict = dict()
        if buffer_dat:
            buffer_dict['q'], buffer_dict['I'], buffer_dict['err'] = dat.load_RAW_dat(buffer_dat)
        else:
            buffer_dat = [fname for fname in file_list \
                          if 'buffer' in fname.split(os.path.sep)[-1].lower()]
            try:
                print('Use buffer file:', buffer_dat[0])
            except IndexError:
                raise FileNotFoundError('Please check whether exist a buffer dat file.')
            buffer_dict = get_data_dict(buffer_dat[0])
        # subtracting
        data_dict_list = [get_data_dict(dat_file) for dat_file in average_dat_list]
        # smoothing must behind subtracting, cropping after scaling.
        subtracted_data_dict_list = subtract_data_dict(data_dict_list, buffer_dict, smooth=smooth,
                                                       scale=scale, ref_dat=ref_dat,
                                                       scale_qmin=scale_qmin, scale_qmax=scale_qmax)
        # Undone: pass file_list of dats into class
        return cls(subtracted_data_dict_list, buffer_dict=buffer_dict, file_list=None)

    @classmethod
    def from_subtracted_dats(cls, subtracted_dat_location, smooth=False,
                             scale=False, ref_dat=None, scale_qmin=0.0, scale_qmax=-1.0):
        # glob files
        subtracted_dat_list = glob.glob(subtracted_dat_location)
        subtracted_dat_list.sort()
        if not subtracted_dat_list:
            raise FileNotFoundError('Do not find any subtracted dat files.')
        # read data
        data_dict_list = [get_data_dict(dat_file, smooth=smooth) \
                          for dat_file in subtracted_dat_list]
        if scale:
            if ref_dat:
                ref_dict = get_data_dict(ref_dat)
                ref_q, ref_I = ref_dict['q'], ref_dict['I']
            else:
                ref_q = copy.deepcopy(data_dict_list[0]['q'])
                ref_I = copy.deepcopy(data_dict_list[0]['I'])
            for data_dict in data_dict_list:
                data_dict['I'], data_dict['scaling_factor'] = \
                    dat.scale_curve((data_dict['q'], data_dict['I']), (ref_q, ref_I),
                                    qmin=scale_qmin, qmax=scale_qmax, inc_factor=True)
                data_dict['err'] *= data_dict['scaling_factor']
                print('For {0} file, the scaling factor is {1}.'.format(
                    data_dict['filename'], data_dict['scaling_factor']))
        return cls(data_dict_list, file_list=subtracted_dat_list)

    @classmethod
    def from_dats_list(cls, file_list, smooth=False,
                       scale=False, ref_dat=None, scale_qmin=0.0, scale_qmax=-1.0):
        # glob files
        if not isinstance(file_list, list):
            raise TypeError('Expect list of dat files.')
        file_list.sort()
        if not file_list:
            raise FileNotFoundError('Do not find dat files')
        # read data
        # Notice that here is no option !
        data_dict_list = [get_data_dict(dat_file, smooth=smooth) for dat_file in file_list]
        if scale:
            if ref_dat:
                ref_q, ref_I, _ = get_data_dict(ref_dat)
            else:
                ref_q = copy.deepcopy(data_dict_list[0]['q'])
                ref_I = copy.deepcopy(data_dict_list[0]['I'])
            for data_dict in data_dict_list:
                data_dict['I'], data_dict['scaling_factor'] = \
                    dat.scale_curve((data_dict['q'], data_dict['I']), (ref_q, ref_I),
                                    qmin=scale_qmin, qmax=scale_qmax, inc_factor=True)
                print('For {0} file, the scaling factor is {1}.'.format(
                    data_dict['filename'], data_dict['scaling_factor']))
        return cls(data_dict_list, file_list=file_list)

    # ----------------------------------------------------------------------- #
    #                         INSTANCE METHODS                                #
    # ----------------------------------------------------------------------- #
    def data_dict_keys(self):
        return self.data_dict_list[0].keys()

    def data_dict_label(self):
        return [data_dict['label'] for data_dict in self.data_dict_list]

    def update_linestyle(self, dash_line_index=(None,)):
        """
        index starts from 1
        """
        for i, data_dict in enumerate(self.data_dict_list):
            if i+1 in dash_line_index:
                data_dict['linestyle'] = '--'

    def calc_log_intensity(self):
        for data_dict in self.data_dict_list:
            data_dict['log_I'] = np.log10(data_dict['I'])

    def calc_relative_diff(self, baseline_index=1, baseline_dat=None):
        if not baseline_dat:
            baseline_dict = copy.deepcopy(self.data_dict_list[baseline_index-1])
        else:
            if baseline_dat in self.file_list:
                baseline_dict = copy.deepcopy(self.data_dict_list[self.file_list.index(baseline_dat)])
            else:
                baseline_dict = get_data_dict(baseline_dat)
        base_q_length = baseline_dict['q'].shape[0]
        for data_dict in self.data_dict_list:
            if data_dict['q'].shape[0] == base_q_length:
                data_dict['relative_diff'] = (data_dict['I'] - baseline_dict['I']) / baseline_dict['I']
                data_dict['relative_diff'] *= 100
            else:
                # length of difference should be the same with length of q(for plotting figures)
                # hence interpolate baseline instead of data dat.
                print('Warning: 1D length of two dat files {0} and {1} is different. ' \
                      'Try to interpolate curve to get difference.'.format(
                          data_dict['filename'], baseline_dict['filename']))
                baseline_interp_I = np.interp(data_dict['q'], baseline_dict['q'], baseline_dict['I'])
                data_dict['relative_diff'] = (data_dict['I']-baseline_interp_I) / baseline_interp_I
                data_dict['relative_diff'] *= 100

    def calc_absolute_diff(self, baseline_index=1, baseline_dat=None):
        if not baseline_dat:
            baseline_dict = copy.deepcopy(self.data_dict_list[baseline_index-1])
        else:
            baseline_dict = get_data_dict(baseline_dat)
        base_q_length = baseline_dict['q'].shape[0]
        for data_dict in self.data_dict_list:
            if data_dict['q'].shape[0] == base_q_length:
                data_dict['absolute_diff'] = data_dict['I'] - baseline_dict['I']
            else:
                # length of difference should be the same with length of q(for plotting figures)
                # hence interpolate baseline instead of data dat.
                print('Warning: 1D length of two dat files {0} and {1} is different. ' \
                      'Try to interpolate curve to get difference.'.format(
                          data_dict['filename'], baseline_dict['filename']))
                baseline_interp_I = np.interp(data_dict['q'], baseline_dict['q'], baseline_dict['I'])
                data_dict['absolute_diff'] = data_dict['I'] - baseline_interp_I

    def calc_error_relative_diff(self, baseline_index=1, baseline_dat=None):
        if not baseline_dat:
            baseline_dict = copy.deepcopy(self.data_dict_list[baseline_index-1])
        else:
            if baseline_dat in self.file_list:
                baseline_dict = copy.deepcopy(self.data_dict_list[self.file_list.index(baseline_dat)])
            else:
                baseline_dict = get_data_dict(baseline_dat)
        base_q_length = baseline_dict['q'].shape[0]
        for data_dict in self.data_dict_list:
            if data_dict['q'].shape[0] == base_q_length:
                data_dict['err_relative_diff'] = (data_dict['err'] - baseline_dict['err']) / baseline_dict['err']
            else:
                # length of difference should be the same with length of q(for plotting figures)
                # hence interpolate baseline instead of data dat.
                print('Warning: 1D length of two dat files {0} and {1} is different. ' \
                      'Try to interpolate curve to get difference.'.format(
                          data_dict['filename'], baseline_dict['filename']))
                baseline_interp_I = np.interp(data_dict['q'], baseline_dict['q'], baseline_dict['err'])
                data_dict['err_relative_diff'] = (data_dict['err']-baseline_interp_I) / baseline_interp_I
            data_dict['err_relative_diff'] *= 100

    def eval_datcrop(self, qmin, qmax):
        """
        datcrop:
        --first <N>	Index of the first point to be kept. This is mutually exclusive with smin.
 	    --last <N>	Index of the last point to be kept. This is mutually exclusive with smax.
 	    --smin <S>	Minimal s value to be kept. This is mutually exclusive with first.
 	    --smax <S>	Maximal s value to be kept. This is mutually exclusive with last.
        -o	--output DATAFILE	Relative or absolute path to save the result; if not specified, the result is printed to stdout.

        datcrop bsa.dat --first 29 --smax 2.5 -o bsa_cropped.dat
        """
        file_list = list()
        skip = list()
        for i, dat_file in enumerate(self.file_list):
            first = sum(self.data_dict_list[i]['q'] < qmin) + 1
            last = sum(self.data_dict_list[i]['q'] < qmax) + 1
            skip.append(first)
            output = os.path.join(os.path.dirname(dat_file), 'cropped_'+os.path.basename(dat_file))
            datcrop = 'datcrop {0} --first {1} --last {2} --output {3}'.format(
                dat_file.replace('\\', '/'), first, last, output.replace('\\', '/'))
            run_system_command(datcrop)
            file_list.append(output)
        return file_list, skip

    def calc_radius_of_gyration(self, options='', crop=False, del_cropped=True):
        """
        autorg:
        output for csv support:
        File,Rg,Rg StDev,I(0),I(0) StDev,First point,Last point,Quality,Aggregated
        output for ssv support:
        Rg,Rg StDev,I(0),I(0) StDev,First point,Last point,Quality,Aggregated,File

        ref: https://www.embl-hamburg.de/biosaxs/manuals/autorg.html
        --mininterval <NUMBER>	Minimum acceptable Guinier interval length in points. Default is '3'.
        """
        if self.file_list is None:
            raise FileNotFoundError('Please specifiy input dat files')
        if crop:
            file_list, skip = self.eval_datcrop(qmin=0.010, qmax=0.20)  # (1/angstrom)
        else:
            file_list = self.file_list
            skip = [0 for i in range(self.num_curves)]
        output_format = '-f csv'
        mininterval = 10  # default: 3
        autorg = 'autorg {0} {1} --mininterval {2} {3}'.format(
            ' '.join(file_list).replace('\\', '/'), output_format, mininterval, options)
        log = run_system_command(autorg).splitlines()
        if crop and del_cropped:
            for cropped_file in file_list:
                os.remove(cropped_file)
        if len(log) != 1:
            self.rg_found = True
            rg_keys = log[0].split(',')
            log_line = 0  # as a pointer to move during log.
            for i, data_dict in enumerate(self.data_dict_list):
                try:
                    rg_data = log[log_line+1].split(',')  # first line (idx=0) is key map.
                except IndexError:  # out of boundary. all the rest is no found 'Rg'.
                    data_dict['Rg'] = None
                    continue
                # compare 'File' information to avoid 'No Rg found for ***'
                if rg_data[0] == file_list[i].replace('\\', '/'):
                    log_line += 1  # move to next line
                    data_dict['Rg'] = dict()
                    data_dict['Rg']['skip'] = skip[i-1]  # skip points due to cropping
                    for j, key in enumerate(rg_keys):
                        # undone: do not record 'File' information
                        try:
                            data_dict['Rg'][key] = float(rg_data[j])
                        except ValueError:
                            data_dict['Rg'][key] = rg_data[j]
                else:
                    data_dict['Rg'] = None
        else:
            self.rg_found = False
            for data_dict in self.data_dict_list:
                data_dict['Rg'] = None

    def calc_pair_distribution(self, output_dir='.', options='', rg_options=''):
        """
        datgnom4
        calculate pair distribution function
        read GNOM file (Version 4.5a revised 09/02/02)

        ref:
        https://www.embl-hamburg.de/biosaxs/manuals/datgnom.html
        https://www.embl-hamburg.de/biosaxs/manuals/gnom.html
        """
        if 'Rg' not in self.data_dict_keys():
            self.calc_radius_of_gyration(options=rg_options)
        if self.rg_found:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            for data_dict in self.data_dict_list:
                if data_dict['Rg'] is None:
                    data_dict['pair_distribution'] = None
                else:
                    rg = data_dict['Rg']['Rg']
                    if data_dict['filename'].endswith('.dat'):
                        output_name = os.path.join(output_dir, data_dict['filename'][:-4] + '.out')
                    else:
                        print('Warning: {0} file do not end with .dat format'.format(
                            data_dict['filename']))
                        output_name = os.path.join(output_dir, data_dict['filename']+'.out')
                    skip = sum(data_dict['q'] < 0.010) + 1 # ignore q < 0.010 (1/angstrom)
                    datgnom = 'datgnom4 {0} --rg {1} --output {2} --skip {3} {4}'.format(
                        data_dict['filepath'].replace('\\', '/'), rg, output_name.replace('\\', '/'), skip, options)
                    run_system_command(datgnom)
                    data_dict['pair_distribution'] = gnom.parse_gnom_file(output_name.replace('\\', '/'))

    def calc_guinier(self):
        """
        Guinier Analysis
        qg = q ** 2
        Ig = ln(I)
        """
        for data_dict in self.data_dict_list:
            data_dict['guinier'] = dict()
            data_dict['guinier']['x'] = data_dict['q'] ** 2
            data_dict['guinier']['y'] = np.log2(data_dict['I'])  # in ln scale

    def calc_kratky(self):
        """
        Kratky Analysis
        qk = q
        Ik = I * q ** 2
        """
        for data_dict in self.data_dict_list:
            data_dict['kratky'] = dict()
            data_dict['kratky']['x'] = data_dict['q']
            data_dict['kratky']['y'] = data_dict['I'] * data_dict['q'] ** 2

    def calc_porod(self):
        """
        Porod Analysis
        qp = q ** 4
        Ip = I * q ** 4
        """
        for data_dict in self.data_dict_list:
            data_dict['porod'] = dict()
            data_dict['porod']['x'] = data_dict['q'] ** 4
            data_dict['porod']['y'] = data_dict['I'] * data_dict['porod']['x']

    # ----------------------- PLOT ------------------------#
    def plot_profiles(self, log_intensity=True, dash_line_index=(None,),
                      crop=False, crop_qmin=0.0, crop_qmax=-1.0,
                      display=True, save=False, filename=None, legend_loc='left', directory=None,
                      axes=None):
        """
        SAXS Profiles
        """
        self.PLOT_NUM += 1
        # +++++++++++++++++++ CALCULATE INTENSITY +++++++++++++++++++++++ #
        intensity_key = 'I'
        if log_intensity:
            if 'log_I' not in self.data_dict_keys():
                self.calc_log_intensity()
            intensity_key = 'log_I'

        # ++++++++++++++++++++++++++++++ PLOT +++++++++++++++++++++++++++ #
        self.update_linestyle(dash_line_index=dash_line_index)
        if axes is not None:
            ax = axes
        else:
            fig = plt.figure(self.PLOT_NUM)
            ax = plt.subplot(111)
        for data_dict in self.data_dict_list:
            crop_slice = dat.get_crop_slice(data_dict['q'], crop, crop_qmin, crop_qmax)
            ax.plot(data_dict['q'][crop_slice], data_dict[intensity_key][crop_slice],
                    label=data_dict['label'],
                    linestyle=data_dict['linestyle'], linewidth=1)
        plot_x_zeros = False
        if not log_intensity and plot_x_zeros:
            crop_slice = dat.get_crop_slice(self.data_dict_list[0]['q'], crop, crop_qmin, crop_qmax)
            zeros_x = self.data_dict_list[0]['q'][crop_slice]
            zeros_y = np.zeros_like(zeros_x)
            ax.plot(zeros_x, zeros_y, '--r')
        ax.set_xlabel(self.XLABEL['q'], fontdict=self.PLOT_LABEL)
        ax.set_ylabel(self.YLABEL[intensity_key], fontdict=self.PLOT_LABEL)
        ax.set_title(r'SAXS Subtracted Profiles')
        if axes is None:
            box = ax.get_position()
            ax.set_position([box.x0, box.y0, box.width * 1.1, box.height])
            if not log_intensity or self.num_curves < 5:
                lgd = ax.legend(loc=0, frameon=False, prop={'size': self.LEGEND_SIZE})
            else:
                if 'left' in legend_loc:
                    lgd = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),
                                    frameon=False, prop={'size': self.LEGEND_SIZE})
                elif 'down' in legend_loc:
                    lgd = ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
                                    frameon=False, prop={'size': self.LEGEND_SIZE})
        # else:
        #     lgd = ax.legend(loc='upper right', frameon=False, prop={'size': self.LEGEND_SIZE})

        # +++++++++++++++++++++ SAVE AND/OR DISPLAY +++++++++++++++++++++ #
        if not filename:
            filename = 'saxs_profiles.png'
        if axes is None:
            if save:
                if directory:
                    if not os.path.exists(directory):
                        os.mkdir(directory)
                    fig_path = os.path.join(directory, filename)
                else:
                    fig_path = filename
                fig.savefig(fig_path, dpi=self.DPI, transparent=False,
                            bbox_extra_artists=(lgd,), bbox_inches='tight')
            if display:
                # ax.legend().draggable()
                fig.tight_layout()
                plt.show()

    def plot_analysis(self, analysis, dash_line_index=(None,),
                      crop=False, crop_qmin=0.0, crop_qmax=-1.0,
                      display=True, save=False, filename=None, legend_loc='left', directory=None,
                      axes=None):
        """
        SAXS Analysis (guinier, kratky, porod)
        """
        self.PLOT_NUM += 1

        # +++++++++++++++++++++ CALCULATE ANALYSIS ++++++++++++++++++++++ #
        analysis = str(analysis).lower()
        if analysis not in self.data_dict_keys():
            try:
                eval('self.calc_{0}()'.format(analysis))
            except NameError:
                raise ValueError('Error: unsupport type of analysis. Please check again.')

        # ++++++++++++++++++++++++++++++ PLOT +++++++++++++++++++++++++++ #
        self.update_linestyle(dash_line_index=dash_line_index)
        if axes is not None:
            ax = axes
        else:
            fig = plt.figure(self.PLOT_NUM)
            ax = plt.subplot(111)
        for data_dict in self.data_dict_list:
            crop_slice = dat.get_crop_slice(data_dict['q'], crop, crop_qmin, crop_qmax)
            ax.plot(data_dict[analysis]['x'][crop_slice], data_dict[analysis]['y'][crop_slice],
                    label=data_dict['label'],
                    linestyle=data_dict['linestyle'], linewidth=1)
        ax.set_xlabel(self.XLABEL[analysis], fontdict=self.PLOT_LABEL)
        ax.set_ylabel(self.YLABEL[analysis], fontdict=self.PLOT_LABEL)
        ax.set_title(r'SAXS {0} Analysis'.format(analysis.capitalize()))
        if axes is None:
            box = ax.get_position()
            ax.set_position([box.x0, box.y0, box.width * 1.1, box.height])
            if 'left' in legend_loc:
                lgd = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),
                                frameon=False, prop={'size': self.LEGEND_SIZE})
            elif 'down' in legend_loc:
                lgd = ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
                                frameon=False, prop={'size': self.LEGEND_SIZE})

        # +++++++++++++++++++++ SAVE AND/OR DISPLAY +++++++++++++++++++++ #
        if not filename:
            filename = 'saxs_{}_analysis.png'.format(analysis)
        if axes is None:
            if save:
                if directory:
                    if not os.path.exists(directory):
                        os.mkdir(directory)
                    fig_path = os.path.join(directory, filename)
                else:
                    fig_path = filename
                fig.savefig(fig_path, dpi=self.DPI, transparent=False,
                            bbox_extra_artists=(lgd,), bbox_inches='tight')
            if display:
                # ax.legend().draggable()
                fig.tight_layout()
                plt.show()

    def plot_difference(self, difference,
                        crop=False, crop_qmin=0.0, crop_qmax=-1.0,
                        baseline_index=1, baseline_dat=None, dash_line_index=(None,),
                        display=True, save=False, filename=None, legend_loc='left', directory=None,
                        axes=None):
        """
        Sequence Difference Analysis
        """
        self.PLOT_NUM += 1

        # +++++++++++++++++++ CALCULATE DIFFERENCE ++++++++++++++++++++++ #
        diff_mode = str(difference).lower() + '_diff'
        try:
            eval('self.calc_{0}(baseline_index={1}, baseline_dat={2})'.format(
                diff_mode, baseline_index, baseline_dat))
        except NameError:
            raise ValueError('Error: unsupport mode of difference analysis. Please check again.')

        # ++++++++++++++++++++++++++++++ PLOT +++++++++++++++++++++++++++ #
        self.update_linestyle(dash_line_index=dash_line_index)
        if axes is not None:
            ax = axes
        else:
            fig = plt.figure(self.PLOT_NUM)
            ax = plt.subplot(111)
        for data_dict in self.data_dict_list:
            crop_slice = dat.get_crop_slice(data_dict['q'], crop, crop_qmin, crop_qmax)
            ax.plot(data_dict['q'][crop_slice], data_dict[diff_mode][crop_slice],
                    label=data_dict['label'],
                    linestyle=data_dict['linestyle'], linewidth=1)
        ylim = ax.get_ylim()
        if ylim[0] >= -2.0:
            lower_lim = -2.0
        else:
            lower_lim = ylim[0]
        if ylim[1] <= 2.0:
            upper_lim = 2.0
        else:
            upper_lim = ylim[1]
        ax.set_ylim([lower_lim, upper_lim])
        ax.set_xlabel(self.XLABEL['q'], fontdict=self.PLOT_LABEL)
        ax.set_ylabel(self.YLABEL[diff_mode], fontdict=self.PLOT_LABEL)
        ax.set_title(r'{0} Difference Analysis'.format(difference.lower().capitalize()))
        if axes is None:
            box = ax.get_position()
            ax.set_position([box.x0, box.y0, box.width * 1.1, box.height])
            if 'left' in legend_loc:
                lgd = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),
                                frameon=False, prop={'size': self.LEGEND_SIZE})
            elif 'down' in legend_loc:
                lgd = ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
                                frameon=False, prop={'size': self.LEGEND_SIZE})
        else:
            lgd = ax.legend(loc='upper right', frameon=False, prop={'size': self.LEGEND_SIZE})

        # +++++++++++++++++++++ SAVE AND/OR DISPLAY +++++++++++++++++++++ #
        if not filename:
            filename = '{0}.png'.format(diff_mode)
        if axes is None:
            if save:
                if directory:
                    if not os.path.exists(directory):
                        os.mkdir(directory)
                    fig_path = os.path.join(directory, filename)
                else:
                    fig_path = filename
                fig.savefig(fig_path, dpi=self.DPI, transparent=False,
                            bbox_extra_artists=(lgd,), bbox_inches='tight')
            if display:
                # ax.legend().draggable()
                # fig.tight_layout()
                plt.show()

    def plot_pair_distribution(self, output_dir='.', dash_line_index=(None,),
                               display=True, save=False, filename=None, legend_loc='left', directory=None,
                               axes=None):
        """
        Pair distribution function
        """
        self.PLOT_NUM += 1

        # +++++++++++++++++++++ CALCULATE PDF +++++++++++++++++++++++++++ #
        if 'pair_distribution' not in self.data_dict_keys():
            self.calc_pair_distribution(output_dir=output_dir)
        # print(self.data_dict_list[0]['Rg']['Rg'])
        # print(self.data_dict_list[0]['pair_distribution']['reciprocal_rg'])
        # print(self.data_dict_list[0]['pair_distribution']['real_rg'])
        # undone: check rg value between autorg and datgnom4

        if self.rg_found:
            # ++++++++++++++++++++++++++++++ PLOT +++++++++++++++++++++++++++ #
            self.update_linestyle(dash_line_index=dash_line_index)
            if axes is not None:
                ax = axes
            else:
                fig = plt.figure(self.PLOT_NUM)
                ax = plt.subplot(111)
            for data_dict in self.data_dict_list:
                if data_dict['pair_distribution'] is not None:
                     ax.plot(data_dict['pair_distribution']['r'], data_dict['pair_distribution']['pr'],
                            label=r'{0} $D_{{max}}={1:.2f}$'.format(
                                data_dict['label'], data_dict['pair_distribution']['Dmax']),
                            linestyle=data_dict['linestyle'], linewidth=1)
            ax.set_xlabel(r'$r$ $(\mathrm{\AA})$', fontdict=self.PLOT_LABEL)
            ax.set_ylabel(r'$P(r)$', fontdict=self.PLOT_LABEL)
            ax.set_title(r'Pair Distribution Function')
            ylim = ax.get_ylim()
            ax.set_ylim([0, ylim[1]])
            if axes is None:
                box = ax.get_position()
                ax.set_position([box.x0, box.y0, box.width * 1.1, box.height])
                if 'left' in legend_loc:
                    lgd = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),
                                    frameon=False, prop={'size': self.LEGEND_SIZE})
                elif 'down' in legend_loc:
                    lgd = ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
                                    frameon=False, prop={'size': self.LEGEND_SIZE})

            # +++++++++++++++++++++ SAVE AND/OR DISPLAY +++++++++++++++++++++ #
            if not filename:
                filename = 'pair_distribution.png'
            if axes is None:
                if save:
                    if directory:
                        if not os.path.exists(directory):
                            os.mkdir(directory)
                        fig_path = os.path.join(directory, filename)
                    else:
                        fig_path = filename
                    fig.savefig(fig_path, dpi=self.DPI, transparent=False,
                                bbox_extra_artists=(lgd,), bbox_inches='tight')
                if display:
                    # ax.legend().draggable()
                    # fig.tight_layout()
                    plt.show()
        else:
            print('Warning: Do not find any pair distribution function.')

    def plot_guinier_fitting(self, display=True,
                             save=False, filename=None, fig_format='png', directory=None):
        """
        Guinier fitting
        """

        # ++++++++++++++ CALCULATE GUINIER FITTING ++++++++++++++++++++++ #
        if 'guinier' not in self.data_dict_keys():
            self.calc_guinier()
        if 'Rg' not in self.data_dict_keys():
            self.calc_radius_of_gyration()

        # ++++++++++++++++++++++++++++++ PLOT +++++++++++++++++++++++++++ #
        for data_dict in self.data_dict_list:
            # Rg,Rg StDev,I(0),I(0) StDev,First point,Last point,Quality,Aggregated,
            if data_dict['Rg'] is not None:
                rg_skip = data_dict['Rg']['skip']  # skip points
                rg_slice = slice(rg_skip + int(data_dict['Rg']['First point']) - 1,
                                 rg_skip + int(data_dict['Rg']['Last point']))
                # fitting curve: ln(I(q)) = ln(I0) - Rg^2 / 3 * q^2
                fitting_curve = np.log2(data_dict['Rg']['I(0)']) \
                                - data_dict['Rg']['Rg'] ** 2 / 3 * data_dict['guinier']['x'][rg_slice]

                self.PLOT_NUM += 1
                fig, ax = plt.subplots(nrows=2, ncols=1)
                ax[0].plot(data_dict['guinier']['x'][rg_slice], data_dict['guinier']['y'][rg_slice],
                           marker='o', linestyle='None', label=data_dict['label'], linewidth=1)
                ax[0].plot(data_dict['guinier']['x'][rg_slice], fitting_curve,
                           label='Fitting', linewidth=1)
                ax[0].set_xlabel(self.XLABEL['guinier'], fontdict=self.PLOT_LABEL)
                ax[0].set_ylabel(self.YLABEL['guinier'], fontdict=self.PLOT_LABEL)
                ax[0].set_title(r'Guinier Fitting (Quality={0:.2f}%, Aggregated={1:.2f}%)'.format(
                    data_dict['Rg']['Quality'] * 100, data_dict['Rg']['Aggregated'] * 100))
                ax[0].legend(loc=0, frameon=False, prop={'size': self.LEGEND_SIZE-2})
                ax[1].plot(data_dict['q'][rg_slice], np.log10(data_dict['I'][rg_slice]),
                           marker='o', linestyle='None', label=data_dict['label'], linewidth=1)
                ax[1].set_xlabel(self.XLABEL['q'], fontdict=self.PLOT_LABEL)
                ax[1].set_ylabel(self.YLABEL['log_I'], fontdict=self.PLOT_LABEL)
                ax[1].legend(loc=0, frameon=True, prop={'size': self.LEGEND_SIZE-2})
                fig.tight_layout()

                # +++++++++++++++++++++ SAVE AND/OR DISPLAY +++++++++++++++++++++ #
                # if not filename:
                filename = 'guinier_fitting_{0}.{1}'.format(
                    data_dict['label'].replace(' ', '_'), fig_format)
                if save:
                    if directory:
                        if not os.path.exists(directory):
                            os.mkdir(directory)
                        fig_path = os.path.join(directory, filename)
                    else:
                        fig_path = filename
                    fig.savefig(fig_path, dpi=self.DPI, transparent=False, bbox_inches='tight')

        if display and self.rg_found:
            plt.show()

    def plot_error(self, dash_line_index=(None,),
                      crop=False, crop_qmin=0.0, crop_qmax=-1.0,
                      display=True, save=False, filename=None, legend_loc='left', directory=None,
                      axes=None):
        """
        SAXS error profiles
        """
        self.PLOT_NUM += 1
        # ++++++++++++++++++++++++++++++ PLOT +++++++++++++++++++++++++++ #
        self.update_linestyle(dash_line_index=dash_line_index)
        if axes is not None:
            ax = axes
        else:
            fig = plt.figure(self.PLOT_NUM)
            ax = plt.subplot(111)
        for data_dict in self.data_dict_list:
            crop_slice = dat.get_crop_slice(data_dict['q'], crop, crop_qmin, crop_qmax)
            ax.plot(data_dict['q'][crop_slice], data_dict['err'][crop_slice],
                    label=data_dict['label'],
                    linestyle=data_dict['linestyle'], linewidth=1)
        plot_x_zeros = False
        if plot_x_zeros:
            crop_slice = dat.get_crop_slice(self.data_dict_list[0]['q'], crop, crop_qmin, crop_qmax)
            zeros_x = self.data_dict_list[0]['q'][crop_slice]
            zeros_y = np.zeros_like(zeros_x)
            ax.plot(zeros_x, zeros_y, '--r')
        ax.set_xlabel(self.XLABEL['q'], fontdict=self.PLOT_LABEL)
        ax.set_ylabel(self.YLABEL['err'], fontdict=self.PLOT_LABEL)
        ax.set_title(r'SAXS Error Profiles for Subtracted Curves')
        if axes is None:
            box = ax.get_position()
            ax.set_position([box.x0, box.y0, box.width * 1.1, box.height])
            if self.num_curves < 5:
                lgd = ax.legend(loc=0, frameon=False, prop={'size': self.LEGEND_SIZE})
            else:
                if 'left' in legend_loc:
                    lgd = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),
                                    frameon=False, prop={'size': self.LEGEND_SIZE})
                elif 'down' in legend_loc:
                    lgd = ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
                                    frameon=False, prop={'size': self.LEGEND_SIZE})
        # else:
        #     lgd = ax.legend(loc='upper right', frameon=False, prop={'size': self.LEGEND_SIZE})

        # +++++++++++++++++++++ SAVE AND/OR DISPLAY +++++++++++++++++++++ #
        if not filename:
            filename = 'saxs_error_profiles.png'
        if axes is None:
            if save:
                if directory:
                    if not os.path.exists(directory):
                        os.mkdir(directory)
                    fig_path = os.path.join(directory, filename)
                else:
                    fig_path = filename
                fig.savefig(fig_path, dpi=self.DPI, transparent=False,
                            bbox_extra_artists=(lgd,), bbox_inches='tight')
            if display:
                # ax.legend().draggable()
                fig.tight_layout()
                plt.show()

    def plot_error_difference(self, difference,
                        crop=False, crop_qmin=0.0, crop_qmax=-1.0,
                        baseline_index=1, baseline_dat=None, dash_line_index=(None,),
                        display=True, save=False, filename=None, legend_loc='left', directory=None,
                        axes=None):
        """
        Sequence Difference Analysis
        """
        self.PLOT_NUM += 1

        # +++++++++++++++++++ CALCULATE DIFFERENCE ++++++++++++++++++++++ #
        diff_mode = str(difference).lower() + '_diff'
        try:
            eval('self.calc_error_{0}(baseline_index={1}, baseline_dat={2})'.format(
                diff_mode, baseline_index, baseline_dat))
        except NameError:
            raise ValueError('Error: unsupport mode of difference analysis. Please check again.')

        # ++++++++++++++++++++++++++++++ PLOT +++++++++++++++++++++++++++ #
        self.update_linestyle(dash_line_index=dash_line_index)
        if axes is not None:
            ax = axes
        else:
            fig = plt.figure(self.PLOT_NUM)
            ax = plt.subplot(111)
        for data_dict in self.data_dict_list:
            crop_slice = dat.get_crop_slice(data_dict['q'], crop, crop_qmin, crop_qmax)
            ax.plot(data_dict['q'][crop_slice], data_dict['err_'+diff_mode][crop_slice],
                    label=data_dict['label'],
                    linestyle=data_dict['linestyle'], linewidth=1)
        ylim = ax.get_ylim()
        if ylim[0] >= -2.0:
            lower_lim = -2.0
        else:
            lower_lim = ylim[0]
        if ylim[1] <= 2.0:
            upper_lim = 2.0
        else:
            upper_lim = ylim[1]
        ax.set_ylim([lower_lim, upper_lim])
        ax.set_xlabel(self.XLABEL['q'], fontdict=self.PLOT_LABEL)
        ax.set_ylabel(self.YLABEL['err_'+diff_mode], fontdict=self.PLOT_LABEL)
        ax.set_title(r'Error {0} Difference Analysis'.format(difference.lower().capitalize()))
        if axes is None:
            box = ax.get_position()
            ax.set_position([box.x0, box.y0, box.width * 1.1, box.height])
            if 'left' in legend_loc:
                lgd = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),
                                frameon=False, prop={'size': self.LEGEND_SIZE})
            elif 'down' in legend_loc:
                lgd = ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
                                frameon=False, prop={'size': self.LEGEND_SIZE})
        else:
            lgd = ax.legend(loc='upper right', frameon=False, prop={'size': self.LEGEND_SIZE})

        # +++++++++++++++++++++ SAVE AND/OR DISPLAY +++++++++++++++++++++ #
        if not filename:
            filename = '{0}.png'.format('_'.join(['error', diff_mode]))
        if axes is None:
            if save:
                if directory:
                    if not os.path.exists(directory):
                        os.mkdir(directory)
                    fig_path = os.path.join(directory, filename)
                else:
                    fig_path = filename
                fig.savefig(fig_path, dpi=self.DPI, transparent=False,
                            bbox_extra_artists=(lgd,), bbox_inches='tight')
            if display:
                # ax.legend().draggable()
                # fig.tight_layout()
                plt.show()
