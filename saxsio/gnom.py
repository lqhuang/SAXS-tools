import os
from numpy import asarray


def parse_gnom_file(gnom_name):
    gnom_dict = dict()
    with open(gnom_name, 'r') as gnom_file:
        line = 0
        while True:
            line_string = gnom_file.readline()
            line += 1
            if line_string.find('Distance distribution') > -1:
                break
        for i in range(4):
            gnom_file.readline()
        r = list()
        pr = list()
        error = list()
        while True:
            line_string = gnom_file.readline()
            data = line_string.split()
            try:
                r.append(float(data[0]))
                pr.append(float(data[1]))
                error.append(float(data[2]))
            except ValueError:
                """
                Reciprocal space: Rg =   38.17     , I(0) =   0.1882E+02
                Real space: Rg =   38.24 +- 0.167  I(0) =   0.1882E+02 +-  0.8409E-01
                """
                gnom_dict['reciprocal_rg'] = float(data[4])
                gnom_dict['reciprocal_I0'] = float(data[8])
                break
        data = gnom_file.readline().split()
        gnom_dict['real_rg'] = float(data[4])
        gnom_dict['real_I0'] = float(data[9])
        gnom_dict['r'] = asarray(r)
        gnom_dict['pr'] = asarray(pr)
        gnom_dict['error'] = asarray(error)
        gnom_dict['Dmax'] = max(gnom_dict['r'])
    return gnom_dict
