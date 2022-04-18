import numpy as np
from typing import List, Dict
from match_handler import Match, MatchHandler


class DictExplore:

    def __init__(self, dico: dict=None):
        self.d = dico

        self._eq = self._null_function

        self.handled_types = (List, Dict, np.ndarray)

        self._max_print_elems = 5
        self._max_gen_elems = 5
        self._max_gen_levels = 5
        self._subval_manager = None
        self.match_handler = None

        # Word list
        self._wl = None
        self._Nwl = 0

        # Result search methods
        self._key = None
        self.res_get_val = None

    @staticmethod
    def _strictly_equal(a, b):
        return a == b

    @staticmethod
    def _a_in_b(a, b):
        return a in b

    @staticmethod
    def _null_function(a, b):
        return False

    def _choose_comparison(self, exact):
        if exact:
            self._eq = DictExplore._strictly_equal
        else:
            self._eq = DictExplore._a_in_b

    ############################# GET KEY #############################
    def find_key(self, key, exact=False, get=False, handler=None):

        # Initialize methods
        self._choose_comparison(exact)
        self._key = key
        self.match_handler = handler or MatchHandler(key, outdict=get)

        # Recursive search generator
        matches = self._find_str_in_key(self.d)

        # Display results
        outdict = self.match_handler.output(matches)

        if outdict:
            return outdict

    def _find_str_in_key(self, obj, path=[]):
        for (k, v) in get_iterator(obj):
            if self._eq(self._key, k):
                yield Match(path, k, v)
            else:
                yield from self._find_str_in_key(v, path=path + [k])

    ############################# GET VAL #############################
    def get_val(self, key, exact=False):
        self.res_get_val = {}
        self._choose_comparison(exact)
        self._search_val_of_key(self.d, key)
        return self.res_get_val

    def _search_val_of_key(self, obj, key, path=[]):
        for (k, v) in get_iterator(obj):
            if self._eq(key, k):
                self.res_get_val[k] = return_only_number_or_text(v)
            else:
                self._search_val_of_key(v,key, path=path.copy() + [k])

    ############################# DISPLAY #############################
    def display(self, obj=None, max_print_elems=5):
        if obj is None: obj=self.d
        
        self._max_print_elems = max_print_elems

        print(f"Root object type: {type(obj)}")
        self._recursive_print(obj, "")

    def _recursive_print(self, obj, tabs=""):
        # Display the tree of the nested object.

        for il, (k, v) in enumerate(get_iterator(obj)):

            if il > self._max_print_elems:
                print(f"{tabs}...")
                break

            if isinstance(v, self.handled_types):
                s = type(v)
                print(f"{tabs}{k}:{s}")
                loc_ind = "|" + " " * (len(k))
                self._recursive_print(obj=v, tabs=tabs + loc_ind)
            else:
                # We don't want to recurse further (text or number)
                print(f"{tabs}{k}: {v}")

