from itertools import chain, combinations

# https://docs.python.org/3/library/itertools.html#recipes
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(set(iterable))
    combs = chain.from_iterable(combinations(s, r) for r in range(len(s)+1))
    res = set(tuple(sorted(x)) for x in combs)
    return res
