
dfoalgos has been tested with Python 2.7 and 3.6. The recommended version is
Python 3.x, because compatibility is reached by avoiding usage of xrange. So,
the code has a higher memory consumption under Python 2.

Everything in this package is pure Python. For a description of the contents
see DESCRIPTION.rst.


Changes
=======

0.5
---
* Added a factory method for creating Nelder-Mead instances with adaptive
  (a.k.a. dimension-dependent) parameters. The parameters are chosen
  according to the formulas of Gao and Han.
* Added a simplex construction method proposed by Lixing Han.

0.4
---
* Fixed a bug in the NMKSimplexSearch where the direction vectors were
  unnecessarily transposed in the simplex gradient calculation. This was caused
  by Python being row-major, while Matlab uses column-major layout.

0.3
---
* Fixed a bug in the NMKSimplexSearch where alpha was recomputed in every
  iteration. Two options are now available: 1) only initial calculation,
  2) recalculation after every reorientation (see argument recalc_alpha).

0.2
---
* Added simplex construction methods originating from L.E. Pfeffer, J.C.
  Nash, and Spendley/Varadhan.
* Added Nelder-Mead variant with sufficient decrease condition and
  reorientation of the simplex by Kelley.
* Added a minimize function that mimics the SciPy interface to all optimization
  algorithms.

0.1
---
* Initial version containing two simplex searches (Spendley and Nelder-Mead)
  and a pattern search algorithm.
