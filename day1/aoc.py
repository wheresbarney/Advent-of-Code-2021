#!/usr/bin/env python3.8

def q1(it):
    last = None
    count = 0
    for reading in it:
        if last and reading > last:
            count = count + 1
        last = reading
    return count

def q2(it):
    first, second, third = it[:3]
    last = first + second + third
    count = 0
    for reading in it[3:]:
        first = second
        second = third
        third = reading
        total = first + second + third
        if total > last:
            count = count + 1
        last = total
    return count

print(q1([199 ,200 ,208 ,210 ,200 ,207 ,240 ,269 ,260 ,263 ]))

# with open('input.txt', 'r') as f:
#     print(q2([int(t) for t in f]))
