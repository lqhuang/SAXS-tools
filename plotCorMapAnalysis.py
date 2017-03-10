import os
import re
import glob
import difflib
from matplotlib import pyplot as plt
from CorMapAnalysis import ScatterAnalysis
from saxsio import dat
from utils import find_common_string_from_list

def plot_CorMapAnalysis(root_location, scale=False, subtract=True, skip=0,
                        buffer_dat=None, ref_dat=None, save=False, directory=None):
    # check frames
    if not os.path.exists(os.path.join(root_location, 'Valid_Frames')):
        raise ValueError('Do not exist frames directory')
    file_location = os.path.join(root_location, 'Valid_Frames', '*')
    file_list = glob.glob(file_location)
    buffer_dat_list = list()
    data_dat_list = list()
    frame_num_list = list()
    for i, fname in enumerate(file_list):
        if 'buffer' in fname.lower():
            buffer_dat_list.append(fname)
        else:
            data_dat_list.append(fname)
            frame_num = re.findall(r'\d+', fname)[-1]
            frame_num_list.append(float(frame_num))
    assert sorted(frame_num_list) == frame_num_list
    
    # scale and subtract
    if not buffer_dat:
        if len(buffer_dat_list) < 1:
            raise NotImplementedError('Do not exist buffer, please specify a buffer file')
        elif len(buffer_dat_list) == 1:
            buffer_dat = buffer_dat_list[0]
        else:
            pass
            # buffer_dat = dat.average_curves(buffer_dat_list, skip=skip)
    ref_dat = data_dat_list[0+skip]
    data_dat_list = data_dat_list[0+skip:]
    print(r'ref dat file: ', ref_dat)
    print(r'buffer dat file:', buffer_dat)
    subtract_directory = os.path.join(root_location, 'Subtract')
    subtract_dat_list = dat.subtract_curves(data_dat_list, buffer_dat, subtract_directory, prefix='data',
                                            scale=scale, ref_dat=ref_dat, qmin=0.15, qmax=0.20)
    
    # plot CorMap
    subtract_dat_location = find_common_string_from_list(subtract_dat_list)
    scat_obj = ScatterAnalysis.from_1d_curves(subtract_dat_location + '*')
    scat_obj.plot_cormap(display=False, save=save, filename='cormap', directory=directory)
    scat_obj.plot_heatmap(display=False, save=save, filename='heatmap', directory=directory)
    plt.close('all')
    num_frames = len(subtract_dat_list)
    cormap_step = 10
    for last_frame in range(cormap_step, num_frames+cormap_step, cormap_step):
        scat_obj.plot_cormap(display=False, last=last_frame,
                             save=save, filename='cormap_1_to_'+str(last_frame), directory=directory)
    plt.close('all')

if __name__ == '__main__':
    working_directory = r'E:\2017\201703\20170310'
    # for i in [1,2,3,4,5,6,7,8,9,10]:
    #     try:
    #         root_location = os.path.join(working_directory, 'EXP'+str(i).zfill(2))
    #         plot_CorMapAnalysis(os.path.join(root_location), scale=False, subtract=True, skip=1,
    #                             save=True, directory=os.path.join(root_location, 'Figures'))
    #     except:
    #         print('test')
    root_location = os.path.join(working_directory,  'EXP13')
    plot_CorMapAnalysis(os.path.join(root_location), scale=True, subtract=True, skip=0,
                        save=True, directory=os.path.join(root_location, 'Figures'))