#!/usr/bin/env python3.8
# https://adventofcode.com/2021/day/3

from sys import argv

def bitCount(readings):
    ones = [0 for x in range(len(readings[0]))]
    for reading in readings:
        for i in range(len(reading)):
            if reading[i] == '1':
                ones[i] += 1
    return ones

def q1(readings):
    gammaStr = ''
    epsilonStr = ''
    for count in bitCount(readings):
        if count > len(readings) / 2:
            nextGammaBit = '1'
            nextEpsilonBit = '0'
        else:
            nextGammaBit = '0'
            nextEpsilonBit = '1'
        gammaStr = gammaStr + nextGammaBit
        epsilonStr = epsilonStr + nextEpsilonBit
    return int(gammaStr, 2) * int(epsilonStr, 2)

def q2(readings):
    oxygenCandidates = readings
    filterBit = 0
    while len(oxygenCandidates) > 1:
        ones = bitCount(oxygenCandidates)
        if ones[filterBit] >= len(oxygenCandidates) / 2:
            filter = '1'
        else:
            filter = '0'
        oxygenCandidates = [c for c in oxygenCandidates if c[filterBit] == filter]
        filterBit += 1

    scrubberCandidates = readings
    filterBit = 0
    while len(scrubberCandidates) > 1:
        ones = bitCount(scrubberCandidates)
        if ones[filterBit] < len(scrubberCandidates) / 2:
            filter = '1'
        else:
            filter = '0'
        scrubberCandidates = [c for c in scrubberCandidates if c[filterBit] == filter]
        # print(f'filtered {scrubberCandidates} down to {filtered} on bit {filterBit} = {filter}')
        filterBit += 1

    print(f'{oxygenCandidates=} {scrubberCandidates=}')
    return int(oxygenCandidates[0], 2) * int(scrubberCandidates[0], 2)

if len(argv) > 1:
    with open(argv[1], 'r') as f:
        print(q2([l.strip() for l in f]))
else:
    print(q2([l.strip() for l in '''00100
        11110
        10110
        10111
        10101
        01111
        00111
        11100
        10000
        11001
        00010
        01010'''.splitlines()]))
