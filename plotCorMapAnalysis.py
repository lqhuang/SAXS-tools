import os
import re
import glob
import difflib
import argparse
from matplotlib.pyplot import close
from CorMapAnalysis import ScatterAnalysis
from saxsio import dat
from utils import find_common_string_from_list


def plot_CorMapAnalysis(root_directory, skip=0,
                        subtract=True, buffer_dat=None,
                        scale=False, ref_dat=None, scale_qmin=0.0, scale_qmax=-1.0,
                        crop=False, crop_qmin=0.0, crop_qmax=-1.0,
                        display=False, save_figures=True,
                        fig_format='png', figures_directory=None):
    # check Frames directory
    exists_frames_directory = os.path.exists(os.path.join(root_directory, 'Frames'))
    exists_valid_frames_directory = os.path.exists(os.path.join(root_directory, 'Valid_Frames'))
    if exists_frames_directory and exists_valid_frames_directory:
        file_location = os.path.join(root_directory, 'Frames')
        skip = 0
    elif exists_frames_directory and not exists_valid_frames_directory:
        file_location = os.path.join(root_directory, 'Frames')
        skip = 0
    elif not exists_frames_directory and exists_valid_frames_directory:
        file_location = os.path.join(root_directory, 'Valid_Frames')
        skip = 0
    else:
        raise ValueError('Do not exist frames directory')
    # glob files
    file_list = glob.glob(os.path.join(file_location, '*'))
    buffer_dat_list = list()
    data_dat_list = list()
    frame_num_list = list()
    for fname in file_list:
        if 'buffer' in fname.lower():
            buffer_dat_list.append(fname)
        else:
            data_dat_list.append(fname)
            frame_num = re.findall(r'\d+', fname)[-1]
            frame_num_list.append(float(frame_num))
    assert sorted(frame_num_list) == frame_num_list # check sequence of frame_num
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
    print(r'ref dat file: ', ref_dat.split(os.path.sep)[-1])
    print(r'buffer dat file:', buffer_dat.split(os.path.sep)[-1])
    subtract_directory = os.path.join(root_directory, 'Subtract')
    subtract_dat_list = dat.subtract_curves(data_dat_list, buffer_dat, subtract_directory, prefix='data',
                                            scale=scale, ref_dat=ref_dat,
                                            scale_qmin=scale_qmin, scale_qmax=scale_qmax,
                                            crop=crop, crop_qmin=crop_qmin, crop_qmax=crop_qmax)
    # plot CorMap
    subtract_dat_location = find_common_string_from_list(subtract_dat_list)
    scat_obj = ScatterAnalysis.from_1d_curves(subtract_dat_location + '*')
    if not figures_directory:
        figures_directory = os.path.join(root_directory, 'Figures')
    EXP_prefix = os.path.basename(root_directory)
    scat_obj.plot_cormap(display=display, save=save_figures,
                         filename=EXP_prefix+'_cormap.'+fig_format,
                         directory=figures_directory)
    scat_obj.plot_heatmap(display=display, save=save_figures,
                          filename=EXP_prefix+'_heatmap.'+fig_format,
                          directory=figures_directory)

    close('all')
    # num_frames = len(subtract_dat_list)
    # cormap_step = 10
    # for last_frame in range(cormap_step, num_frames+cormap_step, cormap_step):
    #     scat_obj.plot_cormap(display=display, last=last_frame,
    #                          save=save_figures, filename=EXP_prefix+'_cormap_1_to_'+str(last_frame)+'.'+fig_format,
    #                          directory=figures_directory)
    # 
    # close('all')

if __name__ == '__main__':
    # working_directory = r'E:\2017\201703\20170310'
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--root_directory', help='Root directory for EXPERIMENTS data')
    parser.add_argument('-f', '--figures_directory',
                        help='Figures directory in root directory for CorMap Analysis (default=Figures)',
                        default='Figures')
    
    parser.add_argument('--skip', help='Frames need to be skipped (default=1)', type=int, default=0)
    
    parser.add_argument('--crop', help='Whether to crop curves (default=False)', type=bool, default=False)
    parser.add_argument('--crop_qmin', help='min q for cropping',  type=float, default=0.0)
    parser.add_argument('--crop_qmax', help='max q for cropping',  type=float, default=-1.0)

    parser.add_argument('--scale', help='Whether to scale curves (default=False)', type=bool, default=False)
    parser.add_argument('--scale_qmin', help='min q for scaling',  type=float, default=0.0)
    parser.add_argument('--scale_qmax', help='max q for scaling',  type=float, default=-1.0)
    
    args = parser.parse_args()
    print(args)
    root_directory = args.root_directory
    figures_directory = os.path.join(root_directory, args.figures_directory)
    skip = args.skip

    scale = args.scale
    scale_qmin = args.scale_qmin
    scale_qmax = args.scale_qmax

    crop = args.crop
    crop_qmin = args.crop_qmin
    crop_qmax = args.crop_qmax
        
    plot_CorMapAnalysis(root_directory, subtract=True, skip=skip,
                        scale=scale, scale_qmin=scale_qmin, scale_qmax=scale_qmax,
                        crop=crop, crop_qmin=crop_qmin, crop_qmax=crop_qmax,
                        save_figures=True, figures_directory=figures_directory)
