from typing import Callable
import numpy as np
import numbers


class DictExplore():

    def __init__(self, dico: dict=None):
        self.d = dico
        self.value = None
        self.eqfunc = self.null_function # DictExplore()._strictly_equal

    @staticmethod
    def _strictly_equal(a,b):
        return (a==b)

    @staticmethod
    def _a_in_b(a,b):
        return (a in b)

    def null_function(self, a,b):
        return False

    def _choose_comparison(self, exact):
        if exact:
            self.eqfunc = DictExplore()._strictly_equal
        else:
            self.eqfunc = DictExplore()._a_in_b

    def find_in_key(self, key, exact=False, get=False):
        self.find_result = []
        self._choose_comparison(exact)
        self._find_str_in_key(self.d, key)
        if get:
            return self.find_result

    def _find_str_in_key(self, obj, key, path=[]):
        for (k, v) in DictExplore()._get_iterator(obj):
            if self.eqfunc(key, k):
                print("#### Key '%s' was found in %s/%s ####" %(key, "/".join(path), k))
                if isinstance(v, numbers.Number) or isinstance(v,str):
                    print(v)
                    self.find_result.append(v)
                else:
                    for k2,v2 in DictExplore()._get_iterator(v):
                        print("Key: ", k2, " Value: ", v2)
                        self.find_result.append({k2:v2})
            else:
                self._find_str_in_key(v,key, path=path.copy() + [k])

    def val_of_key(self, key):
        self.value = None
        self._search_val_of_key(self.d, key)
        return self.value

    def _search_val_of_key(self, obj, key, path=[]):
        # The key as parameter must strictly equal to the key
        for (k, v) in DictExplore()._get_iterator(obj):
            if self.value is not None:
                return
            if key == k:
                if isinstance(v, numbers.Number) or isinstance(v,str):
                    self.value = v
                else:
                    raise TypeError("The value linked to the key %s is neither a number nor a string." %(k))
            else:
                self._search_val_of_key(v,key, path=path.copy() + [k])

    def display(self, obj=None):
        if obj is None: obj=self.d
        print("Object type:", type(obj))
        self._recurprint(obj, "")

    @staticmethod
    def _get_iterator(obj):
        if isinstance(obj,dict):
            iterator = (obj.items())
        elif isinstance(obj,list) or isinstance(obj,np.ndarray):
            iterator = ((str(k),v) for (k,v) in enumerate(obj))
        else:
            iterator = ()
        return iterator

    @staticmethod
    def _recurprint(obj, tabs=""):
        # Display the arborescence of the dict.
        # (D,L,N) stand for dictionnary, list and numpy array, respectively

        for (k,v) in DictExplore()._get_iterator(obj):
            further = True
            s=""
            # If we want to iterate recursively (dict, list, ndarray)
            if   isinstance(v, dict): s="Dict"
            elif isinstance(v, list): s="List"
            elif isinstance(v, np.ndarray): s="NpArray"
            # If we don't want to iterate (text or number)
            else:
                further = False
                if isinstance(v, str): s="T"

            print("%s%s:%s" % (tabs, k, s), end="")

            if further:
                loc_ind = "|" + " " * (len(k))
                print()
                DictExplore()._recurprint(obj=v, tabs=tabs + loc_ind)
            else:
                print(v)

    @staticmethod
    def random_generation(levmax, Nfield_per_level=5, wl=None, level=0):
        # level: level of recursion
        # levmax: max depth
        # field per level: number of field per level, randomly dran
        from numpy import random as rnd

        if wl is None:
            wl = get_word_list()

        if level == levmax:
            if rnd.randint(2)==0:
                return rnd.random(rnd.randint(1,5))
            else:
                n,m = rnd.randint(1,5), len(wl)
                return {wl[rnd.randint(m)]:wl[rnd.randint(m)] for i in range(n)}
        else:
            type = rnd.randint(3)
            if type == 0:
                dico = {}
                for i in range(rnd.randint(1,Nfield_per_level)):
                    dico["L%i_F%i" %(level,i)] = DictExplore().random_generation(levmax, Nfield_per_level, wl, level+1)
                return dico
            elif type == 1:
                liste = []
                for i in range(rnd.randint(1, Nfield_per_level)):
                    elem = DictExplore().random_generation(levmax, Nfield_per_level, wl, level + 1)
                    liste.append(elem)
                return liste
            elif type == 2:
                array = np.zeros(rnd.randint(1, Nfield_per_level), dtype=object)
                for i in range(len(array)):
                    array[i] = DictExplore().random_generation(levmax, Nfield_per_level, wl, level + 1)
                return array

def get_word_list():
    import urllib.request
    word_url = "https://www.mit.edu/~ecprice/wordlist.10000"
    response = urllib.request.urlopen(word_url)
    long_txt = response.read().decode()
    return long_txt.splitlines()


if __name__ == "__main__":

    dico = DictExplore().random_generation(5)
    dx = DictExplore(dico)
    dx.display()
    print("Done")