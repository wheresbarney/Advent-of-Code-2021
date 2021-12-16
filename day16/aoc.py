#!/usr/bin/env python3.8
# https://adventofcode.com/2021/day/16


from math import prod
from sys import argv


def parse_literal(packet):
    pos = 0
    bin = ''
    while True:
        bin += packet[pos+1:pos+5]
        flag = packet[pos]
        pos += 5
        if flag == '0':
            break

    return packet[pos:], int(bin, 2)


def parse_length_operator(packet):
    bits = int(packet[:15], 2)
    # print(f'    parse_length_op {bits=} ({packet})')
    packets = parse_packets(packet[15:15+bits])
    return packet[15+bits:], packets


def parse_num_subpackets_operator(packet):
    packets = []
    num_packets = int(packet[:11], 2)
    # print(f'    parse_num_op {num_packets=} ({packet})')
    packet = packet[11:]
    for i in range(num_packets):
        packet, new_packet = parse_single_packet(packet)
        packets.append(new_packet)
    return packet, packets


def parse_single_packet(packet_str):
    version = int(packet_str[0:3], 2)
    type = int(packet_str[3:6], 2)
    # print(f' parse_single_packet {version=}, {type=} ({packet_str})')

    if type == 4:
        packet_str, val = parse_literal(packet_str[6:])
        packet = (version, type, val)
    else:
        if packet_str[6:7] == '0':
            op_type = 'len'
            packet_str, new_packets = parse_length_operator(packet_str[7:])
        else:
            op_type = 'num'
            packet_str, new_packets = parse_num_subpackets_operator(packet_str[7:])

        # print(f'    {(version, type, "???", op_type, new_packets)}')
        val = 0
        if type == 0:
            val = sum([p[2] for p in new_packets])
        elif type == 1:
            val = prod([p[2] for p in new_packets])
        elif type == 2:
            val = min([p[2] for p in new_packets])
        elif type == 3:
            val = max([p[2] for p in new_packets])
        elif type == 5:
            if new_packets[0][2] > new_packets[1][2]:
                val = 1
        elif type == 6:
            if new_packets[0][2] < new_packets[1][2]:
                val = 1
        elif type == 7:
            if new_packets[0][2] == new_packets[1][2]:
                val = 1

        packet = (version, type, val, op_type, new_packets)
        # print(f'    -->{packet}')

    return packet_str, packet


def parse_packets(packet_str):
    packets = []
    while '1' in packet_str:
        packet_str, new_packet = parse_single_packet(packet_str)
        packets.append(new_packet)
    return packets


def hex_to_bin(input):
    binary = ''
    pointer = 0
    while len(input) - pointer > 0:
        chunk = bin(int(input[pointer:pointer+1], 16))[2:]
        chunk = ('0' * (4 - len(chunk))) + chunk
        binary += chunk
        # print(f'{input[pointer:pointer+1]} --> {chunk}, {pointer=}')
        pointer += 1

    print(f'{input} --> {binary}')
    return binary


def q1(input):
    packets = parse_packets(hex_to_bin(input))

    for packet in packets:
        print(f'  {packet}')
    return sum([p[0] for p in packets])


def q2(input):
    packets = parse_packets(hex_to_bin(input))

    print(f'{packet}')
    return packets[0][2]


if len(argv) > 1:
    with open(argv[1], 'r') as f:
        print(q2([l.strip() for l in f][0]))
else:
    print([q2(l.strip()) for l in '''
C200B40A82
04005AC33890
880086C3E88112
CE00C43D881120
D8005AC2A8F0
F600BC2D8F
9C005AC2F8F0
9C0141080250320F1802104A08
'''.splitlines()[1:]])


'''
D2FE28
38006F45291200
EE00D40C823060
8A004A801A8002F478
620080001611562C8802118E34
C0015000016115A2E0802F182340
A0016C880162017C3686B18A3D4780
'''
