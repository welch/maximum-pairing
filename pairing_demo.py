"""
Use maximum_pairing() to match different pairs of club
members week after week, with history.

```
> python demo.py

... lots of solver spew ....

ids: ('alice', 'bob', 'carol', 'diane', 'edgar')
exclude: [('alice', 'bob')]
weekly pairings
week 0: [('.', 'bob'), ('alice', 'diane'), ('carol', 'edgar')]
week 1: [('.', 'edgar'), ('alice', 'carol'), ('bob', 'diane')]
week 2: [('.', 'alice'), ('bob', 'carol'), ('diane', 'edgar')]
week 3: [('.', 'bob'), ('alice', 'edgar'), ('carol', 'diane')]
week 4: [('.', 'carol'), ('alice', 'diane'), ('bob', 'edgar')]
week 5: [('.', 'diane'), ('alice', 'edgar'), ('bob', 'carol')]
week 6: [('.', 'alice'), ('bob', 'diane'), ('carol', 'edgar')]
week 7: [('.', 'bob'), ('alice', 'carol'), ('diane', 'edgar')]
week 8: [('.', 'edgar'), ('alice', 'diane'), ('bob', 'carol')]
week 9: [('.', 'alice'), ('bob', 'edgar'), ('carol', 'diane')]
```

Because there are an odd number of members, one will be left out
of the pairing. A placeholder (".") is used so that history can
be tracked for this odd-person-out and spread across the members.

The simulation also allows random participant dropouts each week
(change the dropouts parameter in the call to simulate_turns)
```
weekly pairings
week 0: [('alice', 'diane'), ('bob', 'edgar')]
week 1: [('alice', 'carol'), ('bob', 'diane')]
week 2: [('.', 'alice')]
week 3: [('.', 'carol'), ('alice', 'diane')]
week 4: [('alice', 'diane'), ('bob', 'carol')]
week 5: [('.', 'bob'), ('diane', 'edgar')]
week 6: [('.', 'bob'), ('alice', 'edgar')]
week 7: [('.', 'diane'), ('alice', 'carol'), ('bob', 'edgar')]
week 8: [('alice', 'diane'), ('carol', 'edgar')]
week 9: [('bob', 'edgar')]
```

"""
import numpy as np
from maximum_pairing import maximum_pairing


def simulate_turns(ids, exclude_pairs=[], n_turns=10, dropouts=True):
    """
    take maximum_pairing() out for a spin by making successive pairings
    while accumulating history, as if doing the matching over and over
    with different subsets of members wanting to participate each turn.

    Parameters
    ----------
    ids: list(ids)
        list of ids. may be strings, integers, anything that can be used as a dict key.
    exclude_pairs: list( (id1, id2), .... )
        list of pairings we should not allow.
    n_turns: int
        number of turns to simulate
    dropouts: bool
        if True, simulate random non-participants each turn (else always match all)

    Returns
    -------
    turn pairs: [ [(id1, id2), ...], ... [(id1, id2), ...] ]
        a list of each turn's pairings

    """
    N = len(ids)

    # create a placeholder 0th member that only participates when there are an odd
    # number of participants. This lets us spread the pain of being odd-person-out
    # by tracking the number of non-pairings in history.
    ids = np.concatenate([["."], ids])

    # H is the pairing history, number of turns since i,j were paired, where i < j,
    # and will be used as the edge weights in computing matches.
    # begin by assuming all i, j have never been paired.
    H = {(i, j): N for i in ids for j in ids[ids > i]}

    # by removing edges from H we can suppress those pairings.
    for exclude in exclude_pairs:
        del H[exclude]

    turn_pairs = []
    for _ in range(n_turns):
        if dropouts:  # who wants a pal?
            participating = np.random.randint(2, size=len(ids))
        else:
            participating = np.ones(len(ids))
        participating[0] = np.sum(participating[1:]) % 2  # placeholder gives even no.
        pairs = maximum_pairing(ids[participating != 0], H)
        # update history with new pairings
        H = {pair: 0 if pair in pairs else H[pair] + 1 for pair in H}
        turn_pairs.append(pairs)
    return turn_pairs


if __name__ == "__main__":
    # demo: make successive weekly matchings among club members.
    ids = ("alice", "bob", "carol", "diane", "edgar")
    # alice and bob are a couple, so don't pair them!
    exclude_pairs = [("alice", "bob")]
    np.random.seed(0)
    pairings = simulate_turns(ids, exclude_pairs, 10, dropouts=False)

    print("ids: {}".format(ids))
    print("exclude: {}".format(exclude_pairs))
    print("weekly pairings")
    for i, pairs in enumerate(pairings):
        print("week {}: {}".format(i, pairs))
