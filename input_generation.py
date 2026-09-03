"""Mock input generator for the doctor-hospital rank assignment problem.

preferences: (d doctors x h hospitals) matrix, entry = rank (1 = best)
capacities: (h,) vector, hospital capacities (sum >= d)

Hospitals aren't equally popular (normal distribution to determine popularity), 
and each doctor's ranking is sampled via Plackett-Luce (pick next-favorite 
without replacement, weighted by popularity).

Usage: 

preds, caps = generate_mock_dataset(n_doctors, n_hospitals)

We can modify the standard deviation of the hospital popularity distribution by 
changing sigma, and we canb set seeds to get reproducible data."""

import json
import numpy as np


def generate_mock_dataset(n_doctors, n_hospitals, sigma=1.0, seed=None):
    rng = np.random.default_rng(seed)
    
    # Random sample from a normal distribution for popularity
    popularity = np.exp(rng.normal(loc=0, scale=sigma, size=n_hospitals))

    # Empty ranking matrix
    preferences = np.zeros((n_doctors, n_hospitals), dtype=int)
    
    # Make random rankings based on popularity
    for i in range(n_doctors):
        remaining = list(range(n_hospitals))
        weights = popularity.copy()
        for rank in range(n_hospitals):
            p = weights[remaining] / weights[remaining].sum()
            choice = rng.choice(remaining, p=p)
            preferences[i, choice] = rank + 1
            remaining.remove(choice)

    # Make sure capacity is equal to the number of doctors
    capacities = rng.multinomial(n_doctors, np.ones(n_hospitals) / n_hospitals)

    return preferences, capacities


# Just for my own testing, not essential code here.
if __name__ == "__main__":
    prefs, caps = generate_mock_dataset(n_doctors=20, n_hospitals=5)
    print("preferences:", prefs.shape)
    print(prefs)
    print("capacities:", caps)
    
    # Check average rank to see how popular each hospital is
    avg_rank = prefs.mean(axis=0)
    print("average rank per hospital:", np.round(avg_rank, 2))