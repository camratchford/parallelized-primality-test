# parallelized-primality-test

## Overview

A script I wrote for fun while watching math videos.

It also contains a somehwat modular, but kind of janky implementation of [multiprocessing.Pool](https://github.com/camratchford/parallelized-primality-test/blob/master/main.py#L8-L50).


## Interesting note

With some minor modifications, you can use this script to benchmark the single-core vs. multicore performace of a processor.

Interesting results were found:

- M1 Mac CPUs perform much better with single-thread jobs (Compared to AMD Ryzen and Intel Xeon CPUs)
- AMD Ryzen CPUs perform much better multi-thread jobs (Compared to Apple M1 CPUs)
- Intel Xeon CPUs perform even better with multi-thread jobs (Compared to Apple M1 and AMD Ryzen CPUs)

