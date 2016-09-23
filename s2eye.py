#!/usr/bin/python

from  scipy import *
from  scipy import signal
from random import *

import sys
import time
import math
import re

from matplotlib import pyplot
from pylab import *
import numpy
from numpy import arange
from hp8510c import *

def main():
	figure(figsize = (8,6), facecolor='white')
	pyplot.axes(frameon = 0, polar = 0)
	pyplot.grid(True)
	filename = sys.argv[1]
	s11 = []
	s12 = []
	s21 = []
	s22 = []
	freq = []
	numoffreqs = 0
	f = open(filename, 'r')
	s_fre = re.compile('\[Number of Frequencies\] ([0-9]*).*')
	s_re = re.compile(' +([-+]?[0-9]*\.?[0-9]*) +([-+]?[0-9]*\.?[0-9]*) +([-+]?[0-9]*\.?[0-9]*) +([-+]?[0-9]*\.?[0-9]*) +([-+]?[0-9]*\.?[0-9]*) +([-+]?[0-9]*\.?[0-9]*) +([-+]?[0-9]*\.?[0-9]*) +([-+]?[0-9]*\.?[0-9]*) +([-+]?[0-9]*\.?[0-9]*).*')
	for line in f:
		m = s_fre.match(line)
		if m :
			g = m.groups()
			numoffreqs = int(g[0])
			break
	for line in f:
		m = s_re.match(line)
		if m :
			g = m.groups()
			freq.append(float(g[0]))
			s11.append(complex(float(g[1]), float(g[2])))
			s12.append(complex(float(g[3]), float(g[4])))
			s21.append(complex(float(g[5]), float(g[6])))
			s22.append(complex(float(g[7]), float(g[8])))

	for i in range(len(freq)):
		print " " + str(freq[i]) + " GHz " + str(s11[i]) + " " +  str(s12[i]) + " " + str(s21[i]) + " " + str(s22[i])
	g11 = (numpy.fft.ifft(numpy.fft.fftshift(s11)))
	g12 = (numpy.fft.ifft(numpy.fft.fftshift(s12)))
	g21 = (numpy.fft.ifft(numpy.fft.fftshift(s21)))
	g22 = (numpy.fft.ifft(numpy.fft.fftshift(s22)))
	sig = np.repeat([0, -0.5, 0.5, -0.5, 0.5, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1], numoffreqs/16);
	print sig
	sig = numpy.concatenate((sig, [-1]));
 	for j in range(1):
		rand0 = sig;
		rand0 = np.array(rand0);
		bla = numpy.fft.fft(g12) * numpy.fft.fft(rand0)
		foo = numpy.fft.ifft(bla)
		pyplot.plot(foo, color = 'green', alpha = 0.3);
		pyplot.plot(rand0, color = 'green');
		pyplot.plot(g12, color = 'black');
		bla = numpy.fft.ifft(s12 * numpy.fft.fft(rand0))
		pyplot.plot(bla, color = 'red')
	show();	
if __name__ == "__main__":
    main()
