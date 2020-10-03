import random

import numpy as np

from utility import Preferences, encode_line

with open("candidates.txt", "r") as file:
    candidates = file.read().splitlines()

# %%
preferences = Preferences(candidates, load=False)

# %%
for _ in range(10000):
    c1, c2 = random.sample(candidates, 2)
    if not preferences.has_voted(c1, c2):
        print(encode_line(c1, c2, "?"))
        # za simulaciju uzimamo da je bolji kandidat koji je prije na listi
        p = np.sign(candidates.index(c1) - candidates.index(c2))
        preferences.insert(c1, c2, p)

# %%
phi, consistency = preferences.potential()
preferences.rank_table().sort_values()

# %%
print(consistency)
