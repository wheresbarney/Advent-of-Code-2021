#!/usr/bin/env python3.8
# https://adventofcode.com/2021/day/22

# with full credit to https://www.reddit.com/r/adventofcode/comments/rlxhmg/comment/hpknuke

from dataclasses import dataclass
from itertools import combinations
from re import compile, search
from sys import argv


@dataclass(frozen=True)
class Cuboid:
    xmin: int
    xmax: int
    ymin: int
    ymax: int
    zmin: int
    zmax: int

    def volume(self):
        return (
            (self.xmax - self.xmin + 1)
            * (self.ymax - self.ymin + 1)
            * (self.zmax - self.zmin + 1))

    def intersects(self, other):
        return not(
            self.xmax < other.xmin or self.xmin > other.xmax
            or self.ymax < other.ymin or self.ymin > other.ymax
            or self.zmax < other.zmin or self.zmin > other.zmax)

    def intersection(self, other):
        if not self.intersects(other):
            return None
        return Cuboid(
            max(self.xmin, other.xmin),
            min(self.xmax, other.xmax),
            max(self.ymin, other.ymin),
            min(self.ymax, other.ymax),
            max(self.zmin, other.zmin),
            min(self.zmax, other.zmax))

    def get_non_occluded(self, other):
        """
        Returns up to six cuboids representing the remainder
            slices of this after occluding other
        """
        remainders = set()

        # top
        ymin = other.ymax + 1
        if ymin <= self.ymax:
            remainders.add(Cuboid(
                self.xmin, self.xmax, ymin, self.ymax, self.zmin, self.zmax
            ))
            ymin -= 1
        else:
            ymin = self.ymax

        # bottom
        ymax = other.ymin - 1
        if ymax >= self.ymin:
            remainders.add(Cuboid(
                self.xmin, self.xmax, self.ymin, ymax, self.zmin, self.zmax
            ))
            ymax += 1
        else:
            ymax = self.ymin

        # right
        xmin = other.xmax + 1
        if xmin <= self.xmax:
            remainders.add(Cuboid(
                xmin, self.xmax, ymax, ymin, self.zmin, self.zmax
            ))
            xmin -= 1
        else:
            xmin = self.xmax

        # left
        xmax = other.xmin - 1
        if xmax >= self.xmin:
            remainders.add(Cuboid(
                self.xmin, xmax, ymax, ymin, self.zmin, self.zmax
            ))
            xmax += 1
        else:
            xmax = self.xmin

        # back
        zmin = other.zmax + 1
        if zmin <= self.zmax:
            remainders.add(Cuboid(
                xmax, xmin, ymax, ymin, zmin, self.zmax
            ))

        # front
        zmax = other.zmin - 1
        if zmax >= self.zmin:
            remainders.add(Cuboid(
                xmax, xmin, ymax, ymin, self.zmin, zmax
            ))

        # sanity check - cannot overlap with each other
        assert all(not a.intersects(b) for (a, b) in combinations(remainders, 2)), f'{self} - {other} -> {remainders}'
        # cannot overlap with other
        assert all(not a.intersects(other) for a in remainders), f'{self} - {other} -> {remainders}'
        # must overlap with self
        assert all(a.intersects(self) for a in remainders), f'{self} - {other} -> {remainders}'

        return remainders

    def remove_intersection(self, other):
        intersection = self.intersection(other)
        if not intersection:
            return {self}
        if intersection == self:
            return set() # self entirely within other
        return self.get_non_occluded(other)

# unit tests
assert Cuboid(10, 12, 10, 12, 10, 12).volume() == 27

assert Cuboid(10, 12, 10, 12, 10, 12).intersects(Cuboid(10, 12, 9, 12, 10, 12))
assert not Cuboid(10, 12, 10, 12, 10, 12).intersects(Cuboid(20, 22, 20, 22, 20, 22))
assert Cuboid(10, 12, 10, 12, 10, 12).intersects(Cuboid(12, 22, 12, 22, 12, 22))

