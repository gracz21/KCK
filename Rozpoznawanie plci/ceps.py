from __future__ import division
import getopt
from pylab import *
from numpy import *
from scipy import *
import scipy.io.wavfile
import math
import os
import wave
import struct

def readwav(fname):
    wav = wave.open(fname, "r")
    nchannels, sampwidth, framerate, nframes, comptype, compname = wav.getparams()
    frames = wav.readframes(nframes * nchannels)
    out = struct.unpack_from("%dh" % nframes * nchannels, frames)
    if nchannels == 2:
        left = array(out[0::2], dtype='float_')
        left /= 2
        right = array(out[1::2], dtype='float_')
        right /= 2
        signal = left + right
    else:
        signal = array(out, dtype='float_')
    w = framerate
    return w, signal

listing = os.listdir('samples')
#file = '006_K.wav'
for file in listing:
    w, signal = readwav(file)

    window_size = 256
    n = len(signal)

    #print 'w: ', w, 'n: ', n

    f_list = []

    window = blackman(window_size)
    num_of_wind = math.ceil(n/window_size)
    print num_of_wind

    for i in range(1, num_of_wind + 1):
        chunk =
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


        signal2 = irfft(signal1)
        signal2 = abs(signal2)

        poz = 0
        r1 = int(w/80)
        r2 = int(w/255)
        m = max(signal2[r2:r1])
        for i in range(r2, r1):
            if m == signal2[i]:
                poz = i

        f_list.append(w/poz)

    f = median(array(f_list))

    print "Pitch: ", f

    if f <= 175:
        print file, 'M'
    else:
        print file, 'K'
