from __future__ import print_function, division

import os
import glob
import re
import shlex
from functools import reduce
import subprocess
from difflib import SequenceMatcher

import numpy as np
from scipy.spatial.distance import squareform
from PIL import Image

from RAW.RAWWrapper import RAWSimulator


def get_datcmp_info(scattering_curve_files):
    """
    Extract the data produced by DATCMP.

    This method is used by the constructor method of the ScatterAnalysis
    class. It runs the DATCMP program on the dataset and returns a
    dictionary containing the main results from the DATCMP run.

    Parameters
    ----------
    scattering_curve_files : str
        Location of the scattering curves for the dataset.

    Returns
    -------
    dict(str, numpy.array)
        Dictionary containing the results of the DATCMP run. The dictionary
        key is a string (with no spaces) denoting the pair of frames that
        were compared e.g. "1,2" would be frames 1 and 2. The dictionary
        value is an array of DATCMP results for the corresponding pairwise
        comparison.

    Examples
    --------
    >>>  datcmp_data = scat_obj.get_datcmp_info("saxs_files.00*.dat")
    """
    cmd = "datcmp {}".format(scattering_curve_files)
    log = run_system_command(cmd)
    # define a dictionary to store the data produced from DATCMP - this
    # value will be overwritten.
    pair_frames = []
    c_values = []
    p_values = []
    adjp_values = []
    for line in iter(log.splitlines()):
        match_obj = re.match(r'\s* \d{1,} vs', line)
        if match_obj:
            data = line.split()
            if "*" in data[5]:
                data[5] = data[5][:-1]
            pair_frames.append("{},{}".format(data[0], data[2]))
            c_values.append(int(float(data[3])))
            p_values.append(float(data[4]))
            adjp_values.append(float(data[5]))

    return (
        pair_frames,
        np.asarray(c_values, dtype=int),
        np.asarray(p_values, dtype=float),
        np.asarray(adjp_values, dtype=float),
    )


def run_system_command(command_string):
    """Function used to run the system command and return the log"""
    process = subprocess.Popen(
        # shlex.split(command_string),  # Run system command
        command_string,
        stdout=subprocess.PIPE,
        # stderr=subprocess.PIPE,
        shell=True,
    )
    output, error = process.communicate()  # Get the log.
    if error is not None:
        print(error.decode('utf-8'))
    return output.decode('utf-8')  # return the log file


def find_common_string_from_list(string_list):
    common_string = reduce(find_common_string, string_list)
    return common_string


def find_common_string(a, b):
    match = SequenceMatcher(None, a, b).find_longest_match(
        0, len(a), 0, len(b))
    common_string = a[match.a:match.size]
    return common_string


def boxsize(array_shape, center, radius=100):
    if len(center) != len(array_shape):
        raise ValueError(
            'Length of center must be the same with dimension of array')
    size = (np.minimum(curr_center + radius, max_len, dtype=int) -
            np.maximum(curr_center - radius, 0, dtype=int)
            for curr_center, max_len in zip(center, array_shape))
    return tuple(size)


def boxslice(array, center, radius=100):
    """Slice a box with given radius from ndim array and return a view.
    Please notice the size of return is uncertain which depends on boundary.

    Parameters
    ----------
    array : array_like
    Input array.

    center : tuple of int
    Center in array to boxing. For 2D array, it's (row_center, col_center).
    Length must be the same with dimension of array.

    Returns
    -------
    out : array_like
    A view of `array` with given box range.
    """
    if len(center) != array.ndim:
        raise ValueError(
            'Length of center must be the same with dimension of array')
    slicer = [
        slice(
            np.maximum(curr_center - radius, 0, dtype=int),
            np.minimum(curr_center + radius, max_len, dtype=int),
        ) for curr_center, max_len in zip(center, array.shape)
    ]
    return array[slicer]


