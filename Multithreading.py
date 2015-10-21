__author__ = 'Michael Kaldawi'

"""
Programmer: Michael Kaldawi
Class: CE 4348.501
Assignment: P01 (Program 1)

Program Description:
This program implements a prime number finder utilizing the sieve
of Eratosthenes and multi-threading.
"""

# Note: we are using numpy for our array processing to speed up
# runtime. numpy needs to be installed/ imported for this
# program to work.
import threading
import math
import cProfile

import numpy as np


# This function finds primes between 'start' and 'end' indices.
# The function returns a 1x(end-start) array of boolean values
# indicating primes as 'True'.
def find_primes(start, end):
    # create an array of boolean True values, size: 1 x 'end'
    array = np.ones(shape=end, dtype=np.bool)
    # For each value 'i' in the True array, starting at 2, until the
    # square root of the end value, mark multiples of 'i' as False.
    # Hence, for i = 2, the values marked False would be {4, 6, 8, ...}
    for i in range(2, int(math.sqrt(end)+1)):
        if array[i]:
            j = i**2
            while j < end:
                array[j] = False
                j += i
    # Return the array with a start value.
    return {'start': start, 'array': array[start:]}


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
# an additional function to start the thread.
class MyThread (threading.Thread):
    def __init__(self, start, end):
        threading.Thread.__init__(self)
        self.begin = start
        self.end = end
        self.data = None

    def run(self):
        self.data = find_primes(self.begin, self.end)

# This function calculates the prime numbers between
# 2 and 1,000, then starts 10 threads to complete
# the calculation of prime numbers between 1,001 and 1,000,000.


def main():
    # 'master_data' stores all boolean arrays. 'threads' is an
    # array of child threads.
    master_data = []
    thread_data = []
    threads = []

    # Find the primes between 2 and 1000.
    for i in find_primes(start=2, end=1000)['array']:
        master_data.append(i)

    # Make 10 threads.
    for thread in range(0, 10):
        if thread == 0:
            threads.append(MyThread(1001, 100000))
        else:
            threads.append(MyThread(thread*100001, (thread+1)*100000))

        # Start each child thread. Note, threads[-1] gets the last item in the list.
        threads[-1].start()

        # cProfile.runctx('start_child(threads[thread])',
        #                 globals(), locals())

    # Request each boolean array from the threads,
    # and append the arrays to 'master_data'.
    threads[9].join()
    for each in range(0, 10):
        for data_point in threads[each].data['array']:
            master_data.append(data_point)

    write_primes(file_name="primes.txt", mode="w", start=2, array=master_data)

    print("number of primes found: " + master_data.count(1).__str__())
    # cProfile.runctx('write_primes(file_name="primes.txt", '
    #                 'mode="w", start=2, array=master_data)',
    #                 globals(), locals())

# This is our 'main' function. The first lines of code
# are executed here.
#
# This function executes main().
# Only the parent process can run this function.
if __name__ == '__main__':
    main()