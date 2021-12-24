#!/usr/bin/env python3.8
# https://adventofcode.com/2021/day/23


from sys import argv
from collections import defaultdict
from math import inf
import heapq


#   #############
#   #01234567890#
#   ###1#2#3#4###
#     #5#6#7#8#
#     #########

DESTINATIONS = {'A': [11, 15], 'B': [12, 16], 'C': [13, 17], 'D': [14, 18]}
DESTINATIONS_Q2 = {'A': [11, 15, 19, 23], 'B': [12, 16, 20, 24], 'C': [13, 17, 21, 25], 'D': [14, 18, 22, 26]}
HALL_SPOTS = {0, 1, 3, 5, 7, 9, 10}
HALL_ENTRY = {11: 2, 12: 4, 13: 6, 14: 8}
COSTS = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}

def parse(input):
    map = ['.'] * 11
    for line in input[2:4]:
        map += line.replace('#', '').replace(' ', '')
    return map

def viable_moves_dijkstra(state):
    viable_moves = set()
    for pos, type in [(i, state[i]) for i in range(len(state)) if state[i] in 'ABCD']:
        dest = DESTINATIONS[type]
        if state[dest[1]] not in 'ABCD' or pos == dest[1]:
            home = dest[1]
        elif state[dest[1]] == type:
            home = dest[0]
        else:
            home = None

        if pos == home:
            continue

        candidates = set()

        if home:
            candidates.add(home)

        if pos > 10:
            candidates |= HALL_SPOTS

        candidates.discard(pos)

        for destination in candidates:

            path = []
            current = pos

            # back of the room? move to front of room first
            if current > 14:
                current = current - 4
                path.append(current)

            # front of the room? move to hallway
            if current > 10 and destination != current + 4:
                current = HALL_ENTRY[current]
                path.append(current)

            # move along the hall
            if destination > 10:
                if destination > 14:
                    first_room_pos = destination - 4
                else:
                    first_room_pos = destination
                hall_dest = HALL_ENTRY[first_room_pos]
            else:
                hall_dest = destination

            if hall_dest < current:
                path += range(current-1, hall_dest-1, -1)
            else:
                path += range(current+1, hall_dest+1, 1)
            current = path[-1]

            # move into a room if that's where you're going
            if current < destination:
                current = DESTINATIONS[type][0]
                path.append(current)

            # move to back of room if that's where you're going
            if current != destination:
                current += 4
                path.append(current)

            # now check journey is unobstructed
            obstructed = False
            for p in path:
                if state[p] in 'ABCD':
                    obstructed = True
                    break
            if not obstructed:
                new_state = list(state)
                new_state[pos] = '.'
                new_state[destination] = type
                viable_moves.add((''.join(new_state), len(path) * COSTS[type]))

    return viable_moves

# unit tests
def test_viable_moves_dijkstra(state, test):
    moves = viable_moves_dijkstra(state)
    assert test(moves), moves

test_viable_moves_dijkstra('A.+.+.+.+..........', lambda m: m == {('..+.+.+.+......A...', 4)})
test_viable_moves_dijkstra('A.+.+.+.+...BCDABCD', lambda m: m == {('..+.+.+.+..ABCDABCD', 3)})
test_viable_moves_dijkstra('..+.+.+.+..BACDABCD', lambda m: ('..+B+.+.+...ACDABCD', 20) in m)

#   #############
#   #01234567890#
#   ###1#2#3#4###
#     #5#6#7#8#
#     #9#0#1#2#
#     #3#4#5#6#
#     #########

def viable_moves_dijkstra_q2(state):
    viable_moves = set()
    for pos, type in [(i, state[i]) for i in range(len(state)) if state[i] in 'ABCD']:
        for dest in reversed(sorted(DESTINATIONS_Q2[type])):
            if pos == dest:
                home = dest
                break
            if state[dest] not in 'ABCD':
                home = dest
                break
            if state[dest] != type:
                home = None
                break

        # print(f' {type}@{pos} {home=}')
        if pos == home:
            continue

        candidates = set()

        if home:
            candidates.add(home)

        if pos > 10:
            candidates |= HALL_SPOTS

        candidates.discard(pos)

        for destination in candidates:

            path = []
            current = pos

            # back of the room? move to front of room first
            while current > 14:
                current = current - 4
                path.append(current)

            # front of the room? move to hallway
            if current > 10 and destination != current + 4:
                current = HALL_ENTRY[current]
                path.append(current)

            # move along the hall
            if destination > 10:
                first_room_pos = destination
                while first_room_pos > 14:
                    first_room_pos -= 4
                hall_dest = HALL_ENTRY[first_room_pos]
            else:
                hall_dest = destination

            if hall_dest < current:
                path += range(current-1, hall_dest-1, -1)
            else:
                path += range(current+1, hall_dest+1, 1)
            current = path[-1]

            # move into a room if that's where you're going
            if current < destination:
                current = DESTINATIONS_Q2[type][0]
                path.append(current)

            # move to back of room if that's where you're going
            while current != destination:
                current += 4
                path.append(current)

            # now check journey is unobstructed
            obstructed = False
            for p in path:
                if state[p] in 'ABCD':
                    obstructed = True
                    break
            if not obstructed:
                new_state = list(state)
                new_state[pos] = '.'
                new_state[destination] = type
                viable_moves.add((''.join(new_state), len(path) * COSTS[type]))

    return viable_moves

def test_viable_moves_dijkstra_q2(state, test):
    moves = viable_moves_dijkstra_q2(state)
    assert test(moves), moves

test_viable_moves_dijkstra_q2('A.+.+.+.+..................', lambda m: m == {('..+.+.+.+..............A...', 6)})
test_viable_moves_dijkstra_q2('A.+.+.+.+...BCDABCDABCDABCD', lambda m: m == {('..+.+.+.+..ABCDABCDABCDABCD', 3)})
test_viable_moves_dijkstra_q2('..+.+.+.+..BACDABCDABCDABCD', lambda m: ('..+B+.+.+...ACDABCDABCDABCD', 20) in m)

def solve_dijkstra(initial, viable_moves):
    costs = defaultdict(lambda: inf, {initial: 0})
    visited = defaultdict(lambda: False)
    heapq.heappush(Q := [], (0, initial))
    while Q:
        state = heapq.heappop(Q)[1]
        visited[state] = True
        next_moves = viable_moves(state)
        # print(f'{state} --> {next_moves}')
        for (new_state, cost) in next_moves:
            if not visited[new_state]:
                new_cost = costs[state] + cost
                if new_cost < costs[new_state]:
                    costs[new_state] = new_cost
                    heapq.heappush(Q, (new_cost, new_state))
    return costs

def q1(input):
    initial = parse(input)
    for lobby in [2, 4, 6, 8]:
        initial[lobby] = '+'
    initial = ''.join(initial)
    print(f'{initial=}')

    costs = solve_dijkstra(initial, viable_moves_dijkstra)

    return costs['..+.+.+.+..ABCDABCD']

def q2(input):
    initial = parse(input)
    for lobby in [2, 4, 6, 8]:
        initial[lobby] = '+'
    initial = initial[:15] + 'DCBA'.split() + 'DBAC'.split() + initial[15:]
    initial = ''.join(initial)
    print(f'{initial=}')

    costs = solve_dijkstra(initial, viable_moves_dijkstra_q2)

    return costs['..+.+.+.+..ABCDABCDABCDABCD']

if len(argv) > 1:
    with open(argv[1], 'r') as f:
        print(q2([l.strip() for l in f]))
else:
    print(q2([l.strip() for l in '''
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
'''.splitlines()[1:]]))
