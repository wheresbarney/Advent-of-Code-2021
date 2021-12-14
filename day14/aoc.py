#!/usr/bin/env python3.8
# https://adventofcode.com/2021/day/14


from collections import Counter, defaultdict
from sys import argv


def parse(input):
    polymer = [c for c in input[0]]
    rules = {x[0]: x[1] for x in [x.split(' -> ') for x in input[2:]]}
    # print(f'{polymer=} {rules=}')
    return polymer, rules


def q1(input):
    polymer, rules = parse(input)
    for i in range(10):
        inserts = 0
        for x in range(len(polymer)):
            start = x + inserts
            pair = ''.join(polymer[start:start+2])
            if pair in rules:
                insert = rules[pair]
                # print(f'    insert {pair}->{insert} @ {start} ({x}+{inserts})')
                polymer.insert(start+1, insert)
                inserts += 1
        # print(f'{i}: {"".join(polymer)} ({len(polymer)})')
    c = Counter(polymer).most_common()
    return c[0][1] - c[-1][1]


def q2(input):
    polymer, rules = parse(input)
    pairs = defaultdict(int)
    for i in range(len(polymer)-1):
        pairs[''.join(polymer[i:i+2])] += 1

    for i in range(40):
        # print(f'  {i=} {pairs}')
        newpairs = defaultdict(int)
        for pair, count in pairs.items():
            if pair in rules:
                insert = rules[pair]
                newpairs[pair[0] + insert] += count
                newpairs[insert + pair[1]] += count
            else:
                newpairs[pair] += count
        pairs = newpairs

    element_counts = defaultdict(int)
    for pair, count in pairs.items():
        element_counts[pair[0]] += count
        element_counts[pair[1]] += count
    element_counts[polymer[0]] += 1 # start isn't double-counted, make it so
    element_counts[polymer[-1]] += 1 # end isn't double-counted, make it so
    ordered = sorted([int(n/2) for n in element_counts.values()]) # un-double-count all elements
    # print(f'{element_counts=}, {ordered=}')
    return ordered[-1] - ordered[0]


if len(argv) > 1:
    with open(argv[1], 'r') as f:
        print(q2([l.strip() for l in f]))
else:
    print(q2([l.strip() for l in '''
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
'''.splitlines()[1:]]))
