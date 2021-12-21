#!/usr/bin/env python3.9
# https://adventofcode.com/2021/day/20


from collections import Counter, defaultdict
from functools import lru_cache
from itertools import product
from sys import argv


class DeterministicDie:
    def __init__(self):
        self.rolls = 0

    def sum_of_three_rolls(self):
        self.rolls += 3
        # print(f'  {[(i % 100)+1 for i in range(self.rolls-3, self.rolls)]} ->{sum([(i % 100)+1 for i in range(self.rolls-3, self.rolls)])}')
        return sum([(i % 100)+1 for i in range(self.rolls-3, self.rolls)])


def q1(input, threshold, die):
    positions = [int(l.split(': ')[1]) for l in input]
    totals = [0, 0]
    moves = 0

    while totals[0] < threshold and totals[1] < threshold:
        index = (moves) % 2
        moves += 1
        move = die.sum_of_three_rolls()
        positions[index] = (positions[index] + move) % 10
        if positions[index] == 0:
            positions[index] = 10
        totals[index] += positions[index]
        # print(f'{moves}: player{index+1} {move=} position={positions[index]} score={totals[index]}')

    # print(f'{moves=} {positions=} {totals=}')
    loser = sorted(totals)[0]
    return loser * moves * 3

def q2(input):
    starting_positions = [int(l.split(': ')[1]) for l in input]

    outcomes = Counter([((u1d1 + u1d2 + u1d3), (u2d1 + u2d2 + u2d3))
        for u1d1 in range(1,4)
        for u1d2 in range(1,4)
        for u1d3 in range(1,4)
        for u2d1 in range(1,4)
        for u2d2 in range(1,4)
        for u2d3 in range(1,4)])

    games = defaultdict(int)
    games[(starting_positions[0], starting_positions[1], 0, 0)] = 1
    wongames = [0, 0]

    loop = 0
    while True:
        newgames = defaultdict(int)
        oldgames = defaultdict(int)
        for game in [g for g,c in games.items() if c>0]:
            for outcome, freq in outcomes.items():
                pos1 = (game[0] + outcome[0]) % 10
                if pos1 == 0:
                    pos1 = 10
                pos2 = (game[1] + outcome[1]) % 10
                if pos2 == 0:
                    pos2 = 10
                newgame = (pos1, pos2, game[2] + pos1, game[3] + pos2)

                if newgame[2] >= 21:
                    wongames[0] += freq
                elif newgame[3] >= 21:
                    wongames[1] += freq
                else:
                    newgames[newgame] += freq
            oldgames[game] += 1

        # print(f'  {loop} {newgames=} {oldgames=}')
        for newgame, count in newgames.items():
            games[newgame] += count
        for oldgame, count in oldgames.items():
            games[oldgame] -= count
        loop += 1

        if loop % 50 == 0:
            dead = [g for g,c in games.items() if c == 0]
            lo = [c for g,c in games.items() if c > 0 and g[2] < 6 and g[3] < 6]
            mid = [c for g,c in games.items() if c > 0 and g[2] >= 6 and g[3] >= 6 and g[2] < 11 and g[3] < 11]
            hi = [c for g,c in games.items() if c > 0 and g[2] >= 11 and g[3] >= 11 and g[2] < 16 and g[3] < 16]
            vhi = [c for g,c in games.items() if c > 0 and g[2] >= 16 and g[3] >= 16]
            print(f'{loop}: lo={len(lo)} mid={len(mid)} hi={len(hi)} vhi={len(vhi)} won:{wongames} (dead={len(dead)})')

        if not oldgames:
            # finished!
            break

    return wongames

DIRAC_DIE = [1, 2, 3]
ROLLS_AND_FREQS = Counter([d1 + d2 + d3 for d1, d2, d3 in product(DIRAC_DIE, DIRAC_DIE, DIRAC_DIE)])

 # with a little help from Reddit!
@lru_cache(maxsize=None)
def play2(my_pos, my_score, other_pos, other_score):
    if my_score >= 21:
        return 1, 0

    if other_score >= 21:
        return 0, 1

    my_wins = other_wins = 0

    for roll, freq in ROLLS_AND_FREQS.items():
        # Play one turn calculating the new score with the current roll:
        new_pos   = 1 + (my_pos + roll - 1) % 10
        new_score = my_score + new_pos

        # Let the other player play, swapping the arguments:
        ow, mw = play2(other_pos, other_score, new_pos, new_score)

        # Update total wins of each player:
        my_wins    += mw * freq
        other_wins += ow * freq

    return my_wins, other_wins

def q2_recursive(input):
    starting_positions = [int(l.split(': ')[1]) for l in input]
    return max(play2(starting_positions[0], 0, starting_positions[1], 0))

print(q1([l.strip() for l in '''
Player 1 starting position: 4
Player 2 starting position: 8
'''.splitlines()[1:]], 1000, DeterministicDie()))

print(q1([l.strip() for l in '''
Player 1 starting position: 7
Player 2 starting position: 1
'''.splitlines()[1:]], 1000, DeterministicDie()))

print(q2_recursive([l.strip() for l in '''
Player 1 starting position: 4
Player 2 starting position: 8
'''.splitlines()[1:]]))

print(q2_recursive([l.strip() for l in '''
Player 1 starting position: 7
Player 2 starting position: 1
'''.splitlines()[1:]]))
