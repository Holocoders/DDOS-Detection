import numpy
from extraction import getData
from features import features
import argparse

def write(src, dst, res):
    with open('result.txt', 'w') as f:
        f.write('{} {} {}'.format(src, dst, res))


def eval(path):
    result = getData(path)
    result, src, dst = features(result)
    result = result.T



if __name__ == '__main__':
    pass