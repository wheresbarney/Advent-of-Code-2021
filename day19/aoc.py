#!/usr/bin/env python3.8
# https://adventofcode.com/2021/day/19


from sys import argv


class Scanner:
    def __init__(self, index):
        self.index = index
        self.beacons = []
        self.centre = None

    def relative_positions(self, beacon_index):
        ret = set()
        anchor = self.beacons[beacon_index]
        for i, beacon in enumerate(self.beacons):
            if i == beacon_index:
                continue
            ret.add((beacon.x - anchor.x, beacon.y - anchor.y, beacon.z - anchor.z))
        return ret

    def rotate(self, count):
        for beacon in self.beacons:
            beacon.rotate_on_x()
            if count % 4 == 0:
                if count < 16:
                    beacon.rotate_on_y()
                else:
                    beacon.rotate_on_z()

    def set_offset(self, offset):
        self.centre = offset
        for beacon in self.beacons:
            beacon.x += offset[0]
            beacon.y += offset[1]
            beacon.z += offset[2]

    def __str__(self):
        return f'<Scanner:{self.index}@{self.centre} {self.beacons}>'

    def __repr__(self):
        return self.__str__()


class Beacon:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def rotate_on_x(self):
        temp = self.y
        self.y = self.z
        self.z = temp * -1

    def rotate_on_y(self):
        temp = self.x
        self.x = self.z
        self.z = temp * -1

    def rotate_on_z(self):
        temp = self.x
        self.x = self.y
        self.y = temp * -1

    def __str__(self):
        return f'{(self.x, self.y, self.z)}'

    def __repr__(self):
        return self.__str__()


def parse(input):
    scanners = []
    scanner = None
    for line in input:
        if 'scanner' in line:
            scanner = Scanner(int(line.split(' ')[2]))
            scanners.append(scanner)
        elif line.count(',') == 2:
            ints = [int(n) for n in line.split(',')]
            scanner.beacons.append(Beacon(ints[0], ints[1], ints[2]))

    scanners[0].centre = (0, 0, 0)
    # print(f'{scanners=}')
    return scanners

def matches(anchor, candidate):
    for anchor_beacon_index in range(len(anchor.beacons)):
        for rotation in range(24):
            for candidate_beacon_index in range(len(candidate.beacons)):
                matches = anchor.relative_positions(anchor_beacon_index) & candidate.relative_positions(candidate_beacon_index)
                if len(matches) >= 11: # 11 because the anchor pairs are implicit match
                    anchor_beacon = anchor.beacons[anchor_beacon_index]
                    candidate_beacon = candidate.beacons[candidate_beacon_index]
                    return (anchor_beacon.x - candidate_beacon.x, anchor_beacon.y - candidate_beacon.y, anchor_beacon.z - candidate_beacon.z)
            candidate.rotate(rotation)
    return None


def q1(input):
    scanners = parse(input)

    matched = [0] # queue to be evaluated against unmatched
    unmatched = {i for i in range(1, len(scanners))}
    while matched:
        anchor = scanners[matched.pop()]
        new_matches = []
        for c in unmatched:
            candidate = scanners[c]
            if offset := matches(anchor, candidate):
                print(f'match between {anchor.index} and {candidate.index}; candidate is at {offset=}')
                candidate.set_offset(offset) # candidate is already aligned correctly relative to anchor
                new_matches.append(c)
        for s in new_matches:
            unmatched.remove(s)
        matched += new_matches

    # print(f'{scanners=}')
    distinct = set()
    for scanner in scanners:
        distinct.update({(b.x, b.y, b.z) for b in scanner.beacons})
    max_manhatten = 0
    for i in range(len(scanners)):
        for j in range(i + 1, len(scanners)):
            c1 = scanners[i].centre
            c2 = scanners[j].centre
            max_manhatten = max(max_manhatten, abs(c2[0] - c1[0]) + abs(c2[1] - c1[1]) + abs(c2[2] - c1[2]))
    return (len(distinct), max_manhatten)

if len(argv) > 1:
    with open(argv[1], 'r') as f:
        print(q1([l.strip() for l in f]))
else:
    print(q1([l.strip() for l in '''
--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14
'''.splitlines()[1:]]))
