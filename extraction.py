from scapy.all import *
import os
from collections import defaultdict as dd
from tqdm import tqdm
from scapy.layers.inet import IP
from scapy.layers.l2 import Ether

def fix_digit(x):
    if len(x) == 1:
        return '0'+x
    else:
        return x


def get_feat_dir(dataset):
    feat = os.path.join(dataset, 'attack_feat')
    if not os.path.exists(feat):
        os.mkdir(feat)

    return feat


def get_dataset(dataset):
    attack = os.path.join(dataset, 'Ddos_Dataset_Part2')
    dirs = os.listdir(attack)
    dirs = list(map(lambda x: int(x), dirs))
    dirs.sort()
    dirs = filter(lambda x: x < 85, dirs)
    dirs = list(map(lambda x: str(x), dirs))
    dirs = list(map(fix_digit, dirs))

    completed = os.listdir(get_feat_dir(dataset))
    completed = set(list(map(lambda x: x.split('.')[0], completed)))
    dirs = filter(lambda x: x not in completed, dirs)

    dirs = list(map(lambda x: os.path.join(attack, x), dirs))
    return dirs


def get_packet_layers(packet):
    counter = 0
    while True:
        layer = packet.getlayer(counter)
        if layer is None:
            break

        yield layer.name
        counter += 1


def UDPCheck(pkt):
  s = set()
  for layer in get_packet_layers(pkt):
    s.add(layer)
  return 'UDP' in s


def getData(pcap):
    count = 0
    udp = 0
    times = []
    src = []
    dst = []
    size = []
    traffic = dd(lambda: 0)
    for (pkt_data, pkt_metadata) in tqdm(RawPcapReader(pcap)):
        count += 1
        ether = Ether(pkt_data)
        ip = IP(pkt_data)
        if UDPCheck(ether):
            udp += 1

        times.append(ip.time)
        src.append(ip.src)
        dst.append(ip.dst)
        size.append(ip.len)
        traffic[(ip.src, ip.dst)] += ip.len

    udp = (udp / count) * 100
    traffic = dict(traffic)

    result = {
        'times': times,
        'src': src,
        'dst': dst,
        'size': size,
        'traffic': traffic,
        'udp': udp,
        'count': count
    }
    return result






