import random

def monte_carlo_pi(n: int) -> float:

    def sample() -> bool:
        x = random.random()
        y = random.random()
        return x * x + y * y <= 1

    return 4 * sum(sample() for _ in range(n)) / n

pi = monte_carlo_pi(n := 1_000_000)

print(f"A Monte Carlo estimate of π from {n:,} rounds of simulation: {pi}")
