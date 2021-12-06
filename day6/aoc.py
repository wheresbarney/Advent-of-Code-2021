#!/usr/bin/env python3.8
# https://adventofcode.com/2021/day/6

from sys import argv

def q1(seedAges):
    seedAges = [int(s) for s in seedAges[0].split(',')]
    ages = [0] * 9
    for seed in seedAges:
        ages[seed] += 1

    for i in range(1, 256 + 1):
        zeros = ages[0]
        ages[0] = 0
        for n in range(1, 9):
            if ages[n] > 0:
                ages[n-1] += ages[n] # circular buffer more efficient
                ages[n] = 0
        ages[8] = zeros # new ones
        ages[6] += zeros # go to the back of the queue
        # print(f'{i}: {sum(ages)} ({ages=})')

    return sum(ages)

if len(argv) > 1:
    with open(argv[1], 'r') as f:
        print(q1([l.strip() for l in f]))
else:
    print(q1([l.strip() for l in '''3,4,3,1,2'''.splitlines()]))
