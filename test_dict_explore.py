
from dict_explore import DictExplore
from random_dict_generation import RandomDict

if __name__ == "__main__":

    dico = RandomDict(5, max_elem_per_level=10).generation()

    dx = DictExplore(dico)

    dx.display()

    dx.find_key("L3", exact=True)

    keys = dx.find_key("L3", get=True)

    vals = dx.get_val("2")

    print("Done")