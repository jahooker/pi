import random
import numpy as np
from multiprocessing import Pool, cpu_count
from typing import Optional
from threading import Thread
from queue import Queue
import time


rand = random.random


def distribute(dividend: int, divisor: int) -> list[int]:
    q, r = divmod(dividend, divisor)
    chunks = [q] * divisor
    chunks[-1] += r
    assert sum(chunks) == dividend
    return chunks


def worker(n: int) -> int:
    k = 0
    for _ in range(n):
        x = rand()
        y = rand()
        k += x * x + y * y <= 1
    return k


def monte_carlo_pi_random(n: int) -> float:

    def sample() -> bool:
        x = rand()
        y = rand()
        return x * x + y * y <= 1

    k = sum(sample() for _ in range(n))
    return 4 * k / n


def monte_carlo_pi_numpy(n: int) -> float:
    xy = np.random.random((n, 2))
    k = ((xy * xy).sum(axis=1) <= 1).sum()
    return 4 * k / n


def thread_worker(n, q):
    rand = random.Random().random
    k = 0
    for _ in range(n):
        x = rand()
        y = rand()
        k += x * x + y * y <= 1
    q.put(k)


def monte_carlo_pi_threading(n: int):

    chunks = distribute(n, nthreads := 4)
    results = Queue()
    threads = [Thread(target=thread_worker, args=(chunk, results)) for chunk in chunks]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    k = sum(results.get() for _ in threads)
    return k * 4 / n


def monte_carlo_pi_parallel(n: int, processes: Optional[int] = None) -> float:

    if processes is None:
        processes = cpu_count()

    chunks = distribute(n, processes)

    with Pool(processes) as pool:
        k = sum(pool.map(worker, chunks, 1))

    return 4 * k / n


if __name__ == "__main__":
    t0 = time.time()
    pi = monte_carlo_pi_parallel(n := 1_000_000)
    print(f"A Monte Carlo estimate of π from {n:,} rounds of simulation: {pi}")
    t1 = time.time()
    print(f"Executed in {t1 - t0:.3f} seconds.")
