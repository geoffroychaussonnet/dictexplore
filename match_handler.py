import numbers
from typing import Dict, Generator
from helper_functions import boldize, get_iterator, return_only_number_or_text


class Match:
    def __init__(self, path, k, v=None):
        self.path = path
        self.key = k
        self.val = v


class MatchHandler:
    def __init__(self, key, outdict=False):
        self._key = key
        self.outdict = outdict

    def output(self, results: Generator[Match, None, None]) -> Dict:
        output = {}
        found = 0
        for res in results:
            found += 1

            # Collect Matches
            notif = self._get_notification(res.path, res.key)
            vals = self._get_subvalues(res.val)

            # Display Matches in terminal
            print(notif)
            print("\n".join(vals))

            # If output dictionary
            if self.outdict:
                key = "/".join([p if p.isdigit() else f"{p}" for p in (res.path+[res.key])])
                output[key] = vals

        if found == 0:
            print(f"Key {self._key} was not found.")

        return output

    def _get_notification(self, path, k):
        pathtxt = "][".join([p if p.isdigit() else f"'{p}'" for p in (path+[k])])
        pathtxt = boldize(pathtxt, self._key)
        text = f"#### Key '{self._key}' was found in [{pathtxt}] ####"
        return text

    @staticmethod
    def _get_subvalues(v):
        if isinstance(v, numbers.Number) or isinstance(v, str):
            return v
        else:
            return [f"Key: {k2}, -- Value: {return_only_number_or_text(v2)}"
                    for k2, v2 in get_iterator(v)]
