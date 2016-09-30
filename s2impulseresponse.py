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

#	for i in range(len(freq)):
#		print " " + str(freq[i]) + " GHz " + str(s11[i]) + " " +  str(s12[i]) + " " + str(s21[i]) + " " + str(s22[i])
#	g11 = (numpy.fft.ifft(numpy.fft.fftshift(s11)))
#	zerp = np.repeat([complex(0.0, 0.0)], 8192 - numoffreqs)
#	s11_ = numpy.concatenate(zerp, np.array(s11));
	g11 = (numpy.fft.ifft(numpy.fft.fftshift(s11)))
	g12 = (numpy.fft.ifft(numpy.fft.fftshift(s12)))
#	g12 = numpy.fft.ifftshift(numpy.fft.ifft(numpy.fft.fftshift(s12)))
	g21 = (numpy.fft.ifft(numpy.fft.fftshift(s21)))
	g22 = (numpy.fft.ifft(numpy.fft.fftshift(s22)))
	sig = np.repeat([-0.25, 0.25, -0.25, 0.25, -0.5, 0.5, -0.5, 0.5, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1 ], numoffreqs/64);
	#sig = np.repeat([-0.25, 0.25, -0.5, 0.5, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1], numoffreqs/16);
	print sig
	sig = numpy.concatenate((sig, np.repeat([-1], numoffreqs - (int(numoffreqs/64) * 64))));
 	for j in range(1):
		rand0 = sig;
		rand0 = np.array(rand0);
		bla = numpy.fft.fft(g12) * numpy.fft.fft(rand0)
		foo = numpy.fft.ifft(bla)
		pyplot.plot(g12, color = 'black');
		for k in range(100):
			g12 = (numpy.fft.ifft(numpy.fft.fftshift(s12[k::1])))
			s = numpy.linspace(0, len(g12), len(g12))
		#	s = numpy.linspace(0 + k, len(g12) + k, len(g12))
			pyplot.plot(s, g12, color = 'red', alpha = 0.3)
		
	#	pyplot.plot([c.real for c in foo], color = 'green', alpha = 0.3);
	#	pyplot.plot([c.imag for c in foo], color = 'red', alpha = 0.3);
	#	pyplot.plot(rand0, color = 'green');
	#	pyplot.plot(g11, color = 'red');
	#	pyplot.plot([c for c in g12], color = 'green');
	#	pyplot.plot(g21, color = 'blue');
	#	pyplot.plot(g22, color = 'yellow');
	#	bla = numpy.fft.ifftshift(numpy.fft.ifft(s12 * numpy.fft.fft(rand0)))
	#	pyplot.plot(bla, color = 'red')
	show();	
if __name__ == "__main__":
    main()
