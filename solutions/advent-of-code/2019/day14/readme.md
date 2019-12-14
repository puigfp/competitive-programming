The key observation here is: a given chemical can only be produced by a single transformation.

We can to a BFS starting from the state `{FUEL: 1}`, transforming the state into more primitive elements and stopping when all the values of that state but the one for `ORE` are negative (stricly negative values are waste).
