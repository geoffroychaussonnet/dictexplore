import numbers

import numpy as np


def get_iterator(obj):
    if isinstance(obj, dict):
        iterator = (obj.items())
    elif isinstance(obj, list) or isinstance(obj, np.ndarray):
        iterator = ((str(k), v) for (k, v) in enumerate(obj))
    else:
        iterator = ()
    return iterator


def return_only_number_or_text(v):
    if isinstance(v, numbers.Number) or isinstance(v, str):
        return v
    else:
        # raise TypeError("The value linked to the key %s is neither a number nor a string." %(k))
        return type(v)


def boldize(txt, k):
    return txt.replace(k, '\033[1m' + k + '\033[0m')
