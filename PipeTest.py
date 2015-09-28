__author__ = 'Michael Kaldawi'

"""
Programmer: Michael Kaldawi
Class: CE 4348.501
Assignment: P01 (Program 1)

Program Description:
This program implements a prime number finder utilizing the sieve
of Eratosthenes.
"""

from multiprocessing import Process, Pipe
import numpy as np
import math


# a function to find primes between start and end indices
# the function returns a True/ False array indicating primes
def find_primes(conn, start, end):
    # create an array of boolean True values, size: 1 x 'end'
    array = np.ones(shape=end, dtype=np.bool)

    # for each value 'i' in the True array, starting at 2, until the
    # square root of the end value, mark multiples of 'i' as False.
    # Hence, for i = 2, the values marked False would be {4, 6, 8, ...}
    for i in range(2, int(math.sqrt(end))):
        if array[i]:
            j = i**2
            while j < end:
                array[j] = False
                j += i

    if conn is None:
        return {'start': start, 'array': array[start:]}
    # when requested by the parent process, send the information found
    conn.send({'start': start, 'array': array[start:]})
    conn.close()


# a function to print the prime numbers marked by True in a
# passed True/ False array
def print_primes(start, array):
    total = 0
    for i in array:
        if i:
            print(start, i)
            total += 1
        start += 1
#    print(total)

# a function to print the prime numbers marked by True in a
# passed True/ False array into a file
def write_primes(file, mode, start, array):
    f = open(file, mode)
    total = 0
    for i in array:
        if i:
            f.write(start.__str__() + " is a prime" + "\n")
            total += 1
        start += 1


if __name__ == '__main__':
    data = []
    children = []

    for i in find_primes(None, 2, 1000)['array']: data.append(i)

    for process in range(0, 10):
        parent_conn, child_conn = Pipe()
        if process == 0:
            children.append(Process(target=find_primes, args=(
                child_conn, 1001, 100000)))
        else:
            children.append(Process(target=find_primes, args=(
                child_conn, process*100001, (process+1)*100000)))

        children[process].start()
        for i in parent_conn.recv()['array']: data.append(i)
        children[process].join()

#    print_primes(2, data)
    write_primes(file='primes.txt', mode='w', start=2, array=data)