import numpy as np
import numbers
from numpy import random as rnd
from typing import List, Dict


class DictExplore():

    def __init__(self, dico: dict=None):
        self.d = dico

        self._eq = self._null_function

        self.handled_types = (List, Dict, np.ndarray)

        self._max_print_elems = 5
        self._max_gen_elems = 5
        self._max_gen_levels = 5

        # Word list
        self._wl = None
        self._Nwl = 0

        # Result search methods
        self.res_get_val = None
        self.res_find_key = None

    @staticmethod
    def _strictly_equal(a,b):
        return a == b

    @staticmethod
    def _a_in_b(a,b):
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
    def find_key(self, key, exact=False, get=False):
        self.res_find_key = []
        self._choose_comparison(exact)
        results = self._find_str_in_key(self.d, key)
        for ire, res in enumerate(results):
            print(ire, res)
        print("Done")
        # if len(self.res_find_key) == 0:
        #     print(f"Key was {key} not found")
        # if get:
        #     return self.res_find_key

    def _find_str_in_key(self, obj, key, path=[]):
        for (k, v) in get_iterator(obj):
            print(key, path, k, self._eq(key, k))
            if self._eq(key, k):
                pathtxt = "][".join([p if p.isdigit() else f"'{p}'" for p in (path+[k])])
                pathtxt = boldize(pathtxt, key)
                text = f"#### Key '{key}' was found in [{pathtxt}] ####"
                print(text)
                yield text
                # If we want to show what contains the searched key:
                # if isinstance(v, numbers.Number) or isinstance(v,str):
                #     #print(v)
                #     #self.res_find_key.append(v)
                #     yield text, v
                # else:
                #     for k2,v2 in get_iterator(v):
                #         print(f"Key: {k2}, -- Value: {return_only_number_or_text(v2)}")
                #         self.res_find_key.append({k2:v2})
            else:
                self._find_str_in_key(v, key, path=path + [k])

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


    ############################# RANDOM GENERATION #############################
    def random_generation(self, max_level, max_elem_per_level=5):
        self._max_gen_elems = max_elem_per_level
        self._max_gen_levels = max_level

        if self._wl is None:
            #self._wl = get_word_list()
            self._wl = ["caviar", "loutre", "flûte", "pâté", "pirouette", "cacahuète"]
            self._Nwl = len(self._wl)

        return self._random_generation(0)

    def _random_generation(self, level=0):
        # level: level of recursion

        if level == self._max_gen_levels:
            return self._random_leaf()
        else:
            ty = rnd.randint(3)
            if ty == 0:
                dico = {}
                for i in range(rnd.randint(1,self._max_gen_elems)):
                    dico[f"L{level}_E{i}"] = self._random_generation(level+1)
                return dico
            elif ty == 1:
                liste = []
                for i in range(rnd.randint(1, self._max_gen_elems)):
                    elem = self._random_generation(level + 1)
                    liste.append(elem)
                return liste
            elif ty == 2:
                array = np.zeros(rnd.randint(1, self._max_gen_elems), dtype=object)
                for i in range(len(array)):
                    array[i] = self._random_generation(level + 1)
                return array

    def _random_leaf(self):
        ty = rnd.randint(4)
        if ty == 0:
            return rnd.random(rnd.randint(1, 5))
        elif ty == 1:
            n = rnd.randint(1, self._max_gen_elems)
            keys = rnd.choice(self._wl, n)
            vals = [self._random_scalar() for i in range(n)]
            return {k:v for k,v in zip(keys,vals)}
        elif ty == 2:
            return rnd.random(rnd.randint(1, 5)).tolist()
        elif ty == 3:
            return rnd.randint(1, 5)

    def _random_scalar(self):
        ty = rnd.randint(4)
        if ty == 0:
            return rnd.random()
        elif ty == 1:
            return int(rnd.random()*1e9)
        elif ty == 2:
            return True
        elif ty == 3:
            return rnd.choice(self._wl)


############################# HELPER FUNCTIONS #############################
def get_iterator(obj):
    if isinstance(obj, dict):
        iterator = (obj.items())
    elif isinstance(obj, list) or isinstance(obj,np.ndarray):
        iterator = ((str(k), v) for (k, v) in enumerate(obj))
    else:
        iterator = ()
    return iterator


def get_word_list():
    import urllib.request
    word_url = "https://www.mit.edu/~ecprice/wordlist.10000"
    response = urllib.request.urlopen(word_url)
    long_txt = response.read().decode()
    return long_txt.splitlines()

def return_only_number_or_text(v):
    if isinstance(v, numbers.Number) or isinstance(v, str):
        return v
    else:
        # raise TypeError("The value linked to the key %s is neither a number nor a string." %(k))
        return type(v)

def boldize(txt, k):
    return txt.replace(k,'\033[1m'+k+'\033[0m')


if __name__ == "__main__":

    dico = DictExplore().random_generation(5, max_elem_per_level=10)
    dx = DictExplore(dico)
    dx.display()

    #dx.find_key("L3", exact=True)

    keys = dx.find_key("L3", get=True)
    vals = dx.get_val("2")

    print("Done")