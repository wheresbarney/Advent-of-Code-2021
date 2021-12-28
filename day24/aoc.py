#!/usr/bin/env python3.8
# https://adventofcode.com/2021/day/24


from random import randrange
from sys import argv


# the registers
REGISTERS = [0, 0, 0, 0]
def read(reg):
    index = ord(reg) - 119
    return REGISTERS[index]

def write(reg, val):
    index = ord(reg) - 119
    REGISTERS[index] = val

# prog_input: array of integers
def evaluate(prog_input, prog):
    # convert prog input into stack
    prog_input = list(reversed(prog_input))

    for reg in 'wxyz':
        write(reg, 0)

    for tokens in [line.split(' ') for line in prog]:
        instr = tokens[0]
        register = tokens[1]

        # print(f'evaluating {" ".join(tokens)} {REGISTERS}')
        if instr == 'inp':
            write(register, prog_input.pop())
        else:
            arg = tokens[2]
            if arg in 'wxyz':
                arg = read(arg)
            else:
                arg = int(arg)

            if instr == 'add':
                write(register, read(register) + arg)
            elif instr == 'mul':
                write(register, read(register) * arg)
            elif instr == 'div':
                write(register, int(read(register) / arg))
            elif instr == 'mod':
                write(register, read(register) % arg)
            elif instr == 'eql':
                write(register, 1 if read(register) == arg else 0)
        # print(f'{REGISTERS}')
    return REGISTERS

assert evaluate([7], '''
inp x
mul x -1
'''.splitlines()[1:]) == [0, -7, 0, 0]

assert evaluate([2, 6], '''
inp z
inp x
mul z 3
eql z x
'''.splitlines()[1:])[3] == 1

assert evaluate([2, 7], '''
inp z
inp x
mul z 3
eql z x
'''.splitlines()[1:])[3] == 0

assert evaluate([15], '''
inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2
'''.splitlines()[1:]) == [1, 1, 1, 1]


PROG = '''
inp w
mul x 0
add x z
mod x 26
div z 1
add x 12
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 9
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 12
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 4
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 12
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 2
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -9
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 5
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -9
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 1
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 14
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 6
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 14
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 11
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -10
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 15
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 15
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 7
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -2
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 12
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 11
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 15
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -15
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 9
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -9
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 12
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -3
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 12
mul y x
add z y
'''.splitlines()[1:]

