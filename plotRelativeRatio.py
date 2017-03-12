import os
import argparse
from matplotlib import pyplot as plt
import matplotlib as mpl

mpl.rc('font', family='serif', weight='normal', size=12)
PLOT_LABEL = {'family': 'serif',
                'weight': 'normal',
                'size': 16}
plt.rc('font', PLOT_LABEL)

class RelativeRatioAnalysis(object):
    
    def __init__():

def plot_RelativeRatio(root_location, scale=True, subtract=False, save_figures=True, figures_directory=None):
    
    if not figures_directory:
        fig_path = 'Figures'
        figures_directory = os.path.join(root_location, 'Figures')

    """
    color_dict = {0:'b', 1:'g', 2:'r', 3:'c'}
    qmin = float(argv['--qmin'])
    qmax = float(argv['--qmax'])
    diff_mode = argv['--diff-mode']
    """
    
    ref_qs, ref_Is, ref_Es = load_RAW_dat(ref_dat)
    ref = {}
    ref['ref_qs'] = ref_qs
    ref['ref_Is'] = ref_Is
    ref['ref_Es'] = ref_Es
    
    qmin_id = np.argmin(np.abs(ref_qs - qmin))
    qmax_id = np.argmin(np.abs(ref_qs - qmax))
    sysstr = platform.system()
    
    data_list_1 = get_data_list(raw_dats_1, ref)
    data_list_2 = get_data_list(raw_dats_2, ref)

    q_filter = lambda x: x<0.10
    
def plot_profiles():
    ###########   SAXS Profiles  ####################
    fig = plt.figure()
    if log_intensity:
        intensity = np.log(intensity)
    for i, data in enumerate(data_list_1):
        q = data['qs']
        q_len = len(list(filter(q_filter, q)))
        plt.plot(data['qs'][0:q_len], data['scaling_Is'][0:q_len], label=data['filename'], color=color_dict[i], linewidth=1.5)
    plt.legend(loc='upper right', frameon=False, prop={'size':14})
    # plt.xlim([0, 0.10])
    plt.xlim([0, 0.05])
    plt.xlabel(r'Scattering Vector, q ($nm^{-1}$)')
    if log_intensity:
        plt.ylabel('log(I) (arb. units.)', fontdict=PLOT_LABEL)
    else:
        plt.ylabel('Intensity (arb. units.)', fontdict=PLOT_LABEL)
    plt.title('SAXS profiles')
    # plt.tight_layout()
    fig_path = os.path.join(figures_directory, EXP_prefix+'SAXS_profiles.png')
    plt.savefig(fig_path, dpi=600)
    plt.close(fig)

def plot_relative_ratio():
    ###########   Relative Ratio  ####################
    fig = plt.figure()
    for i, data in enumerate(data_list_1):
        q = data['qs']
        q_len = len(list(filter(q_filter, q)))
        plt.plot(data['qs'][0:q_len], data['rel_scaling_diff'][0:q_len], label=data['filename'])
    plt.xlabel(r'Scattering Vector, q ($nm^{-1}$)')
    plt.ylabel('Relative Ratio')
    plt.legend(loc='upper right', frameon=False, prop={'size':14})
    # plt.xlim([0, 0.10])
    plt.xlim([0, 0.05])
    plt.title('Relative Ratio Analysis')
    fig_path = os.path.join(figures_directory, EXP_prefix+'_relative_ratio.png')
    # plt.tight_layout()
    plt.savefig(fig_path, dpi=600)
    plt.close(fig)

def get_data_list(raw_dats, ref):
    data_list = []
    ref_qs = ref['ref_qs']
    ref_Is = ref['ref_Is']
    ref_Es = ref['ref_Es']
    for raw_dat in raw_dats:
        filename = raw_dat.split('/')[-1]
        qs, Is, Es = load_RAW_dat(raw_dat)
        data_dict = {}
        data_dict['filename'] = filename[:-4].replace('_', ' ')
        data_dict['qs'] = qs 
        data_dict['Is'] = Is 
        data_dict['Es'] = Es 
        data_dict['abs_diff'] = Is - ref_Is
        data_dict['rel_diff'] = (Is - ref_Is) / ref_Is
        scaling_factor =  1
        data_dict['scaling_factor'] = str(scaling_factor)[:5]
        data_dict['scaling_Is'] = scaling_factor * Is
        data_dict['abs_scaling_diff'] = scaling_factor * Is - ref_Is
        data_dict['rel_scaling_diff'] = (scaling_factor * Is - ref_Is) / ref_Is
        data_list.append(data_dict)
        print('scaling factor for %s: %.3f' % (raw_dat, scaling_factor))
    return data_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--root_directory', help='Root directory for EXPERIMENTS data')
    parser.add_argument('-f', '--figures_directory',
                        help='Figures directory in root directory for CorMap Analysis (default=Figures)',
                        default='Figures')
    parser.add_argument('--scale', help='Whether to scale curves (default=False)',  type=bool, default=False)
    args = parser.parse_args()
    root_location = args.root_directory
    figures_directory = os.path.join(root_location, args.figures_directory)
    scale = args.scale
    plot_RelativeRatio(root_location, scale=True,
                       save_figures=True, figures_directory=figures_directory)

