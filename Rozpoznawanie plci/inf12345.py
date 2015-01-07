from __future__ import division
import getopt
from pylab import *
from numpy import *
from scipy import *
import wave
import struct


def opensignal(fname):
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


def clearsignal(fft_signal, n, w):
    r1 = int(math.floor(60*n/w))
    for i in range(1, r1):
        fft_signal[i] = 0

    r2 = int(math.ceil(300*n/w))
    for i in range(r2, len(fft_signal)):
        fft_signal[i] = 0

    m = max(fft_signal[1:])

    for i in range(r1 - 1, r2):
        if fft_signal[i] < m/2:
            fft_signal[i] = 0


def countfreq(fft_signal, n, w):
    r1 = int(math.floor(85*n/w))
    r2 = int(math.ceil(180*n/w))

    man = 0
    for i in range(r1, r2):
        man += fft_signal[i]

    r1 = int(math.floor(165*n/w))
    r2 = int(math.ceil(255*n/w))

    woman = 0
    for i in range(r1, r2):
        woman += fft_signal[i]

    return man, woman


def cepstrum(signal, n, w):
    signal1 = rfft(signal)
    signal1 = abs(signal1)

    clearsignal(signal1, n, w)

    man, woman = countfreq(signal1, n, w)

    for i in range(0, len(signal1)):
        if signal1[i] > 0:
            signal1[i] = log(signal1[i])

    signal2 = irfft(signal1)
    signal2 = abs(signal2)

    poz = 0
    r1 = int(w/80)
    r2 = int(w/255)
    m = max(signal2[r2:r1])
    for i in range(r2, r1):
        if m == signal2[i]:
            poz = i

    f = w/poz
    return f, man, woman


def main(argv):
    opts, file = getopt.getopt(argv, [])

    w, signal = opensignal(file[0])
    n = len(signal)

    f, man, woman = cepstrum(signal, n, w)

    if f <= 165:
        print('M')
    else:
        if f >= 180:
            print('K')
        else:
            if man >= woman:
                print ('M')
            else:
                print ('K')

if __name__ == "__main__":
   main(sys.argv[1:])