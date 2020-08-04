from collections import Counter

import numpy as np

def cumsub(times):
  result = []
  for t in range(len(times)-1):
    result.append(times[t+1]-times[t])

  return np.array(result)


def frequency(times):
  cb = cumsub(times)
  d = {
      'mean': np.mean(cb),
       'std': np.std(cb)
  }
  return d


def total_time(times):
  low, high = min(times), max(times)
  dt = high-low
  return dt


def traffic(times, traffic):
  dt = total_time(times)
  vals = np.array(list(traffic.values()))
  max_val = np.max(vals)
  src, dst = max(traffic, key=traffic.get)
  d = {
      'bandwidth': max_val/dt,
      'mean': np.mean(vals),
      'std': np.std(vals),
      'src': src,
      'dst': dst
  }
  return d


def packetsize(size):
  size = np.array(size)
  d = {
      'mean': np.mean(size),
      'std': np.std(size),
      'max': np.max(size),
      'min': np.min(size),
      'total': np.sum(size)
  }
  return d


def unique_IP(src, dst):
  counter = Counter(dst)
  dst_counts = np.array(list(dict(counter).values()))
  d = {
      'src_count': len(set(src)),
      'dst_count': len(set(dst)),
      'mean_dst': np.mean(dst_counts),
      'std_dst': np.std(dst_counts)
  }
  return d


def features(d):
  freq = frequency(d['times'])
  time_taken = total_time(d['times'])
  traf = traffic(d['times'], d['traffic'])
  size = packetsize(d['size'])
  ip = unique_IP(d['src'], d['dst'])
  udp = d['udp']

  result = [
            freq['mean'], freq['std'], time_taken, traf['bandwidth'], traf['mean'], traf['std'],
            size['mean'], size['std'], size['max'], size['min'], size['total'],
            ip['src_count'], ip['dst_count'], ip['mean_dst'], ip['std_dst'], udp
            ]

  return np.array(result), traf['src'], traf['dst'],