assert (
    Cuboid(10, 12, 10, 12, 10, 12).intersection(Cuboid(12, 22, 12, 22, 12, 22)).volume()
    == 1
)
assert (
    Cuboid(10, 12, 10, 12, 10, 12).intersection(Cuboid(20, 22, 20, 22, 20, 22)) is None
)

# would fail assertion internally
Cuboid(10, 20, 10, 20, 10, 20).get_non_occluded(Cuboid(11, 13, 11, 13, 11, 13))

def parse(input):
    rules = []
    pattern = compile('(\w+) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)')
    for line in input:
        m = pattern.search(line)
        rules.append((m[1] == 'on', Cuboid(int(m[2]), int(m[3]), int(m[4]), int(m[5]), int(m[6]), int(m[7]))))
    return rules

def restrict(coord):
    ret = min(abs(coord), 50)
    if coord < 0:
        ret *= -1
    return ret

def q1(input):
    rules = parse(input)
    core = [[[False for i in range(101)] for i in range(101)] for i in range(101)]
    for (state, cuboid) in rules:
        print(f'{cuboid}  --> {state}')
        for z in range(z1, z2+1):
            if abs(z) > 50:
                continue
            for y in range(y1, y2+1):
                if abs(y) > 50:
                    continue
                for x in range(x1, x2+1):
                    if abs(x) > 50:
                        continue
                    core[z+50][y+50][x+50] = state

    return sum([sum([len([c for c in x if c]) for x in y]) for y in core])

def volume(x1, x2, y1, y2, z1, z2):
    return (x2 - x1) * (y2 - y1) * (z2 - z1)

def intersection(boundary, region, exclude_regions):
    c1x1, c1x2, c1y1, c1y2, c1z1, c1z2 = boundary
    c2x1, c2x2, c2y1, c2y2, c2z1, c2z2 = region

    if \
            c1x2 < c2x1 or c1x1 > c2x2 or \
            c1y2 < c2y1 or c1y1 > c2y2 or \
            c1z2 < c2z1 or c1z1 > c2z2:
        intersection = 0
    else:
        intersection = volume(
            max(c1x1, c2x1), min(c1x2, c2x2),
            max(c1y1, c2y1), min(c1y2, c2y2),
            max(c1z1, c2z1), min(c1z2, c2z2))

    print(f'    {intersection=} ({c1x1}..{c1x2}, {c1y1}..{c1y2}, {c1z1}..{c1z2}) with ({c2x1}..{c2x2}, {c2y1}..{c2y2}, {c2z1}..{c2z2})')
    return intersection

def q2_double_counting(input):
    rules = parse(input)

    # for each On cube in ruleset:
    #     compute volume
    #     subtract intersection of all future rules
    total_active = 0
    for i, rule in enumerate(rules):
        print(f'considering {rule}')
        if not rule[0]:
            continue

        active = volume(*rule[1:])
        # print(f'  original vol={active}')
        exclude_regions = []
        for override in rules[i+1:]:
            active -= intersection(rule[1:], override[1:], exclude_regions)
            exclude_regions.append(override)
        print(f'  adjusted vol={active}')

        total_active += active

    return total_active

def q2(input):
    rules = parse(input)
    all_active = set()
    for this_activate, this_cuboid in rules:
        new_active = set()
        for activated in all_active:
            new_active |= activated.remove_intersection(this_cuboid)
        if this_activate:
            new_active.add(this_cuboid)
        all_active = new_active
    return sum(c.volume() for c in all_active)

if len(argv) > 1:
    with open(argv[1], 'r') as f:
        print(q2([l.strip() for l in f]))