class Simulator():
    _CACHED_ANALYSES = [
        'sasimage',
        # 'cormap',
        'cormap_heatmap',
        'sasprofile',
        'series_analysis',
        'gnom',
        'subtracted_files',
        'gnom_files',
        'image_files',
    ]

    def __init__(self):
        # FIXME: set RAW cfg path
        cfg_path = None
        self._raw_simulator = RAWSimulator(cfg_path)

        self._warehouse = {key: {} for key in self._CACHED_ANALYSES}
        self._root_dir = None

        self._GnomFileDir = 'GNOM'
        self._SubtractedFileDir = 'Subtracted'
        self._ImageFileDir = 'Data'
        self._FileDir = {
            'image_files': self._ImageFileDir,
            'subtracted_files': self._SubtractedFileDir,
            'gnom_files': self._GnomFileDir,
        }
        self._FileExt = {
            'image_files': '.tif',
            'subtracted_files': '.dat',
            'gnom_files': '.out',
        }

        x_center = int(self._raw_simulator.get_raw_settings_value('Xcenter'))
        y_center = int(self._raw_simulator.get_raw_settings_value('Ycenter'))
        image_dim = tuple(
            int(v) for v in self._raw_simulator.get_raw_settings_value(
                'MaskDimension'))

        col_center = x_center
        row_center = image_dim[0] - y_center
        self.center = [row_center, col_center]
        self.radius = 150

        mask = self._raw_simulator.get_raw_settings_value('BeamStopMask')
        if mask is None:
            mask = self._raw_simulator.get_raw_settings_value('Masks')[
                'BeamStopMask']
        self.boxed_mask = boxslice(mask, self.center, self.radius)

    def get_gnom(self, exp):
        if exp not in self._warehouse['gnom']:
            gnom_files = self.get_files(exp, 'gnom_files')
            self._warehouse['gnom'][exp] = self._raw_simulator.loadIFTMs(
                gnom_files)
        return self._warehouse['gnom'][exp]

    def get_sasprofile(self, exp):
        if exp not in self._warehouse['sasprofile']:
            sasm_files = self.get_files(exp, 'subtracted_files')
            self._warehouse['sasprofile'][exp] = self._raw_simulator.loadSASMs(
                sasm_files)
        return self._warehouse['sasprofile'][exp]

    def load_image(self, image_file):
        with Image.open(image_file) as opened_image:
            image = boxslice(
                np.fliplr(np.asarray(opened_image, dtype=float)),
                self.center,
                self.radius,
            ) * self.boxed_mask
        return image

    def get_sasimage(self, exp, image_fname):
        if exp not in self._warehouse['sasimage']:
            self._warehouse['sasimage'][exp] = {}
        if image_fname not in self._warehouse['sasimage'][exp]:
            image_file_path = os.path.join(
                self._root_dir,
                'EXP' + str(exp).zfill(2),
                self._ImageFileDir,
                image_fname,
            )
            self._warehouse['sasimage'][exp][image_fname] = self.load_image(
                image_file_path)
        return self._warehouse['sasimage'][exp][image_fname]

    def get_cormap_heatmap(self, exp, heatmap_type):
        """Return CorMap heatmap.
        
        Parameters
        ----------
        exp : [type]
            [description]
        heatmap_type : str
            options 'C', 'Pr(>C)', 'adj Pr(>C)' 
        Returns
        -------
        np.ndarray
            2D matrix of CorMap heatmap
        """
        if exp not in self._warehouse['cormap_heatmap']:
            self._warehouse['cormap_heatmap'][exp] = self.calc_cormap_heatmap(
                exp)
        return self._warehouse['cormap_heatmap'][exp][heatmap_type]

    def get_files(self, exp, file_type):
        """Return full path of files as a list.
        
        Parameters
        ----------
        exp : [type]
            [description]
        file_type : [type]
            'subtracted_files',
            'gnom_files',
            'image_files',
        Returns
        -------
        list :
            path of files
        """
        if exp not in self._warehouse[file_type]:
            file_pattern = os.path.join(
                self._root_dir, 'EXP' + str(exp).zfill(2),
                self._FileDir[file_type], '*' + self._FileExt[file_type])
            file_list = glob.glob(file_pattern)
            file_list.sort()
            # remove buffer file
            for each in reversed(file_list):
                if 'buffer' in each.lower():
                    file_list.remove(each)
            self._warehouse[file_type][exp] = file_list
        return self._warehouse[file_type][exp]

    def reset_exp(self, exp: int):
        for key in self._CACHED_ANALYSES:
            if exp in self._warehouse[key]:
                self._warehouse[key].pop(exp)

    def calc_cormap_heatmap(self, exp):
        # heatmap_type options: 'C', 'Pr(>C)', 'adj Pr(>C)'
        file_list = self.get_files(exp, 'subtracted_files')
        file_pattern = find_common_string_from_list(file_list)

        scattering_curve_files = '%s*' % file_pattern
        _, c_values, p_values, adjp_values = get_datcmp_info(
            scattering_curve_files)
        cormap_heatmap = dict()
        cormap_heatmap['C'] = squareform(c_values)
        num_rows, num_cols = cormap_heatmap['C'].shape
        eye_matrix = np.eye(num_rows, num_cols)
        cormap_heatmap['Pr(>C)'] = squareform(p_values) + eye_matrix
        cormap_heatmap['adj Pr(>C)'] = squareform(adjp_values) + eye_matrix
        return cormap_heatmap


raw_simulator = Simulator()
