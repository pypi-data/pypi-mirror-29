Functional Subgraph
====================

A machine learning toolbox for the analysis of dynamic graphs.

*Functional Subgraph* implements non-negative matrix factorization to decompose
time-varying, dynamic graphs into a composite set of parts-based, additive
subgraphs.


Quick-Start
-----------
Non-Negative Matrix Factorization for dynamic graphs, such that:

    A ~= WH
    Constraints:
        A, W, H >= 0
        L2-Regularization on W
        L1-Sparsity on H

Implementation is based on :

    1. Jingu Kim, Yunlong He, and Haesun Park. Algorithms for Nonnegative
            Matrix and Tensor Factorizations: A Unified View Based on Block
            Coordinate Descent Framework.
            Journal of Global Optimization, 58(2), pp. 285-319, 2014.

    2. Jingu Kim and Haesun Park. Fast Nonnegative Matrix Factorization:
            An Active-set-like Method And Comparisons.
            SIAM Journal on Scientific Computing (SISC), 33(6),
            pp. 3261-3281, 2011.

Modified from: https://github.com/kimjingu/nonnegfac-python


