import random

from utility import Preferences, encode_line

with open("candidates.txt", "r") as file:
    candidates = file.read().splitlines()

# %%
preferences = Preferences(candidates)

# %%
for _ in range(10):
    c1, c2 = random.sample(candidates, 2)
    if not preferences.has_voted(c1, c2):
        print(encode_line(c1, c2, "?"))
        vote = input()
        p = 1.0 if vote == "1" else -1.0 if vote == "2" else 0.0
        preferences.insert(c1, c2, p)

# %%
preferences.save()

# %%
preferences.rank_table().sort_values()

# %%
print(*[f"{v * 100:.0f}" for v in preferences.rank_table().values], sep="\n")
