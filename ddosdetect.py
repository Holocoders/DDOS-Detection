from extraction import getData
from features import features
import argparse
import pickle


def write(src, dst):
    with open('result.txt', 'w') as f:
        f.write('src: {}     dst: {}'.format(src, dst))


def readData():
    with open('data.p', 'rb') as f:
        d = pickle.load(f)
    return d


def eval(path):
    result = getData(path)
    result, src, dst = features(result)
    result = result.reshape(1, -1)
    model, scaler, df = readData()
    result = scaler.transform(result)
    preds = model.predict(result)
    
    if preds[0] == 1:
        write(src, dst)
    else:
        with open('result.txt', 'w') as f:
            f.write('benign')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    args = parser.parse_args()
    path = args.file
    eval(path)
