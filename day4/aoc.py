#!/usr/bin/env python3.8
# https://adventofcode.com/2021/day/4

from sys import argv
from collections import defaultdict, namedtuple

def parseInput(input):
    numbers = [int(n) for n in input[0].split(',')]
    boards = [[]] # appending list to empty list appends the contents of the list, not the list itself
    board = []
    for line in input[2:]:
        if line:
            board.append([int(x) for x in line.split(' ') if x])
        else:
            boards.append(board)
            board = []
    boards.append(board)
    boards.pop(0) # delete the empty initial entry

    index = defaultdict(list)
    Coord = namedtuple('Coord', ['board', 'row', 'col'])
    for b, board in enumerate(boards):
        for r, row in enumerate(board):
            for c, cell in enumerate(row):
                index[cell].append(Coord(b, r, c))
    # print(f'{numbers=}')
    # print(f'{boards=}')
    # print(f'{index=}')
    return (numbers, boards, index)

def complete(board):
    for row in board:
        if row.count(0) == 0:
            return True
    for i in range(len(board)):
        if [row[i] for row in board].count(0) == 0:
            return True
    return False

def unmarkedSum(board, marks):
    unmarkedSum = 0
    for r, row in enumerate(marks):
        for c, cell in enumerate(row):
            if cell == 0:
                unmarkedSum += board[r][c]
    return unmarkedSum

def q1(input):
    numbers, boards, index = parseInput(input)
    marks = [[[0 for x in boards[0]] for x in boards[0]] for x in boards]
    for n in numbers:
        for coord in index[n]:
            marks[coord.board][coord.row][coord.col] = 1
            if complete(marks[coord.board]):
                print(f'Winner at {coord} after {n}')
                return unmarkedSum(boards[coord.board], marks[coord.board]) * n

def q2(input):
    numbers, boards, index = parseInput(input)
    marks = [[[0 for x in boards[0]] for x in boards[0]] for x in boards]
    unwonBoards = [i for i in range(len(boards))]
    for n in numbers:
        for coord in index[n]:
            if coord.board in unwonBoards:
                marks[coord.board][coord.row][coord.col] = 1
                if complete(marks[coord.board]):
                    print(f'Board {coord.board} won at {coord} after {n}')
                    unwonBoards.remove(coord.board)
                    if len(unwonBoards) == 0:
                        print(f'Final board won at {coord}')
                        return unmarkedSum(boards[coord.board], marks[coord.board]) * n

if len(argv) > 1:
    with open(argv[1], 'r') as f:
        print(q2([l.strip() for l in f]))
else:
    print(q2([l.strip() for l in '''7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
'''.splitlines()]))
