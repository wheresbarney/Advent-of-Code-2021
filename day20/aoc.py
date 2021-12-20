#!/usr/bin/env python3.8
# https://adventofcode.com/2021/day/20


from sys import argv


def parse(input):
    algo = input[0]
    assert len(algo) == 512
    image = []
    for line in input[2:]:
        image.append([c for c in line])
    return image, algo


def get_key(image, r, c, default):
    ret = ''
    for dr in range(r-1, r+2):
        for dc in range(c-1, c+2):
            if dr < 0 or dc < 0 or dr >= len(image) or dc >= len(image[0]):
                ret += default
            else:
                ret += image[dr][dc]
    return ret


lookup_table = {'#': '1', '.': '0'}
def lookup(key, algo):
    binary = ''.join([lookup_table[c] for c in key])
    return algo[int(binary, 2)]


def enhance(image, algo, default):
    new_image = []
    for r in range(-1, len(image)+1):
        new_row = []
        new_image.append(new_row)
        for c in range(-1, len(image[0])+1):
            key = get_key(image, r, c, default)
            enhanced = lookup(key, algo)
            # binary = ''.join([lookup_table[c] for c in key])
            # dec = int(binary, 2)
            # print(f'[{r}, {c}]: {key} -> {binary} -> {dec} -> {enhanced}')
            new_row.append(enhanced)
    assert len(new_image) == len(image) + 2
    assert len(new_image[0]) == len(image[0]) + 2
    return new_image


def q1(input, count):
    image, algo = parse(input)

    default = '.'
    for i in range(count):
        image = enhance(image, algo, default)
        default = lookup(default * 9, algo)

    for r in image:
        print(''.join(r))

    return sum([r.count('#') for r in image])


if len(argv) > 1:
    with open(argv[1], 'r') as f:
        print(q1([l.strip() for l in f], 50))
else:
    print(q1([l.strip() for l in '''
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
'''.splitlines()[1:]], 50))
