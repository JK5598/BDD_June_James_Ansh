"""
Interference function g() for BDD_June_James_Ansh.

Pipeline:  Ansh's generator -> M_R -> g() -> cost matrix -> James's min-cost flow.

Per the proposal, g maps the ranking matrix M_R to a fixed n x m matrix of
assignment costs. Implemented here as the identity function, so the costs are
the rankings themselves: [g(M_R)]_ij = R_ij.

Usage:
    from input_generation import generate_mock_dataset
    from interference_function_june import g, assignment_loss

    M_R, capacities = generate_mock_dataset(n_doctors, n_hospitals)
    costs = g(M_R)                       # (n, m) int, cost of doctor i at hospital j
    loss = assignment_loss(costs, M_X)   # M_X = (n, m) 0/1 decision matrix
"""

import numpy as np


def g(ranking_matrix):
    """
    M_R -> g(M_R).  Identity form: cost of doctor i at hospital j is R_ij.

    ranking_matrix : (n, m) int array, entry = rank, 1 = most preferred.
    returns        : (n, m) int array of assignment costs.
    """
    M_R = np.asarray(ranking_matrix)
    _validate_rankings(M_R)
    return M_R.copy() # Do not interrupt with Ansh's generator output.


def _validate_rankings(M_R):
    """Assumption: complete rankings, each rank used once."""
    if M_R.ndim != 2:
        raise ValueError(f"M_R must be 2D, got {M_R.ndim}D.")

    n, m = M_R.shape
    if n == 0 or m == 0:
        raise ValueError(f"M_R is empty (shape {M_R.shape}).")
    if not np.issubdtype(M_R.dtype, np.integer):
        raise ValueError(f"Ranks must be integers, got dtype {M_R.dtype}.")

    expected = np.arange(1, m + 1)
    bad = np.nonzero((np.sort(M_R, axis=1) != expected).any(axis=1))[0]
    if bad.size:
        i = int(bad[0])
        raise ValueError(
            f"Doctor {i} has an incomplete ranking: expected each of "
            f"{[int(r) for r in expected]} once, got {[int(r) for r in M_R[i]]}."
            + (f" ({bad.size} doctors affected.)" if bad.size > 1 else "")
        )


def assignment_loss(costs, M_X):
    """
    The objective:  sum( g(M_R) (*) M_X ),  elementwise product summed.

    costs : (n, m) output of g().
    M_X   : (n, m) 0/1 decision matrix, X_ij = 1 if doctor i goes to hospital j.
    """
    costs = np.asarray(costs)
    M_X = np.asarray(M_X)
    if M_X.shape != costs.shape:
        raise ValueError(f"M_X shape {M_X.shape} != cost shape {costs.shape}.")
    if not np.isin(M_X, (0, 1)).all():
        raise ValueError("M_X must contain only 0 and 1.")
    # Each doctor exactly one hospital.

    row_sums = M_X.sum(axis=1)
    if not (row_sums == 1).all():
        raise ValueError(
            f"Every doctor needs exactly one hospital; "
            f"doctors {list(np.nonzero(row_sums != 1)[0])} do not."
        )
    return int((costs * M_X).sum())


if __name__ == "__main__":
    from input_generation import generate_mock_dataset

    M_R, capacities = generate_mock_dataset(6, 3, sigma=1.0, seed=1)
    costs = g(M_R)

    print("M_R:\n", M_R)
    print("capacities:", capacities)
    print("g(M_R):\n", costs)
    print("identity, so g(M_R) == M_R:", np.array_equal(costs, M_R))

    # Every doctor to their top choice, ignoring capacity, as a loss check.
    M_X = (M_R == 1).astype(int)
    print("loss if everyone got their 1st choice:", assignment_loss(costs, M_X),
          "(= n, since each first choice costs 1)")