else:
    print(q2([l.strip() for l in '''
on x=-5..47,y=-31..22,z=-19..33
on x=-44..5,y=-27..21,z=-14..35
on x=-49..-1,y=-11..42,z=-10..38
on x=-20..34,y=-40..6,z=-44..1
off x=26..39,y=40..50,z=-2..11
on x=-41..5,y=-41..6,z=-36..8
off x=-43..-33,y=-45..-28,z=7..25
on x=-33..15,y=-32..19,z=-34..11
off x=35..47,y=-46..-34,z=-11..5
on x=-14..36,y=-6..44,z=-16..29
on x=-57795..-6158,y=29564..72030,z=20435..90618
on x=36731..105352,y=-21140..28532,z=16094..90401
on x=30999..107136,y=-53464..15513,z=8553..71215
on x=13528..83982,y=-99403..-27377,z=-24141..23996
on x=-72682..-12347,y=18159..111354,z=7391..80950
on x=-1060..80757,y=-65301..-20884,z=-103788..-16709
on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856
on x=-52752..22273,y=-49450..9096,z=54442..119054
on x=-29982..40483,y=-108474..-28371,z=-24328..38471
on x=-4958..62750,y=40422..118853,z=-7672..65583
on x=55694..108686,y=-43367..46958,z=-26781..48729
on x=-98497..-18186,y=-63569..3412,z=1232..88485
on x=-726..56291,y=-62629..13224,z=18033..85226
on x=-110886..-34664,y=-81338..-8658,z=8914..63723
on x=-55829..24974,y=-16897..54165,z=-121762..-28058
on x=-65152..-11147,y=22489..91432,z=-58782..1780
on x=-120100..-32970,y=-46592..27473,z=-11695..61039
on x=-18631..37533,y=-124565..-50804,z=-35667..28308
on x=-57817..18248,y=49321..117703,z=5745..55881
on x=14781..98692,y=-1341..70827,z=15753..70151
on x=-34419..55919,y=-19626..40991,z=39015..114138
on x=-60785..11593,y=-56135..2999,z=-95368..-26915
on x=-32178..58085,y=17647..101866,z=-91405..-8878
on x=-53655..12091,y=50097..105568,z=-75335..-4862
on x=-111166..-40997,y=-71714..2688,z=5609..50954
on x=-16602..70118,y=-98693..-44401,z=5197..76897
on x=16383..101554,y=4615..83635,z=-44907..18747
off x=-95822..-15171,y=-19987..48940,z=10804..104439
on x=-89813..-14614,y=16069..88491,z=-3297..45228
on x=41075..99376,y=-20427..49978,z=-52012..13762
on x=-21330..50085,y=-17944..62733,z=-112280..-30197
on x=-16478..35915,y=36008..118594,z=-7885..47086
off x=-98156..-27851,y=-49952..43171,z=-99005..-8456
off x=2032..69770,y=-71013..4824,z=7471..94418
on x=43670..120875,y=-42068..12382,z=-24787..38892
off x=37514..111226,y=-45862..25743,z=-16714..54663
off x=25699..97951,y=-30668..59918,z=-15349..69697
off x=-44271..17935,y=-9516..60759,z=49131..112598
on x=-61695..-5813,y=40978..94975,z=8655..80240
off x=-101086..-9439,y=-7088..67543,z=33935..83858
off x=18020..114017,y=-48931..32606,z=21474..89843
off x=-77139..10506,y=-89994..-18797,z=-80..59318
off x=8476..79288,y=-75520..11602,z=-96624..-24783
on x=-47488..-1262,y=24338..100707,z=16292..72967
off x=-84341..13987,y=2429..92914,z=-90671..-1318
off x=-37810..49457,y=-71013..-7894,z=-105357..-13188
off x=-27365..46395,y=31009..98017,z=15428..76570
off x=-70369..-16548,y=22648..78696,z=-1892..86821
on x=-53470..21291,y=-120233..-33476,z=-44150..38147
off x=-93533..-4276,y=-16170..68771,z=-104985..-24507
'''.splitlines()[1:]]))
