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


def clearsignal(fft_signal):
    m = max(fft_signal[1:])

    for i in range(1, len(fft_signal)):
        if fft_signal[i] < m/2:
            fft_signal[i] = 0


def cepstrum(signal, n, w):
    window_time = 250
    window_width = int(window_time*w/1000)
    num_of_wind = int(n/window_width)

    f = []

    for i in range(num_of_wind):
        poz = i*window_width
        signal_tmp = signal[poz:poz+window_width]
        signal_tmp *= blackman(len(signal_tmp))
        signal1 = rfft(signal_tmp)
        signal1 = abs(signal1)

        clearsignal(signal1)

        for i in range(0, len(signal1)):
            if signal1[i] > 0:
                signal1[i] = log(signal1[i])

        signal2 = irfft(signal1)
        signal2 = abs(signal2)

        poz = 1
        r1 = int(math.floor(w/80))
        r2 = int(math.floor(w/255))
        m = max(signal2[r2:r1])
        for i in range(r2, r1):
            if m == signal2[i]:
                poz = i
                break

        f.append(w/poz)

    result = np.median(sorted(f))

    return result


def main(argv):
    opts, file = getopt.getopt(argv, [])

    w, signal = opensignal(file[0])
    n = len(signal)

    f = cepstrum(signal, n, w)

    if f <= 165:
        print('M')
    else:
        print('K')

if __name__ == "__main__":
   main(sys.argv[1:])