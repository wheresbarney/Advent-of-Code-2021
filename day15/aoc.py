#!/usr/bin/env python3.8
# https://adventofcode.com/2021/day/15


from sys import argv, maxsize


def get_neighbours(node, map):
    neighbours = []
    if node[0] != 0:
        neighbours.append((node[0]-1, node[1]))
    if node[0] != len(map)-1:
        neighbours.append((node[0]+1, node[1]))
    if node[1] != 0:
        neighbours.append((node[0], node[1]-1))
    if node[1] != len(map[0])-1:
        neighbours.append((node[0], node[1]+1))
    # print(f'  neighbours of {node}: {neighbours}')
    return neighbours


def dijkstra_shortest_path(map):
    previous_nodes = {}
    unvisited_nodes = {(y, x) for x in range(len(map[0])) for y in range(len(map))}
    # shortest_path = {u: maxsize for u in unvisited_nodes}
    # shortest_path[(0, 0)] = 0
    shortest_path = {(0, 0): 0}

    i = 0
    while unvisited_nodes:
        current_min_node = None
        for node in unvisited_nodes & shortest_path.keys():
            if current_min_node == None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node

        neighbours = get_neighbours(current_min_node, map)
        if i % 100 == 0:
            print(f'{i}/{len(map) * len(map[0])}: {current_min_node} ({shortest_path[current_min_node]})')
        i += 1

        for neighbour in neighbours:
            tentative_value = shortest_path[current_min_node] + map[neighbour[0]][neighbour[1]]
            if tentative_value < shortest_path.get(neighbour, maxsize):
                shortest_path[neighbour] = tentative_value
                previous_nodes[neighbour] = current_min_node

        unvisited_nodes.remove(current_min_node)

    # print(shortest_path)
    return shortest_path[(len(map)-1, len(map[0])-1)]


def q1(input):
    return dijkstra_shortest_path([[int(i) for i in r] for r in input])


def q2(input):
    tile = [[int(i) for i in r] for r in input]
    map = [[None for _ in range(len(tile[0]) * 5)] for _ in range(len(tile) * 5)]
    for tile_y in range(5):
        for tile_x in range(5):
            for y in range(len(tile)):
                for x in range(len(tile[0])):
                    val = tile[y][x] + tile_x + tile_y
                    while val > 9:
                        val -= 9
                    map[tile_y * len(tile) + y][tile_x * len(tile[0]) + x] = val
    return dijkstra_shortest_path(map)


if len(argv) > 1:
    with open(argv[1], 'r') as f:
        print(q2([l.strip() for l in f]))
else:
    print(q2([l.strip() for l in '''
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
'''.splitlines()[1:]]))
