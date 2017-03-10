import os
import re
import glob
import difflib
from matplotlib import pyplot as plt
from CorMapAnalysis import ScatterAnalysis
from saxsio import dat
from utils import find_common_string_from_list

def plot_CorMapAnalysis(location, scale=False, subtract=False, buffer=None, save=False, directory=None):
    # check frames
    if not os.path.exists(os.path.join(location, 'frames')):
        raise ValueError('Do not exist frames directory')
    file_location = os.path.join(location, 'frames', '*')
    file_list = glob.glob(file_location)
    buffer_list = list()
    dat_list = list()
    frame_num_list = list()
    for i, fname in enumerate(file_list):
        if 'buffer' in fname.lower():
            buffer_list.append(fname)
        else:
            dat_list.append(fname)
            frame_num = re.findall(r'\d+', fname)[-1]
            frame_num_list.append(float(frame_num[0]))
    assert sorted(frame_num_list) == frame_num_list

    if not buffer:
        if len(buffer_list) < 1:
            raise NotImplementedError('Do not exist buffer, please specify a buffer file')
        elif len(buffer_list) == 1:
            buffer = buffer_list[0]
        else:
            pass
            buffer = dat.average_curves(buffer_list)
    ref = dat_list[0]
    subtract_directory = os.path.join(location, 'subtract_dat')
    subtract_dat_list = dat.subtract_curves(dat_list, ref, buffer, subtract_directory,
                                            qmin=0.20, qmax=0.25, prefix='data')
    num_frames = len(subtract_dat_list)
    subtract_dat_location = find_common_string_from_list(subtract_dat_list)
    scat_obj = ScatterAnalysis.from_1d_curves(subtract_dat_location + '*')
    scat_obj.plot_cormap(display=False, save=True, filename='cormap', directory=directory)
    for last_frame in range(10, num_frames+10, 10):
        scat_obj.plot_cormap(display=False, save=True, last=last_frame,
                             filename='cormap_1_to_'+str(last_frame), directory=directory)
    scat_obj.plot_heatmap(display=False, save=True, filename='heatmap', directory=directory)
    plt.close('all')


if __name__ == '__main__':
    location = os.path.join(os.getcwd(), 'test/')
    plot_CorMapAnalysis(location, scale=True, subtract=True, save=True, directory='test/figures')