import os
import argparse
from matplotlib import pyplot as plt
import matplotlib as mpl

mpl.rc('font', family='serif', weight='normal', size=12)
PLOT_LABEL = {'family': 'serif',
                'weight': 'normal',
                'size': 16}
plt.rc('font', PLOT_LABEL)



def plot_RelativeRatio(root_location, scale=True, subtract=False, save_figures=True, figures_directory=None):
    
    if not figures_directory:
        figures_directory = os.path.join(root_location, 'Figures')

    save_prefix = '/Users/lqhuang/Documents/CSRC/Data/SSRF_MagR/Analysis/Experiments/20161211-EXP/CanXie'

    color_dict = {0:'b', 1:'g', 2:'r', 3:'c'}
        # add signal to enable CTRL-C
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    argv = docopt(__doc__)
    ref_dat = argv['--ref']
    raw_dats_1 = argv['<dat_files_1>'].split(',')
    raw_dats_2 = argv['<dat_files_2>'].split(',')
    print(raw_dats_2)
    qmin = float(argv['--qmin'])
    qmax = float(argv['--qmax'])
    diff_mode = argv['--diff-mode']
    
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
    
    # making plots
    fig1 = plt.figure(1)
    for i, data in enumerate(data_list_1):
        q = data['qs']
        q_len = len(list(filter(q_filter, q)))
        plt.plot(data['qs'][0:q_len], data['scaling_Is'][0:q_len], label=data['filename'], color=color_dict[i], linewidth=1.5)
    for i, data in enumerate(data_list_2):
        q = data['qs']
        q_len = len(list(filter(q_filter, q)))
        plt.plot(data['qs'][0:q_len], data['scaling_Is'][0:q_len], label=data['filename'], linestyle='--', color=color_dict[i], linewidth=1.5)
    plt.legend(loc='upper right', frameon=False, prop={'size':14})
    # plt.xlim([0, 0.10])
    plt.xlim([0, 0.05])
    plt.xlabel(r'Scattering Vector, q ($nm^{-1}$)')
    plt.ylabel('Intensity')
    plt.title('SAXS profiles after scaling')
    # plt.tight_layout()
    plt.savefig(os.path.join(save_prefix, 'EXP27-SAXS_profiles_of_two_stages.png'), dpi=600)

    fig2 = plt.figure(2)
    for i, data in enumerate(data_list_1):
        if diff_mode == 'absolute':
            plt.plot(data['qs'], data['abs_scaling_diff'], label=data['filename'])
        elif diff_mode == 'relative':
            q = data['qs']
            q_len = len(list(filter(q_filter, q)))
            plt.plot(data['qs'][0:q_len], data['rel_scaling_diff'][0:q_len], label=data['filename'])
    for i, data in enumerate(data_list_2):
        if diff_mode == 'absolute':
            plt.plot(data['qs'], data['abs_scaling_diff'], label=data['filename'], linestyle='--', color=color_dict[i], linewidth=1.5)
        elif diff_mode == 'relative':
            q = data['qs']
            q_len = len(list(filter(q_filter, q)))
            plt.plot(data['qs'][0:q_len], data['rel_scaling_diff'][0:q_len], label=data['filename'], linestyle='--', color=color_dict[i], linewidth=1.5)
    plt.xlabel(r'Scattering Vector, q ($nm^{-1}$)')
    plt.ylabel('relative ratio')
    plt.legend(loc='upper right', frameon=False, prop={'size':14})
    # plt.xlim([0, 0.10])
    plt.xlim([0, 0.05])
    plt.title('%s difference after scaling' % diff_mode)
    plt.savefig(os.path.join(save_prefix, 'EXP27-relative_ratio_of_two_stages.png'), dpi=600)
    # plt.tight_layout()
    # plt.show()

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
    working_directory = r'E:\2017\201703\20170310'
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--root_directory', help='Root directory for EXPERIMENTS data',
                        default=os.path.join(working_directory, 'EXP13'))
    args = parser.parse_args()
    root_location = args.root_directory
    plot_RelativeRatio(root_location, scale=True, subtract=True, save_figures=True)

