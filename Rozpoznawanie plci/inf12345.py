from __future__ import division
import getopt
from pylab import *
from numpy import *
from scipy import *
import scipy.io.wavfile


def opensignal(file):
    w, data = scipy.io.wavfile.read(file)
    signal = np.zeros(data.shape[0])
    if len(data.shape) == 2:
        signal = monofromstereo(data, signal)
    else:
        signal = data
    return signal, w


def monofromstereo(data, signal):
    for i in range(data.shape[0]):
        tmp1 = data[i][0]/2
        tmp2 = data[i][1]/2
        tmp = tmp1 + tmp2
        signal[i] = tmp
    return signal


def main(argv):
    opts, file = getopt.getopt(argv, [])

    signal, w = opensignal(file)
    n = len(signal)

    print signal

    signal1 = rfft(signal)

    r1 = int(math.floor(60*n/w))
    for i in range(1, r1):
        signal1[i] = 0

    r2 = int(math.ceil(300*n/w))
    for i in range(r2, len(signal1)):
        signal1[i] = 0

    poz = 0
    m = max(signal1[1:])
    for i in range(len(signal1[1:])):
        if m == signal1[i]:
            poz = i

    for i in range(r1 - 1, r2):
        if abs(signal1[i]) < m/2:
            signal1[i] = 0

    #m = max(signal1)

    #print m

    #for i in range(1, 299):
        #signal1[i] = 0

    for i in range(5000, len(signal1)):
        signal1[i] = 0


if __name__ == "__main__":
   main(sys.argv[1:])