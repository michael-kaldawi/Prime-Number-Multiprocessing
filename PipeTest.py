__author__ = 'Michael Kaldawi'

"""
Programmer: Michael Kaldawi
Class: CE 4348.501
Assignment: P01 (Program 1)

Program Description:
This program implements a prime number finder utilizing the sieve
of Eratosthenes, multiprocessing, and communication via pipes.
"""

# Note: we are using numpy for our array processing to speed up
# runtime. numpy needs to be installed/ imported for this
# program to work.
from multiprocessing import Process, Pipe
import math
import cProfile

import numpy as np


# This function finds primes between 'start' and 'end' indices.
# The function returns a 1x(end-start) array of boolean values
# indicating primes as 'True'.
def find_primes(start, end, conn=None):
    # create an array of boolean True values, size: 1 x 'end'
    array = np.ones(shape=end, dtype=np.bool)
    # For each value 'i' in the True array, starting at 2, until the
    # square root of the end value, mark multiples of 'i' as False.
    # Hence, for i = 2, the values marked False would be {4, 6, 8, ...}
    for i in range(2, int(math.sqrt(end))):
        if array[i]:
            j = i**2
            while j < end:
                array[j] = False
                j += i
    # If no connection is passed, return the array with a start value.
    if conn is None:
        return {'start': start, 'array': array[start:]}
    # If requested by the parent process, return the array with a start value.
    conn.send({'start': start, 'array': array[start:]})
    conn.close()


# This function prints the prime numbers marked by True in a
# passed True/ False array.
def print_primes(start, array):
    total = 0
    pos = start
    for i in array:
        if i:
            print(pos, i)
            total += 1
        pos += 1
#    print(total)


# a function to print the prime numbers marked by True in a
# passed True/ False array into a file
def write_primes(file_name, mode, start, array):
    f = open(file_name, mode)
    total = 0
    pos = start
    for i in array:
        if i:
            f.write(pos.__str__() + "\n")
            total += 1
        pos += 1
#    f.write("total: " + total.__str__())


# Due to the nature of the profiling package cProfile, we require
# an additional function to start the child process.
def start_child(process):
    process.start()


# This function calculates the prime numbers between
# 2 and 1,000, then starts 10 child processes to complete
# the calculation of prime numbers between 1,001 and 1,000,000.
# The parent process requests for the calculated primes from
# the child processes via Pipes. The child processes then
# return the calculated primes via the pipes.
def main():
    # 'data' stores all boolean arrays. 'children' is an
    # array of child processes.
    data = []
    children = []

    # Find the primes between 2 and 1000.
    for i in find_primes(start=2, end=1000)['array']:
        data.append(i)

    # Make 10 pipes and 10 corresponding child processes.
    for process in range(0, 10):
        parent_conn, child_conn = Pipe()
        if process == 0:
            children.append(Process(target=find_primes,
                                    args=(1001, 100000, child_conn)))
        else:
            children.append(Process(target=find_primes, args=(
                process*100001, (process+1)*100000, child_conn)))

        # Start each child process. Profile the run time of each process.
        cProfile.runctx('start_child(children[process])',
                        globals(), locals())

        # Request each boolean array from the child processes,
        # and append the arrays to 'data'.
        for i in parent_conn.recv()['array']:
            data.append(i)
        children[process].join()

    # write the prime numbers to 'primes.txt'
    cProfile.runctx('write_primes(file_name="primes.txt", '
                    'mode="w", start=2, array=data)',
                    globals(), locals())


# This is our 'main' function. The first line of code
# executed in this program is 'main()'
#
# This function executes main().
# Only the parent process can run this function.
if __name__ == '__main__':
    main()