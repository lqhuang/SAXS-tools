"""
Usage:
    RAW_dat_parser.py -s1 <dat_files_1> -s2 <dat_files_2> --ref=<ref_dat> [options]

Options:
    -h --help               Show this screen.
    --ref=<ref_dat>         Reference RAW dat file.
    --qmin=<qmin>           qmin to calculate scaling ratio [default: 0].
    --qmax=<qmax>           qmax to calculate scaling ratio [default: 1E10].
    --diff-mode=<diff_mode>     Plot difference in absolute scale or relative scale [default: relative].
"""
import platform
import numpy as np 
from docopt import docopt
import matplotlib.pyplot as plt
from scipy.stats import linregress

SIZE = 17
plt.rc('font', size=SIZE)  # controls default text sizes

def load_RAW_dat(filepath):
    f = open(filepath, 'r')
    qs = []  # q
    Is = []  # intensity
    Es = []  # error
    while True:
        line = f.readline()
        if line:
            if line[:10] == '### HEADER':
                # print('processing HEADER section')
                pass
            elif line[:8] == '### DATA':
                # print('processing DATA section')
                for i in range(3):
                    f.readline()
                while True:
                    line = f.readline()
                    data = line.split()
                    if len(data) == 3:
                        qs.append(float(data[0]))
                        Is.append(float(data[1]))
                        Es.append(float(data[2]))
                    else:
                        break
        else:
            break
    f.close()
    qs = np.asarray(qs)
    Is = np.asarray(Is)
    Es = np.asarray(Es)
    return qs, Is, Es

def get_data_list(raw_dats, ref):
    data_list = []
    ref_qs = ref['ref_qs']
    ref_Is = ref['ref_Is']
    ref_Es = ref['ref_Es']
    for raw_dat in raw_dats:
        filename = raw_dat.split('/')[-1]
        qs, Is, Es = load_RAW_dat(raw_dat)
        data_dict = {}
        data_dict['filename'] = filename
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
    color_dict = {0:'b', 1:'g', 2:'r', 3:'c'}
        
    # making plots
    fig1 = plt.figure()
    plt.subplot(211)
    for i,data in enumerate(data_list_1):
        q = data['qs']
        q_len = len(list(filter(q_filter, q)))
        plt.semilogy(data['qs'][1:q_len], data['scaling_Is'][1:q_len], label=data['filename'], color=color_dict[i], linewidth=1.5)
    for i, data in enumerate(data_list_2):
        q = data['qs']
        q_len = len(list(filter(q_filter, q)))
        plt.semilogy(data['qs'][1:q_len], data['scaling_Is'][1:q_len], label=data['filename'], color=color_dict[i], linewidth=2, linestyle='--')
    plt.legend()
    # plt.xlim([0, 0.10])
    plt.xlim([0, 0.05])
    plt.xlabel('q')
    plt.ylabel('Intensity')
    plt.title('SAXS profiles after scaling')
    plt.subplot(212)
    for i,data in enumerate(data_list_1):
        if diff_mode == 'relative':
            q = data['qs']
            q_len = len(list(filter(q_filter, q)))
            plt.plot(data['qs'][1:q_len], data['rel_scaling_diff'][1:q_len], label=data['filename'], color=color_dict[i], linewidth=1.5)
    for i, data in enumerate(data_list_2):
        if diff_mode == 'relative':
            q = data['qs']
            q_len = len(list(filter(q_filter, q)))
            plt.plot(data['qs'][1:q_len], data['rel_scaling_diff'][1:q_len], label=data['filename'], color=color_dict[i], linewidth=2, linestyle='--')
    plt.xlabel('q')
    plt.ylabel('relative ratio')
    plt.legend(loc='upper right')
    # plt.xlim([0, 0.10])
    plt.xlim([0, 0.05])
    plt.title('%s difference after scaling' % diff_mode)
    plt.show()