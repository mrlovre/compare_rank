import re

import numpy as np
import pandas as pd

def decode_line(line):
    return re.compile(r"<(.+)> vs. <(.+)>: (.*)").findall(line)[0]

def encode_line(c1, c2, p):
    return f"<{c1}> vs. <{c2}>: {p}"

class Preferences:
    def __init__(self, candidates, load=True):
        self.candidates = candidates
        self.n_candidates = len(self.candidates)
        self._table = pd.DataFrame(index=self.candidates, columns=self.candidates, dtype=float)

        for c1 in self.candidates:
            self._table.loc[c1, c1] = 0.0

        if load:
            try:
                with open("preferences.txt", "r") as file:
                    lines = file.read().splitlines()

                    for line in lines:
                        c1, c2, p = decode_line(line)
                        p = float(p)
                        self.insert(c1, c2, p)

            except FileNotFoundError:
                pass

    def save(self):
        with open("preferences.txt", "w") as file:
            for i1, c1 in enumerate(self.candidates):
                for c2 in self.candidates[i1 + 1:]:
                    p = self._table.loc[c1, c2]
                    if not pd.isna(p):
                        print(encode_line(c1, c2, p), file=file)

    def insert(self, c1, c2, p):
        self._table.loc[c1, c2] = p
        self._table.loc[c2, c1] = -p

    def reset(self, c1, c2):
        self.insert(c1, c2, np.nan)

    def has_voted(self, c1, c2):
        return not pd.isna(self._table.loc[c1, c2])

    def potential(self, return_consistency=True):
        N = self.n_candidates
        E = N * (N - 1) // 2
        B = np.zeros([E, N])
        f = np.zeros([E])

        for i1 in range(N):
            for i2 in range(i1 + 1, N):
                k = N * i1 + i2 - (i1 + 1) * (i1 + 2) // 2
                B[k, i1] = 1
                B[k, i2] = -1
                f[k] = self._table.iloc[i1, i2]

        f[pd.isna(f)] = 0.0

        phi = B.T @ f / N
        f_ = B @ phi
        consistency = np.linalg.norm(f_) / np.linalg.norm(f)

        if return_consistency:
            return phi, consistency

        return phi

    def rank_table(self):
        potential = self.potential(return_consistency=False)
        score = 0.5 + potential / 2
        rank_table = pd.Series(score, index=self.candidates)
        return rank_table
