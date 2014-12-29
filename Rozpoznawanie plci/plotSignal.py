from __future__ import division
import getopt
from pylab import *
from numpy import *
from scipy import *
import scipy.io.wavfile
import math
import wave

#opts, file = getopt.getopt(argv, [])
file = '091_M.wav'
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

print 'w = ', w, 'n = ', n

print len(signal.shape)

sub1 = subplot(311)
plot(t, signal)

sub2 = subplot(312)
plot(t, data)

show()