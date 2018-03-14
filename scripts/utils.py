import os.path
import shlex
from functools import reduce
import subprocess
from difflib import SequenceMatcher


def run_system_command(command_string):
    """Function used to run the system command and return the log"""
    process = subprocess.Popen(
        shlex.split(command_string),  # Run system command
        stdout=subprocess.PIPE,
        # stderr=subprocess.PIPE,
    )
    output, error = process.communicate()  # Get the log.
    if error is not None:
        print(error.decode('utf-8'))
    return output.decode('utf-8')  # return the log file


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


def find_common_string(str_a, str_b):
    match = SequenceMatcher(None, str_a, str_b).find_longest_match(
        0, len(str_a), 0, len(str_b))
    common_string = str_a[match.str_a:match.size]
    return common_string


def print_arguments(args_dict):
    if 'root_directory' in args_dict.keys():
        exp_base = os.path.basename(
            os.path.realpath(args_dict['root_directory']))
    print('Input parameters for {} are:'.format(exp_base))
    for (key, value) in args_dict.items():
        print('{0}: {1}'.format(key, value))
    print('Processing now')
