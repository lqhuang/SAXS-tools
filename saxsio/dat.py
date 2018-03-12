import os
import numpy as np 
import matplotlib.pyplot as plt
from scipy.stats import linregress
from scipy.signal import savgol_filter


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
                if line[0] == '#':
                    pass
                elif line[0] != '#':
                    data = line.split()
                    if len(data) == 3:
                        qs.append(float(data[0]))
                        Is.append(float(data[1]))
                        Es.append(float(data[2]))
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
    if len(qs) <= 1:
        raise(NotImplementedError('Unsupportted dat file. Please check again'))
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
    if len(qs) <= 1:
        raise(NotImplementedError('Unsupportted RAW dat file. Please check again'))
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
        f.write('#' + '{0:>7} {1:>7} {2:>7}'.format('q', 'I', 'E') + '\n')
        for i in range(length):
            seq = RAW_dat_mat[i]
            content = '{0:.6e} {1:.6e} {2:.6e} \n'.format(seq[0], seq[1], seq[2])
            f.write(content)

def smooth_curve(intensity, window_length=25, polyorder=5):
    smoothing_intensity = savgol_filter(intensity,
                                        window_length=window_length, polyorder=polyorder)
    return smoothing_intensity


# least square method to scale curve
def interp(q, I):
    step = 1e-4
    qmin = np.floor(q[0]*1e3+1)/1e3
    qmax = np.floor(q[-1]*1e3)/1e3
    new_q = np.arange(qmin, qmax, step=step)
    f = interp1d(q, I)
    new_I = f(new_q)
    return new_q, new_I

def larger_or_smaller(x, qmin, qmax):
    lower_bound = x >= qmin
    upper_bound = x < qmax
    idx = np.logical_and(lower_bound, upper_bound)
    return idx

def linear_func(params, x, y):
    """
    fit y = k * x + b
    params = (k, b)
    """
    return y - (params[0] * x + params[1])

def leastsq_factor(input, ref, qmin, qmax):
    """
    Input:
    input: (q, I)
    ref: (q, I)
    """
    ref_idx = larger_or_smaller(ref[0], qmin=qmin, qmax=qmax)
    input_idx = larger_or_smaller(input[0], qmin=qmin, qmax=qmax)
    params, _ = leastsq(linear_func, (1, 0), (input[1][input_idx], ref[1][ref_idx]))
    print('intercept: ', params[1])
    return params[0]

def scale_curve(curve, ref_curve, qmin=0.0, qmax=-1.0, stat_func=np.mean,
                inc_factor=False):
    """
    Scale 1D scatter curve
    input:
        curve: (q, I)
        ref_curve: (q, I)
        qmin:
        qmax:
        inc_factor: bool, default False
            return factor or not
    output:
    """
    assert len(curve) == 2
    assert len(ref_curve) == 2
    curve_q, curve_I = curve[0], curve[1]
    ref_q, ref_I = ref_curve[0], ref_curve[1]
    if qmax < 0:
        curve_scale_idx = curve_q >= qmin
        ref_scale_idx = ref_q >= qmin
    else:
        curve_scale_idx = np.logical_and(curve_q >= qmin, curve_q < qmax)
        ref_scale_idx = np.logical_and(ref_q >= qmin, ref_q < qmax)
    scaling_factor = stat_func(ref_I[ref_scale_idx]) / stat_func(curve_I[curve_scale_idx])
    # print("scaling_factor is ", str(scaling_factor)[0:6])
    scaling_I = scaling_factor * curve_I
    if inc_factor:
        return scaling_I, scaling_factor
    else:
        return scaling_I

def crop_curve(curve, qmin=0.0, qmax=-1.0):
    """
    Crop 1D scatter curve
    input:
        curve: (q, I, E)
        qmin:
        qmax:
    output:
    """
    curve_q = curve[0]
    if qmax < 0:
        crop_idx = curve_q >= qmin
    else:
        crop_idx = np.logical_and(curve_q >= qmin, curve_q < qmax)
    curve_q = np.asarray(curve[0][crop_idx])
    curve_I = np.asarray(curve[1][crop_idx])
    curve_E = np.asarray(curve[2][crop_idx])
    return curve_q, curve_I, curve_E

def get_crop_slice(q, crop, crop_qmin, crop_qmax):
    """
    return slicing index for cropping
    """
    if crop:
        if crop_qmax < 0:
            return q >= crop_qmin
        else:
            return np.logical_and(q >= crop_qmin, q < crop_qmax)
    else:
        return q >= 0.0

def averge_curves(curves_dat_list):
    pass
    if not os.path.exists(directory):
        os.mkdir(directory)

    qs_list = list()
    Is_list = list()
    Es_list = list()
    for fname in dats_list:
        pass

    return average_dat_list

def subtract_curves(RAW_dats_list, buffer_dat, directory, prefix='data',
                    scale=False, ref_dat=None,
                    scale_qmin=0.0, scale_qmax=-1.0,
                    crop=False, crop_qmin=0.0, crop_qmax=-1):
    """all dats should be original format from software RAW"""
    if not os.path.exists(directory):    
        os.mkdir(directory)

    buffer_q, buffer_I, buffer_E = load_RAW_dat(buffer_dat)
    if crop:
        buffer_q, buffer_I, buffer_E = crop_curve((buffer_q, buffer_I, buffer_E),
                                                  qmin=crop_qmin, qmax=crop_qmax)
    if ref_dat:
        ref_q, ref_I, ref_E = load_RAW_dat(ref_dat)
        if crop:
            ref_q, ref_I, ref_E = crop_curve((ref_q, ref_I, ref_E),
                                             qmin=crop_qmin, qmax=crop_qmax)
    else:
        print('ref data not load')

    subtract_dat_list = list()
    for i, filename in enumerate(RAW_dats_list, 1):
        file_path = os.path.join(directory, 'S_' + str(prefix) + '_' + str(i).zfill(5) + '.dat')
        qs, Is, Es = load_RAW_dat(filename)
        if crop:
            qs, Is, Es = crop_curve((qs, Is, Es), qmin=crop_qmin, qmax=crop_qmax)
        if scale:
            scaling_I = scale_curve((qs, Is), (ref_q, ref_I), qmin=scale_qmin, qmax=scale_qmax)
        else:
            # print("Do not scale, scaling_factor is ", str(1))
            scaling_I = Is * 1.0
        subtract_I = scaling_I - buffer_I
        extra_info = filename.split('/')[-1]
        write_dat(file_path, (qs, subtract_I, Es), extra_info)
        subtract_dat_list.append(file_path)

    return subtract_dat_list
