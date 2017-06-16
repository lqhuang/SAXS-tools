import os
from functools import reduce
from difflib import SequenceMatcher

def str2bool(para):
    if para.lower() in ('true', 'yes', 't', 'y', '1'):
        return True
    elif para.lower() in ('false', 'no', 'f', 'n', '0'):
        return False
    else:
        from argparse import ArgumentTypeError
        raise ArgumentTypeError('Boolean value expected.')

def find_common_string_from_list(string_list):
    common_string = reduce(find_common_string, string_list)
    return common_string

def find_common_string(a, b):
    match = SequenceMatcher(None, a, b).find_longest_match(0, len(a), 0, len(b))
    common_string = a[match.a:match.size]
    return common_string

def print_arguments(args_dict):
    if 'root_directory' in args_dict.keys():
        exp_base = os.path.basename(args_dict['root_directory'])
    print('Input parameters for '+str(exp_base)+' are:')
    for (key, value) in args_dict.items():
        print(key, ':', value)
    print('Processing now')