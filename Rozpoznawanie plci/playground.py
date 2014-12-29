from __future__ import division
import getopt
from pylab import *
from numpy import *
from scipy import *
import scipy.io.wavfile
import math

#opts, file = getopt.getopt(argv, [])
file = '006_K.wav'
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
    if abs(signal1[i]) < m/4:
        signal1[i] = 0

f = int((poz*w)/n)

print 'Dominujaca czestotliwosc: ', f

r1 = int(math.floor(85*n/w))
r2 = int(math.ceil(165*n/w))

men = 0
for i in range(r1, r2):
    men += abs(signal1[i])

r1 = int(math.floor(170*n/w))
r2 = int(math.ceil(250*n/w))

woman = 0
for i in range(r1, r2):
    woman += abs(signal1[i])

if men >= woman:
    print 'M'
else:
    print 'K'

#m = max(signal1)
#print m
sub1 = subplot(311)
plot(t, signal)

signal2 = irfft(signal1)
#signal2 = abs(signal2)

print len(signal2)

sub2 = subplot(312)
#yscale('log')
plot(t[1:], signal2)

signal3 = fft(signal2)
signal3 = abs(signal3)

print len(signal3)
print signal3

sub3 = subplot(313)
p = int(math.ceil(300*n/w))
freqs = linspace(0, 300, p, endpoint=False)
stem(freqs, signal3[0:p], '-*')

show()