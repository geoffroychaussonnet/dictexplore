import numpy as np
from numpy import random as rnd


############################# RANDOM GENERATION ############################
class RandomDict:

    def __init__(self, max_level, max_elem_per_level=5):
        self._max_gen_elems = max_elem_per_level
        self._max_gen_levels = max_level

        try:
            self._wl = get_word_list()
        except:
            self._wl = ["caviar", "loutre", "flûte", "pâté", "pirouette", "cacahuète"]

        self._Nwl = len(self._wl)

    def generation(self):
        return self._random_generation(0)

    def _random_generation(self, level=0):
        # level: level of recursion

        if level == self._max_gen_levels:
            return self._random_leaf()
        else:
            ty = rnd.randint(3)
            if ty == 0:
                dico = {}
                for i in range(rnd.randint(1, self._max_gen_elems)):
                    dico[f"L{level}_E{i}"] = self._random_generation(level + 1)
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
            return {k :v for k ,v in zip(keys ,vals)}
        elif ty == 2:
            return rnd.random(rnd.randint(1, 5)).tolist()
        elif ty == 3:
            return rnd.randint(1, 5)

    def _random_scalar(self):
        ty = rnd.randint(4)
        if ty == 0:
            return rnd.random()
        elif ty == 1:
            return int(rnd.random( ) *1e9)
        elif ty == 2:
            return True
        elif ty == 3:
            return rnd.choice(self._wl)


def get_word_list():
    import urllib.request
    word_url = "https://www.mit.edu/~ecprice/wordlist.10000"
    response = urllib.request.urlopen(word_url)
    long_txt = response.read().decode()
    return long_txt.splitlines()