def fast(i1, i2, i3, i4, i5, i6, i7, i8, i9, i10, i11, i12, i13, i14):

    w = x = y = z = 0

    w = i1 # inp w
    x *= 0 # mul x 0
    x += z # add x z
    x %= 26 # mod x 26
    z = int(z / 1) # div z 1
    x += 12 # add x 12
    x = 1 if x == w else 0 # eql x w
    x = 1 if x == 0 else 0 # eql x 0
    y *= 0 # mul y 0
    y += 25 # add y 25
    y *= x # mul y x
    y += 1 # add y 1
    z *= y # mul z y
    y *= 0 # mul y 0
    y += w # add y w
    y += 9 # add y 9
    y *= x # mul y x
    z += y # add z y
    w = i2 # inp w
    x *= 0 # mul x 0
    x += z # add x z
    x %= 26 # mod x 26
    z = int(z / 1) # div z 1
    x += 12 # add x 12
    x = 1 if x == w else 0 # eql x w
    x = 1 if x == 0 else 0 # eql x 0
    y *= 0 # mul y 0
    y += 25 # add y 25
    y *= x # mul y x
    y += 1 # add y 1
    z *= y # mul z y
    y *= 0 # mul y 0
    y += w # add y w
    y += 4 # add y 4
    y *= x # mul y x
    z += y # add z y
    w = i3 # inp w
    x *= 0 # mul x 0
    x += z # add x z
    x %= 26 # mod x 26
    z = int(z / 1) # div z 1
    x += 12 # add x 12
    x = 1 if x == w else 0 # eql x w
    x = 1 if x == 0 else 0 # eql x 0
    y *= 0 # mul y 0
    y += 25 # add y 25
    y *= x # mul y x
    y += 1 # add y 1
    z *= y # mul z y
    y *= 0 # mul y 0
    y += w # add y w
    y += 2 # add y 2
    y *= x # mul y x
    z += y # add z y
    w = i4 # inp w
    x *= 0 # mul x 0
    x += z # add x z
    x %= 26 # mod x 26
    z = int(z / 26) # div z 26
    x += -9 # add x -9
    x = 1 if x == w else 0 # eql x w
    x = 1 if x == 0 else 0 # eql x 0
    y *= 0 # mul y 0
    y += 25 # add y 25
    y *= x # mul y x
    y += 1 # add y 1
    z *= y # mul z y
    y *= 0 # mul y 0
    y += w # add y w
    y += 5 # add y 5
    y *= x # mul y x
    z += y # add z y
    w = i5 # inp w
    x *= 0 # mul x 0
    x += z # add x z
    x %= 26 # mod x 26
    z = int(z / 26) # div z 26
    x += -9 # add x -9
    x = 1 if x == w else 0 # eql x w
    x = 1 if x == 0 else 0 # eql x 0
    y *= 0 # mul y 0
    y += 25 # add y 25
    y *= x # mul y x
    y += 1 # add y 1
    z *= y # mul z y
    y *= 0 # mul y 0
    y += w # add y w
    y += 1 # add y 1
    y *= x # mul y x
    z += y # add z y
    w = i6 # inp w
    x *= 0 # mul x 0
    x += z # add x z
    x %= 26 # mod x 26
    z = int(z / 1) # div z 1
    x += 14 # add x 14
    x = 1 if x == w else 0 # eql x w
    x = 1 if x == 0 else 0 # eql x 0
    y *= 0 # mul y 0
    y += 25 # add y 25
    y *= x # mul y x
    y += 1 # add y 1
    z *= y # mul z y
    y *= 0 # mul y 0
    y += w # add y w
    y += 6 # add y 6
    y *= x # mul y x
    z += y # add z y
    w = i7 # inp w
    x *= 0 # mul x 0
    x += z # add x z
    x %= 26 # mod x 26
    z = int(z / 1) # div z 1
    x += 14 # add x 14
    x = 1 if x == w else 0 # eql x w
    x = 1 if x == 0 else 0 # eql x 0
    y *= 0 # mul y 0
    y += 25 # add y 25
    y *= x # mul y x
    y += 1 # add y 1
    z *= y # mul z y
    y *= 0 # mul y 0
    y += w # add y w
    y += 11 # add y 11
    y *= x # mul y x
    z += y # add z y
    w = i8 # inp w
    x *= 0 # mul x 0
    x += z # add x z
    x %= 26 # mod x 26
    z = int(z / 26) # div z 26
    x += -10 # add x -10
    x = 1 if x == w else 0 # eql x w
    x = 1 if x == 0 else 0 # eql x 0
    y *= 0 # mul y 0
    y += 25 # add y 25
    y *= x # mul y x
    y += 1 # add y 1
    z *= y # mul z y
    y *= 0 # mul y 0
    y += w # add y w
    y += 15 # add y 15
    y *= x # mul y x
    z += y # add z y
    w = i9 # inp w
    x *= 0 # mul x 0
    x += z # add x z
    x %= 26 # mod x 26
    z = int(z / 1) # div z 1
    x += 15 # add x 15
    x = 1 if x == w else 0 # eql x w
    x = 1 if x == 0 else 0 # eql x 0
    y *= 0 # mul y 0
    y += 25 # add y 25
    y *= x # mul y x
    y += 1 # add y 1
    z *= y # mul z y
    y *= 0 # mul y 0
    y += w # add y w
    y += 7 # add y 7
    y *= x # mul y x
    z += y # add z y
    w = i10 # inp w
    x *= 0 # mul x 0
    x += z # add x z
    x %= 26 # mod x 26
    z = int(z / 26) # div z 26
    x += -2 # add x -2
    x = 1 if x == w else 0 # eql x w
    x = 1 if x == 0 else 0 # eql x 0
    y *= 0 # mul y 0
    y += 25 # add y 25
    y *= x # mul y x
    y += 1 # add y 1
    z *= y # mul z y
    y *= 0 # mul y 0
    y += w # add y w
    y += 12 # add y 12
    y *= x # mul y x
    z += y # add z y
    w = i11 # inp w
    x *= 0 # mul x 0
    x += z # add x z
    x %= 26 # mod x 26
    z = int(z / 1) # div z 1
    x += 11 # add x 11
    x = 1 if x == w else 0 # eql x w
    x = 1 if x == 0 else 0 # eql x 0
    y *= 0 # mul y 0
    y += 25 # add y 25
    y *= x # mul y x
    y += 1 # add y 1
    z *= y # mul z y
    y *= 0 # mul y 0
    y += w # add y w
    y += 15 # add y 15
    y *= x # mul y x
    z += y # add z y
    w = i12 # inp w
    x *= 0 # mul x 0
    x += z # add x z
    x %= 26 # mod x 26
    z = int(z / 26) # div z 26
    x += -15 # add x -15
    x = 1 if x == w else 0 # eql x w
    x = 1 if x == 0 else 0 # eql x 0
    y *= 0 # mul y 0
    y += 25 # add y 25
    y *= x # mul y x
    y += 1 # add y 1
    z *= y # mul z y
    y *= 0 # mul y 0
    y += w # add y w
    y += 9 # add y 9
    y *= x # mul y x
    z += y # add z y
    w = i13 # inp w
    x *= 0 # mul x 0
    x += z # add x z
    x %= 26 # mod x 26
    z = int(z / 26) # div z 26
    x += -9 # add x -9
    x = 1 if x == w else 0 # eql x w
    x = 1 if x == 0 else 0 # eql x 0
    y *= 0 # mul y 0
    y += 25 # add y 25
    y *= x # mul y x
    y += 1 # add y 1
    z *= y # mul z y
    y *= 0 # mul y 0
    y += w # add y w
    y += 12 # add y 12
    y *= x # mul y x
    z += y # add z y
    w = i14 # inp w
    x *= 0 # mul x 0
    x += z # add x z
    x %= 26 # mod x 26
    z = int(z / 26) # div z 26
    x += -3 # add x -3
    x = 1 if x == w else 0 # eql x w
    x = 1 if x == 0 else 0 # eql x 0
    y *= 0 # mul y 0
    y += 25 # add y 25
    y *= x # mul y x
    y += 1 # add y 1
    z *= y # mul z y
    y *= 0 # mul y 0
    y += w # add y w
    y += 12 # add y 12
    y *= x # mul y x
    z += y # add z y

    return z


fr = int(argv[1])
for v3 in range(fr, 0, -1):
    for v4 in range(9, 0, -1):
        for v5 in range(9, 0, -1):
            for v6 in range(9, 0, -1):
                for v7 in range(9, 0, -1):
                    for v8 in range(9, 0, -1):
                        for v9 in range(9, 0, -1):
                            for v10 in range(9, 0, -1):
                                for v11 in range(9, 0, -1):
                                    for v12 in range(9, 0, -1):
                                        for v13 in range(9, 0, -1):
                                            for v14 in range(9, 0, -1):

                                                v1 = v2 = 9
                                                if all([v == 1 for v in [v9, v10, v11, v12, v13, v14]]):
                                                    print(f'  [{fr}] {"".join(map(str, (v1, v2, v3, v4, v5, v6, v7, v8 ,v9, v10, v11, v12, v13, v14)))}')

                                                z = fast(v1, v2, v3, v4, v5, v6, v7, v8 ,v9, v10, v11, v12, v13, v14)
                                                if z == 0:
                                                    print(f'SOLUTION: {"".join(map(str, (v1, v2, v3, v4, v5, v6, v7, v8 ,v9, v10, v11, v12, v13, v14)))}')
                                                    break
