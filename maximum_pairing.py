"""maximum_pairing(ids, W)

Implementation of maximum weight euclidean matching using PuLP

In an undirected graph, find disjoint pairings for all nodes such that the total
edge weight is maximized.

This is formulated as an integer linear program and solved by
CBC (the default solver in PuLP).  Nice discussion of the ILP
formulation here: https://www.imsc.res.in/~meena/matching/lecture5.pdf

There are fancier ways to solve this in polynomial time
(cf Edmonds' "Blossom" algorithm https://en.wikipedia.org/wiki/Blossom_algorithm,
and an implementation: http://pub.ist.ac.at/~vnk/software.html#BLOSSOM5).

You'll need the PuLP module to run this:
`pip install pulp`
(And of course numpy.)

"""
import numpy as np
from pulp import *


def maximum_pairing(ids, W):
    """
    compute a pairing of ids, maximizing total edge weight

    Parameters
    ----------
    ids: list(ids)
        list of ids. may be strings, integers, anything that can be used
        as a dictionary key. Must be an even number of entries  (use a placeholder
        id if necessary)
    W: dict((id1, id2): weight)
        Edge weight. For each pair of ids that are allowed to match,
        the weight of this pairing (greater is better).
        Edges are undirected and should appear only once.
        (eg, you might assure that id1 < id2 for  all entries, though
        this is not required). Ok for W to include edges from ids not present in ids.

    Returns
    -------
    pairs: [(id1,id2), (id3,id4), ...]
        list of pairs that maximizes sum of edge weights

    """
    prob = LpProblem("maximum_pairing", LpMaximize)
    # decision variables: True if i and j are paired in the solution
    y = LpVariable.dicts(
        "pair", [(i, j) for i in ids for j in ids if (i, j) in W], cat="Binary",
    )
    # maximize: total edge weight
    prob += lpSum([W[(i, j)] * y[(i, j)] for i in ids for j in ids if (i, j) in W])
    # constraint: one match for each id
    for i in ids:
        prob += (
            lpSum(y[(i, j)] for j in ids if (i, j) in W)
            + lpSum(y[(j, i)] for j in ids if (j, i) in W)
            == 1
        )
    prob.solve()
    result = [
        (i, j) for i in ids for j in ids if (i, j) in y and y[(i, j)].varValue == 1
    ]
    return result
