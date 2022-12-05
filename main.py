import time
import multiprocessing

from collections.abc import Callable
from multiprocessing import Pool


def task_pool_runner(func: Callable, task_list: list):
    """
    :param func: Callable
    The function that you want to run in parallel
    :param task_list: list
    The list of arguments that will be fed to the process pool
    :return: list
    The collected output of the func Callable object after it is executed with the arguments
    """

    cpu_count = multiprocessing.cpu_count()

    if not task_list:
        raise ValueError(f"Input task list may not be empty")

    task_count = len(task_list)

    # Determine how many processes we are running
    slice_count = cpu_count if task_count > cpu_count else task_count
    # See if the number of tasks divides evenly among processes
    remainder = task_count % cpu_count if slice_count != task_count else 0
    # Check to see how many tasks go in each slice
    slice_size = int((task_count - remainder) / slice_count)
    task_slices = []
    # Slice the task list into the requisite number of processes making evenly sized lists
    for i in range(0, slice_count):
        task_slices.append(task_list[slice_size * i: slice_size * (i + 1)])

    # Loop through slices and append 1 from the remaining tasks to each slice (round robin)
    # If the remainder is 0, this has no effect.
    leftover_nums = task_list[task_slices[-1][-1]-1: len(task_list)]
    for s, num in enumerate(leftover_nums):
        task_slices[s].append(num)

    # Create a pool context, giving it desired number of processes.
    with Pool(processes=slice_count) as pool:
        out_list = []
        # Start func execution in the pool with one slice per call
        procs = [pool.apply_async(func, i) for i in task_slices]
        for res_output in [res.get(timeout=10000) for res in procs]:
            out_list.extend(res_output)

    return out_list


def is_prime(*test_case: int):
    """
    :param test_case: *int
    An integer or list of integers that will be tested for primality
    :return: The items from the input test_case that are prime.
    """

    # Stretching the limits of acceptable list comprehension length and complexity for performance
    # Checks each number in the test case to see if it's divisible by every integer that's smaller than it is,
    # excluding 1
    # If it's not divisible by anything, it's added to output_list
    # This makes the CPU angry
    output_list = [
        i for i in test_case
        if all([
            (lambda mod_zero: True if i % j else False)(j)
            for j in range(2, i)
        ])
    ]

    return output_list


def main():
    input_list = [
        10, 100, 1000, 10000,
        20000, 40000, 60000, 80000,
        100000
    ]

    for num in input_list:
        t = time.time()
        input_list = list(range(2, num + 1))
        result = task_pool_runner(func=is_prime, task_list=input_list)
        t = time.time() - t
        print(f"There were {len(result)} primes found while testing from 0 to {num} ({round(t, 4)})")


if __name__ == "__main__":
    main()
