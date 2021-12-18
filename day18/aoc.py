#!/usr/bin/env python3.8
# https://adventofcode.com/2021/day/18


from sys import argv

class Node:
    def __init__(self):
        self.left = self.right = self.parent = None

    def __str__(self):
        return f'[{self.left}, {self.right}]'

    def __repr__(self):
        return self.__str__()

    def addChild(self, child):
        if self.left is None:
            self.left = child
        else:
            self.right = child
        child.parent = self

    def replace(self, node, new_node):
        if node == self.left:
            self.left = new_node
        else:
            assert self.right == node
            self.right = new_node
        new_node.parent = self

    def leaves(self, all_leaves):
        if isinstance(self.left, LeafNode):
            all_leaves.append(self.left)
        else:
            self.left.leaves(all_leaves)

        if isinstance(self.right, LeafNode):
            all_leaves.append(self.right)
        else:
            self.right.leaves(all_leaves)

        return all_leaves

    def magnitude(self):
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()


class LeafNode:
    def __init__(self, n):
        self.val = n
        self.parent = None

    def __str__(self):
        return str(self.val)

    def __repr__(self):
        return self.__str__()

    def magnitude(self):
        return self.val


def parse(input):
    ret = []
    for l in input:
        node = graph = Node()
        for c in l[1:]:
            if c.isdigit():
                node.addChild(LeafNode(int(c)))
            elif c == '[':
                new_node = Node()
                node.addChild(new_node)
                node = new_node
            elif c == ']':
                node = node.parent
        # print(f'{l} -> {graph}')
        ret.append(graph)
    return ret


def add(left, right):
    ret = Node()
    ret.addChild(left)
    ret.addChild(right)
    return ret


def needs_exploding(num, count=0):
    if count == 4:
        return num
    if isinstance(num.left, Node):
        exploder = needs_exploding(num.left, count + 1)
        if exploder:
            return exploder
    if isinstance(num.right, Node):
        exploder = needs_exploding(num.right, count + 1)
        if exploder:
            return exploder

    return None


def needs_splitting(num):
    if isinstance(num.left, LeafNode):
        if num.left.val >= 10:
            return num.left
    else:
        splitter = needs_splitting(num.left)
        if splitter:
            return splitter

    if isinstance(num.right, LeafNode):
        if num.right.val >= 10:
            return num.right
    else:
        splitter = needs_splitting(num.right)
        if splitter:
            return splitter

    return None


def reduce(num):
    reduced = False
    while not reduced:
        reduced = True
        exploder = needs_exploding(num)
        if exploder:
            explode(exploder, num)
            # print(f'  after exploding {exploder}: {num}')
            reduced = False
            continue

        splitter = needs_splitting(num)
        if splitter:
            split(splitter, num)
            # print(f'  after splitting {splitter}: {num}')
            reduced = False
            continue

    return num


def explode(exploder, graph):
    all_leaves = graph.leaves([])
    for i in range(len(all_leaves)):
        if all_leaves[i].parent == exploder:
            if i > 0:
                all_leaves[i-1].val += exploder.left.val
            if i < len(all_leaves) - 2:
                all_leaves[i+2].val += exploder.right.val
            break
    exploder.parent.replace(exploder, LeafNode(0))


def split(splitter, num):
    new_node = Node()
    new_node.addChild(LeafNode(int(splitter.val / 2)))
    new_node.addChild(LeafNode(int((splitter.val + 1) / 2)))
    splitter.parent.replace(splitter, new_node)


def q1(input):
    nums = parse(input)
    num = nums[0]
    for i in range(1, len(nums)):
        num = add(num, nums[i])
        # print(f' after addition of {nums[i]}: {num}')
        reduce(num)
        # print(f'after reducing: {num}')
    print(num)
    return num.magnitude()


def q2(input):
    ret = 0
    for i in range(len(input)):
        for j in range(i+1, len(input)):
            nums = parse(input)
            num = reduce(add(nums[i], nums[j]))
            ret = max(ret, num.magnitude())

            nums = parse(input)
            num = reduce(add(nums[j], nums[i]))
            ret = max(ret, num.magnitude())
    return ret

if len(argv) > 1:
    with open(argv[1], 'r') as f:
        print(q2([l.strip() for l in f]))
else:
    print(q2([l.strip() for l in '''
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
'''.splitlines()[1:]]))
