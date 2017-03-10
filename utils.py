from difflib import SequenceMatcher
from functools import reduce


def find_common_string_from_list(string_list):
    common_string = reduce(find_common_string, string_list)
    return common_string

def find_common_string(a, b):
    match = SequenceMatcher(None, a, b).find_longest_match(0, len(a), 0, len(b))
    common_string = a[match.a:match.size]
    return common_string
