import numpy as np
import numbers
from numpy import random as rnd


class DictExplore():

    def __init__(self, dico: dict=None):
        self.d = dico

        self._eq = self._null_function

        self._max_print_elems = 5
        self._fields_per_level = 5
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
            self._eq = DictExplore()._strictly_equal
        else:
            self._eq = DictExplore()._a_in_b

    ############################# GET KEY #############################
    def find_key(self, key, exact=False, get=False):
        self.res_find_key = []
        self._choose_comparison(exact)
        self._find_str_in_key(self.d, key)
        if len(self.res_find_key) == 0:
            print("Key was %s not found" %key)
        if get:
            return self.res_find_key

    def _find_str_in_key(self, obj, key, path=[]):
        for (k, v) in get_iterator(obj):
            if self._eq(key, k):
                printpath = [p if p.isdigit() else "'"+p+"'" for p in (path+[k])]
                print("#### Key '%s' was found in [%s] ####" %(key, "][".join(printpath)))
                if isinstance(v, numbers.Number) or isinstance(v,str):
                    print(v)
                    self.res_find_key.append(v)
                else:
                    for k2,v2 in get_iterator(v):
                        print("Key: ", k2, " -- Value: ", return_only_number_or_text(v2))
                        self.res_find_key.append({k2:v2})
            else:
                self._find_str_in_key(v,key, path=path.copy() + [k])

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
                # if isinstance(v, numbers.Number) or isinstance(v,str):
                #     self.res_get_val[k] = v
                # else:
                #     #raise TypeError("The value linked to the key %s is neither a number nor a string." %(k))
                #     self.res_get_val[k] = type(v)
            else:
                self._search_val_of_key(v,key, path=path.copy() + [k])

    ############################# DISPLAY #############################
    def display(self, obj=None, max_print_elems=5):
        if obj is None: obj=self.d
        
        self._max_print_elems = max_print_elems

        print("Root object type:", type(obj))
        self._recursive_print(obj, "")

    def _recursive_print(self, obj, tabs=""):
        # Display the tree of the nested object.

        for il, (k,v) in enumerate(get_iterator(obj)):

            if il > self._max_print_elems:
                print("%s..." % (tabs))
                break

            further = True
            s=""
            # If we want to iterate recursively (dict, list, ndarray)
            if   isinstance(v, dict): s="Dict"
            elif isinstance(v, list): s="List"
            elif isinstance(v, np.ndarray): s="NpArray"
            else:
                # We don't want to recurse further (text or number)
                further = False

            print("%s%s:%s" % (tabs, k, s), end="")

            if further:
                loc_ind = "|" + " " * (len(k))
                print()
                self._recursive_print(obj=v, tabs=tabs + loc_ind)
            else:
                print(v)

    ############################# RANDOM GENERATION #############################
    def random_generation(self, max_level, fields_per_level=5):
        self._fields_per_level = fields_per_level
        self._max_gen_levels = max_level

        if self._wl is None:
            self._wl = get_word_list()
            self._Nwl = len(self._wl)

        return self._random_generation(0)

    def _random_generation(self, level=0):
        # level: level of recursion
        # max_gen_levels: max depth
        # field per level: number of field per level, randomly dran

        if level == self._max_gen_levels:
            ty = rnd.randint(3)
            if ty == 0:
                return rnd.random(rnd.randint(1,5))
            elif ty == 1:
                n = rnd.randint(1,5)
                return {self._wl[rnd.randint(self._Nwl)]:self._wl[rnd.randint(self._Nwl)] for i in range(n)}
            elif ty == 2:
                return rnd.randint(1,5)
        else:
            ty = rnd.randint(3)
            if ty == 0:
                dico = {}
                for i in range(rnd.randint(1,self._fields_per_level)):
                    dico["L%i_F%i" %(level,i)] = self._random_generation(level+1)
                return dico
            elif ty == 1:
                liste = []
                for i in range(rnd.randint(1, self._fields_per_level)):
                    elem = self._random_generation(level + 1)
                    liste.append(elem)
                return liste
            elif ty == 2:
                array = np.zeros(rnd.randint(1, self._fields_per_level), dtype=object)
                for i in range(len(array)):
                    array[i] = self._random_generation(level + 1)
                return array

############################# HELPER FUNCTIONS #############################
def get_iterator(obj):
    if isinstance(obj,dict):
        iterator = (obj.items())
    elif isinstance(obj,list) or isinstance(obj,np.ndarray):
        iterator = ((str(k),v) for (k,v) in enumerate(obj))
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

if __name__ == "__main__":

    dico = DictExplore().random_generation(5, fields_per_level=10)
    dx = DictExplore(dico)
    dx.display()

    dx.find_key("L3", exact=True)

    keys = dx.find_key("L3", get=True)
    vals = dx.get_val("2")

    print("Done")