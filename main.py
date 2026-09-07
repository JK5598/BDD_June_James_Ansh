from input_generation import generate_mock_dataset
from interfernce_function_june import g
from Optimizor import minimum_cost
import numpy as np

if __name__ == "__main__":
    prefs, caps = generate_mock_dataset(n_doctors=5, n_hospitals=5)
    print("preferences:", prefs.shape)
    print(prefs)
    print("capacities:", caps)

    # Check average rank to see how popular each hospital is
    avg_rank = prefs.mean(axis=0)
    print("average rank per hospital:", np.round(avg_rank, 2))

    weighted_pref = g(prefs)

    assignments, total_cost = minimum_cost(weighted_pref, caps)

    for doctor, hospital in assignments.items():
        print(f"D{doctor + 1} -> H{hospital + 1}")

    print("Total assignment loss:", total_cost)