#!/usr/bin/env python3.8
# https://adventofcode.com/2021/day/10

from sys import argv

pairs = {b[0]: b[1] for b in ['()', '{}', '[]', '<>']}

def q1(input):
    scores = {')': 3, ']': 57, '}': 1197, '>': 25137}
    score = 0
    for line in input:
        openers = []
        for c in line:
            if c in '([{<':
                openers.append(c)
            else:
                closed = openers.pop()
                if pairs[closed] != c:
                    score += scores[c]
                    break
    return score

def q2(input):
    scores = {')': 1, ']': 2, '}': 3, '>': 4}
    scoreList = []
    for line in input:
        openers = []
        for c in line:
            # print(f'{line} {c=} {openers=}')
            if c in '([{<':
                openers.append(c)
            else:
                closed = openers.pop()
                if pairs[closed] != c:
                    openers.clear()
                    break

        if not openers:
            continue

        score = 0
        while openers:
            o = openers.pop()
            s = scores[pairs[o]]
            score *= 5
            score += s
        scoreList.append(score)

    scoreList.sort()
    return scoreList[int(len(scoreList) / 2)]

if len(argv) > 1:
    with open(argv[1], 'r') as f:
        print(q2([l.strip() for l in f]))
else:
    print(q2([l.strip() for l in '''[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]'''.splitlines()]))
