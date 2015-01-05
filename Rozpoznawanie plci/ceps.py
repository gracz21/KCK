from __future__ import division
import getopt
from pylab import *
from numpy import *
from scipy import *
import scipy.io.wavfile
import math
import os
import wave

#opts, file = getopt.getopt(argv, [])
listing = os.listdir('samples')
#file = '006_K.wav'
for file in listing:
    w, data = scipy.io.wavfile.read(file)

    signal = np.zeros(data.shape[0])
    if len(data.shape) == 2:
        for i in range(data.shape[0]):
            tmp1 = data[i][0]/2
            tmp2 = data[i][1]/2
            tmp = tmp1 + tmp2
            signal[i] = tmp
    else:
        signal = data

    T = 1
    n = len(signal)
    t = linspace(0, T, n, endpoint=False)

    signal1 = rfft(signal)
    signal1 = abs(signal1)

    r1 = int(math.floor(60*n/w))
    for i in range(1, r1):
        signal1[i] = 0

    r2 = int(math.ceil(300*n/w))
    for i in range(r2, len(signal1)):
        signal1[i] = 0

    m = max(signal1[1:])

    for i in range(r1 - 1, r2):
        if abs(signal1[i]) < m/2:
            signal1[i] = 0

    r1 = int(math.floor(85*n/w))
    r2 = int(math.ceil(180*n/w))

    men = 0
    for i in range(r1, r2):
        men += abs(signal1[i])

    r1 = int(math.floor(165*n/w))
    r2 = int(math.ceil(255*n/w))

    woman = 0
    for i in range(r1, r2):
        woman += abs(signal1[i])

    for i in range(0, len(signal1)):
        if signal1[i] > 0:
            signal1[i] = log(signal1[i])

    signal2 = irfft(signal1)
    signal2 = abs(signal2)

    poz = 0
    r1 = int(w/80)
    r2 = int(w/250)
    m = max(signal2[r2:r1])
    for i in range(r2, r1):
        if m == signal2[i]:
            poz = i

    f = w/poz

    print "Pitch: ", f

    if f <= 165:
        print file, 'M'
    else:
        if f >= 180:
            print file, 'K'
        else:
            if men >= woman:
                print file, 'M'
            else:
                print file, 'K'
