# maximum-pairing
Implementation of maximum weight euclidean matching using PuLP

In an undirected graph, find disjoint pairings for all nodes such that the total
edge weight is maximized.

This is formulated as an integer linear program and solved by
CBC (the default solver in PuLP).  A nice discussion of the ILP
formulation is here: https://www.imsc.res.in/~meena/matching/lecture5.pdf

There are fancier ways to solve this in polynomial time
(cf Edmonds' "Blossom" algorithm https://en.wikipedia.org/wiki/Blossom_algorithm,
and an implementation: http://pub.ist.ac.at/~vnk/software.html#BLOSSOM5).

You'll need the PuLP module to run this:

`pip install pulp`

(And of course numpy.)


## demo.py
A demo using maximum_pairing() to match different pairs of club
members week after week, with accumulating history and
maximum diversity over time.

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
(change the dropouts parameter in the call to simulate_turns):
```
ids: ('alice', 'bob', 'carol', 'diane', 'edgar')
exclude: [('alice', 'bob')]
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
Week 6 looks odd, but is a consequence of alice and bob not being pairable.
