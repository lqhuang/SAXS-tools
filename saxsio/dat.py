import os
import numpy as np 
import matplotlib.pyplot as plt
from scipy.stats import linregress


def load_iq_dat(filepath):
    with open(filepath, 'r') as f:
        q = []
        intensity = []
        line = []
        while True:
            line = f.readline()
            data = line.split()
            if data:
                if data[0] == '#':
                    pass
                else:
                    q.append(float(data[0]))
                    intensity.append(float(data[1]))
            else:
                break

    q = np.asarray(q)
    intensity = np.asarray(intensity)

    return q, intensity

def load_dat(filepath):
    with open(filepath, 'r') as f:
        qs = []  # q
        Is = []  # intensity
        Es = []  # error
        while True:
            line = f.readline()
            if line:
                if line[:10] == '### HEADER':
                    # print('processing HEADER section')
                    pass
                elif line[0] == '#':
                    # print('processing DATA section')
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
    qs = np.asarray(qs)
    Is = np.asarray(Is)
    Es = np.asarray(Es)
    return qs, Is, Es


def load_RAW_dat(filepath):
    with open(filepath, 'r') as f:
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
    qs = np.asarray(qs)
    Is = np.asarray(Is)
    Es = np.asarray(Es)
    return qs, Is, Es


def write_dat(filepath, RAW_dat, extra_info=None):
    """
    input:
        filepath: filepath for save
        RAW_dat: (qs, Is, Es)
        extra_info: string
    """
    # check input
    RAW_dat_mat = np.vstack(RAW_dat).T
    length, numbers = RAW_dat_mat.shape 
    assert numbers == 3

    with open(filepath, 'w') as f:
        if extra_info is not None:
            f.write('# ' + str(extra_info) + '\n')
        for i in range(length):
            seq = RAW_dat_mat[i]
            content = '{0:.6e} {1:.6e} {2:.6e} \n'.format(seq[0], seq[1], seq[2])
            f.write(content)


def scale_curve(raw_dat, ref_dat, qmin, qmax):
    """
    Scale 1D scatter curve
    input:
        raw_dat: (q, I)
        ref_dat: (q, I)
        qmin:
        qmax:
    output:
    """
    raw_q, raw_I = raw_dat[0], raw_dat[1]
    ref_q, ref_I = ref_dat[0], ref_dat[1]
    assert len(raw_q) == len(ref_q)

    qmin_idx = np.argmin(np.abs(ref_q - qmin))
    qmax_idx = np.argmin(np.abs(ref_q - qmax))
    scaling_factor =  ref_I[qmin_idx:qmax_idx].mean() / raw_I[qmin_idx:qmax_idx].mean()
    scaling_I = scaling_factor * raw_I

    return scaling_I

def average_curves(dats_list, step=1):
    pass
    return average_list

def subtract_curves(RAW_dats_list, ref_dat, buffer_dat, directory, qmin=0.20, qmax=0.25, prefix='data'):
    """all dats should be original format from software RAW"""
    if not os.path.exists(directory):    
        os.mkdir(directory)

    ref_q, ref_I, ref_E = load_RAW_dat(ref_dat)
    buffer_q, buffer_I, buffer_E = load_RAW_dat(buffer_dat)

    subtract_dat_list = list()
    for i, filename in enumerate(RAW_dats_list, 1):
        savepath = os.path.join(directory, 'S_' + str(prefix) + '_' + str(i).zfill(5) + '.dat')
        qs, Is, Es = load_RAW_dat(filename)
        scaling_I = scale_curve((qs, Is), (ref_q, ref_I), qmin=qmin, qmax=qmax)
        subtract_I = scaling_I - buffer_I
        extra_info = filename.split('/')[-1]
        write_dat(savepath, (qs, subtract_I, Es), extra_info)
        subtract_dat_list.append(savepath)

    return subtract_dat_list