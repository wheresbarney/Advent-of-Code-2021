#!/usr/bin/env python3.8
# https://adventofcode.com/2021/day/8

from sys import argv

def q1(input):
    total = 0
    for l in input:
        (training, output) = [s.split(' ') for s in l.split(' | ')]
        # print(f'{training=} {output=}')
        total += sum([1 for u in output if len(u) in [2, 3, 4, 7]])
    return total


ref = {c: n for (n, c) in enumerate('abcdefg')} # segment positions ('correct')

def mapKey(pattern, key):
    return ''.join(sorted([key[ref[p]] for p in pattern]))

def q2(input):
    ret = 0

    unique_rules = {2: 'cf', 3: 'acf', 4: 'bcdf', 7: 'abcdefg'}
    group_always_on_rules = {5: 'adg', 6: 'abfg'}
    group_mixed_rules = {5: 'bef', 6: 'cde'}

    for l in input:
    # for l in [input[0]]:
        (training, output) = [s.split(' ') for s in l.split(' | ')]
        # print(f'{training=}')
        possibilities = [set('abcdefg') for i in range(7)] # outer array index: segment position; outer array contents: possible segments not invalidated

        for l, rule in unique_rules.items():
            positions = [ref[r] for r in rule]
            for test in [t for t in training if len(t) == l]:
                for pos in positions:
                    possibilities[pos] &= set(test)
                for pos in [pos for pos in range(7) if pos not in positions]:
                    possibilities[pos] -= set(test)

        for l, rule in group_always_on_rules.items():
            training_matches = [set(t) for t in training if len(t) == l]
            if len(training_matches) <= 1:
                continue
            all_ons = training_matches[0].intersection(*training_matches[1:])
            positions = [ref[r] for r in rule]
            for pos in positions:
                possibilities[pos] &= set(all_ons)
            for pos in [pos for pos in range(7) if pos not in positions]:
                possibilities[pos] -= set(all_ons)

        # print(f'{possibilities=}')
        assert len([pos for pos in possibilities if len(pos) == 1]) == len(ref)
        key = [pos.pop() for pos in possibilities]
        cypher = [
            mapKey('abcefg', key), # 0
            mapKey('cf', key),
            mapKey('acdeg', key),
            mapKey('acdfg', key),
            mapKey('bcdf', key),
            mapKey('abdfg', key),
            mapKey('abdefg', key),
            mapKey('acf', key),
            mapKey('abcdefg', key),
            mapKey('abcdfg', key), # 9
        ]
        # print(f'{key=} {cypher=}')

        result = ''
        for o in output:
            result += str(cypher.index(''.join(sorted(o))))
        ret += int(result)
    return ret

if len(argv) > 1:
    with open(argv[1], 'r') as f:
        print(q2([l.strip() for l in f]))
else:
    print(q2([l.strip() for l in '''be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce'''.splitlines()]))
