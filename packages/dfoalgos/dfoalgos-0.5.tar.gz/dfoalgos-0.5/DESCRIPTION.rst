Description
===========

This package contains derivative-free optimization algorithms. With the
exception of NMK, the included algorithms are even "rank-based" algorithms,
which do not use the actual objective values, but only their ranks. Thus, they
do not require objective values to be scalar and finite. A total order on the
objective values is sufficient. For example, an objective function could
return a list of values, which are then compared lexicographically. The
package can only handle bound constraints explicitly. For other constraints,
infeasible solutions should instead be penalized, e.g., evaluated with the
worst possible function value (possibly infinity).

The package is geared to work with optimization problems as defined in the
package optproblems. The whole package assumes minimization problems
throughout.


Documentation
=============

The documentation is located at
https://www.simonwessing.de/dfoalgos/doc/
