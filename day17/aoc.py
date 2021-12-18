#!/usr/bin/env python3.8
# https://adventofcode.com/2021/day/17


from re import search
from sys import argv

ON_TARGET = 'on_target'
OVERSHOOT = 'overshoot'
UNDERSHOOT = 'undershoot'
PASSTHROUGH = 'passthrough'


def parse(input):
    m = search('x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)', input)
    m = [int(n) for n in m.groups()]
    return ((m[0], m[1]), (m[2], m[3]))


def simulate(x_vel, y_vel, target):
    orig = (x_vel, y_vel)
    max_y = x = y = 0
    i = 0
    passthrough = False
    while True:
        prev = (x, y)
        x = x + x_vel
        y = y + y_vel
        max_y = max(max_y, y)
        if x_vel > 0:
            x_vel -= 1
        elif x_vel < 0:
            x_vel += 1
        y_vel -= 1
        i += 1

        # print(f'  {i}:{(x, y)}')
        if x >= target[0][0] and x <= target[0][1]:
            passthrough = True
            if y <= target[1][1] and y >= target[1][0]:
                # print(f'{orig} -> {ON_TARGET}: {(x, y)} == ({target[0][0]}..{target[0][1]}, {target[1][0]}..{target[1][1]})')
                return (x, y, ON_TARGET, max_y)

        if y <= target[1][0]:
            if x > target[0][1]:
                type = OVERSHOOT
            else:
                if passthrough:
                    type = PASSTHROUGH
                else:
                    type = UNDERSHOOT
            # print(f'{orig} -> {type}: {(x, y)} != ({target[0][0]}..{target[0][1]}, {target[1][0]}..{target[1][1]})')
            return (x, y, type, max_y)


def q1(input):
    target = parse(input)

    x_vel = 1
    y_vel = 0
    x_delta = y_delta = 0

    # adjust x_vel first
    i = 0
    # while i<50:
    while True:
        x_vel += x_delta
        y_vel += y_delta

        result = simulate(x_vel, y_vel, target)
        i += 1

        if result[2] in [PASSTHROUGH, ON_TARGET]:
            break

        if result[2] == OVERSHOOT:
            x_delta = min(-1, int((result[0] - target[0][1]) / 2))
        else:
            x_delta = max(1, int((target[0][0] - result[0]) / 2))

        # print(f'  {(x_vel, y_vel)} -> {result} x+={x_delta}, y+={y_delta}')

    # now adjust y_vel
    x_delta = 0
    y_delta = 1
    been_on_target = False
    i = 0
    while i<50:
    # while True:

        result = simulate(x_vel, y_vel, target)
        i += 1

        if result[2] == PASSTHROUGH and been_on_target:
            return (x_vel, y_vel)

        if result[2] == ON_TARGET:
            been_on_target = True

        if result[2] == OVERSHOOT:
            x_delta = -1

        y_delta = 1
        x_vel += x_delta
        y_vel += y_delta


def q1_brute_force(input):
    target = parse(input)
    max_height = 0
    best_coords = ()
    for x in range(target[0][0]):
        for y in range(1000):
            res = simulate(x, y, target)
            if res[2] == ON_TARGET and res[3] > max_height:
                max_height = res[3]
                best_coords = (x, y)
    return (best_coords, max_height)


def q2(input):
    target = parse(input)
    ret = []

    valid_x = [x for x in reversed(range(target[0][1] + 1)) if int((x+1) * x/2) * x >= target[0][0]]
    for x in valid_x:
        for y in range(target[1][0], 105):
            if simulate(x, y, target)[2] == ON_TARGET:
                ret.append((x, y))
    return len(ret)

# print(q1_brute_force('target area: x=20..30, y=-10..-5'))
# print(q1_brute_force('target area: x=206..250, y=-105..-57'))

print(q2('target area: x=20..30, y=-10..-5'))
print(q2('target area: x=206..250, y=-105..-57'))
