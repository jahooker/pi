import random
import numpy as np


def monte_carlo_pi_random(n: int) -> float:

    def sample() -> bool:
        x = random.random()
        y = random.random()
        return x * x + y * y <= 1

    k = sum(sample() for _ in range(n))
    return 4 * k / n


def monte_carlo_pi_numpy(n: int) -> float:
    xy = np.random.random((n, 2))
    k = ((xy * xy).sum(axis=1) <= 1).sum()
    return 4 * k / n


pi = monte_carlo_pi_numpy(n := 1_000_000)

print(f"A Monte Carlo estimate of π from {n:,} rounds of simulation: {pi}")
