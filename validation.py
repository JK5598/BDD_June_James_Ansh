"""Validation helpers for comparing assignment methods."""

import numpy as np


def random_assignment(capacities, n_doctors, seed=None):
    """Return a capacity-feasible random assignment."""
    rng = np.random.default_rng(seed)
    hospital_slots = np.repeat(np.arange(len(capacities)), capacities)
    if len(hospital_slots) < n_doctors:
        raise ValueError("Insufficient hospital capacity to assign all doctors.")

    rng.shuffle(hospital_slots)
    return {doctor: int(hospital_slots[doctor]) for doctor in range(n_doctors)}


def greedy_bucket_assignment(preferences, capacities):
    """
    Return a capacity-feasible greedy assignment.

    The algorithm fills rank bucket 1 first, then bucket 2, and so on. Within
    each bucket, hospitals take currently unassigned doctors who gave that
    hospital the current rank until capacity is full.
    """
    preferences = np.asarray(preferences)
    remaining_capacity = np.asarray(capacities, dtype=int).copy()
    n_doctors, n_hospitals = preferences.shape
    assignments = {}

    for rank in range(1, n_hospitals + 1):
        for hospital in range(n_hospitals):
            if remaining_capacity[hospital] == 0:
                continue

            candidates = [
                doctor
                for doctor in range(n_doctors)
                if doctor not in assignments and preferences[doctor, hospital] == rank
            ]

            for doctor in candidates[: remaining_capacity[hospital]]:
                assignments[doctor] = hospital
                remaining_capacity[hospital] -= 1
                if remaining_capacity[hospital] == 0:
                    break

    if len(assignments) != n_doctors:
        raise RuntimeError("Greedy baseline did not assign every doctor.")

    return assignments


def summarize_assignment(name, assignments, preferences):
    """Summarize total cost, average rank, and per-rank assignment counts."""
    preferences = np.asarray(preferences)
    ranks = np.array(
        [
            preferences[doctor, hospital]
            for doctor, hospital in sorted(assignments.items())
        ]
    )
    counts = np.bincount(ranks, minlength=preferences.shape[1] + 1)[1:]
    return {
        "method": name,
        "total_cost": int(ranks.sum()),
        "avg_rank": float(ranks.mean()),
        "rank_counts": counts,
    }


def compare_assignment_methods(
    preferences,
    capacities,
    method_assignments,
    seed=None,
    n_random_trials=1000,
):
    """Compare one assignment method against random and greedy baselines."""
    preferences = np.asarray(preferences)
    n_doctors = preferences.shape[0]

    random_summaries = [
        summarize_assignment(
            "Random assignment",
            random_assignment(capacities, n_doctors, seed=None if seed is None else seed + trial),
            preferences,
        )
        for trial in range(n_random_trials)
    ]

    random_total_costs = np.array(
        [summary["total_cost"] for summary in random_summaries]
    )
    random_avg_ranks = np.array([summary["avg_rank"] for summary in random_summaries])
    random_rank_counts = np.array(
        [summary["rank_counts"] for summary in random_summaries]
    )

    return {
        "method": summarize_assignment(
            "Our method (min-cost flow)",
            method_assignments,
            preferences,
        ),
        "greedy": summarize_assignment(
            "Greedy bucket",
            greedy_bucket_assignment(preferences, capacities),
            preferences,
        ),
        "random_mean": {
            "method": "Random assignment mean",
            "total_cost": float(random_total_costs.mean()),
            "avg_rank": float(random_avg_ranks.mean()),
            "rank_counts": random_rank_counts.mean(axis=0),
        },
        "random_best": {
            "method": "Random assignment best",
            "total_cost": int(random_total_costs.min()),
            "avg_rank": float(random_avg_ranks.min()),
        },
        "random_trials": n_random_trials,
        "random_total_cost_std": float(random_total_costs.std(ddof=1)),
    }


def print_comparison_summary(comparison):
    """Print a compact text table for assignment comparison results."""
    method_summary = comparison["method"]
    greedy_summary = comparison["greedy"]
    random_mean = comparison["random_mean"]
    random_best = comparison["random_best"]

    print("Comparison summary")
    print("-" * 88)
    print(
        f"{'Method':<28} {'Total cost':>11} {'Avg rank':>10}  "
        "Rank count distribution (#1, #2, ...)"
    )
    print("-" * 88)
    print(
        f"{method_summary['method']:<28} "
        f"{method_summary['total_cost']:>11} "
        f"{method_summary['avg_rank']:>10.2f}  "
        f"{method_summary['rank_counts'].tolist()}"
    )
    print(
        f"{greedy_summary['method']:<28} "
        f"{greedy_summary['total_cost']:>11} "
        f"{greedy_summary['avg_rank']:>10.2f}  "
        f"{greedy_summary['rank_counts'].tolist()}"
    )
    print(
        f"{random_mean['method']:<28} "
        f"{random_mean['total_cost']:>11.2f} "
        f"{random_mean['avg_rank']:>10.2f}  "
        f"{np.round(random_mean['rank_counts'], 2).tolist()}"
    )
    print(
        f"{random_best['method']:<28} "
        f"{random_best['total_cost']:>11} "
        f"{random_best['avg_rank']:>10.2f}  "
        "best total cost across random trials"
    )
    print()
    print(f"Random trials: {comparison['random_trials']}")
    print(f"Random total cost std: {comparison['random_total_cost_std']:.2f}")
