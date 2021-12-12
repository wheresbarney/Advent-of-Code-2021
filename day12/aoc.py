#!/usr/bin/env python3.8
# https://adventofcode.com/2021/day/12

from collections import Counter, defaultdict
from sys import argv

def parse(input):
    map = defaultdict(list)
    small = set()
    for l in input:
        frm, to = l.split('-')
        map[frm].append(to)
        map[to].append(frm)
        if frm.islower(): small.add(frm)
        if to.islower(): small.add(to)
    # print(f'{map=} {small=}')
    return (map, small)


def find_paths(map, smalls, filter, start, allPaths, path=[]):
    path = path + [start]
    if start == 'end':
        # print(f'{" " * len(path)}Found solution {path}')
        allPaths.append(path)
        return
    for node in map[start]:
        # print(f'{" " * len(path)}{path} evaluating {node} ({map[start]})')
        if filter(node, path, smalls):
            continue
        find_paths(map, smalls, filter, node, allPaths, path)


def no_small_cave_revisiting_filter(node, path, smalls):
    return node in smalls and node in path


def q1(input):
    map, smalls = parse(input)
    paths = []
    find_paths(map, smalls, no_small_cave_revisiting_filter, 'start', paths)
    # [print(p) for p in paths]
    return len(paths)


def revisit_small_cave_exactly_once_filter(node, path, smalls):
    if node not in smalls or node not in path:
        return False
    if node == 'start':
        return True
    return 2 in Counter([p for p in path if p in smalls]).values()


def q2(input):
    map, smalls = parse(input)
    paths = []
    find_paths(map, smalls, revisit_small_cave_exactly_once_filter, 'start', paths)
    # [print(p) for p in paths]
    return len(paths)


if len(argv) > 1:
    with open(argv[1], 'r') as f:
        print(q2([l.strip() for l in f]))
else:
    # first, simplest example
    print(q2([l.strip() for l in '''start-A
start-b
A-c
A-b
b-d
A-end
b-end'''.splitlines()]))
    print(q2([l.strip() for l in '''fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW'''.splitlines()]))
