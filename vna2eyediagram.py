#!/usr/bin/python


import sys
import time
import math
from matplotlib import pyplot
from pylab import *
import numpy
from numpy import arange
from hp8510c import *

def main():
	figure(figsize = (8,6), facecolor='white')
        pyplot.axes(frameon = 0, polar = 0)
        pyplot.grid(True)
	suff = sys.argv[2]
	start = sys.argv[1]
	stop = sys.argv[3]
	vna = HP8510C('PROLOGIX::/dev/ttyUSB0::GPIB::16')
	vna.cmd("++spoll;");
	vna.cmd("++loc;");
	time.sleep(1);
	vna.write("POIN801; WAIT; WAIT;" + "STAR " + start + suff + ";" + "STOP " + stop + suff + ";" + "WAIT; WAIT");
	vna.write("S11;FORM4;WAIT;WAIT;WAIT;WAIT;");
	time.sleep(4)
	res = vna.cmd("OUTPDATA;");
	zero_pad = [ 0 for i in range(1024 - 801)];
	s11 = []
	s12 = []
	s21 = []
	s22 = []
	idx = 0
	for c_0_s in res:
		c_1 = c_0_s.split(',')
		c = complex(float(c_1[0]), float(c_1[1]));
		idx += 1
		s11.append(c)
	time.sleep(1);
	vna.write("S12;WAIT;");
	time.sleep(1)
	res = vna.cmd("OUTPDATA;");
	for c_0_s in res:
		c_1 = c_0_s.split(',')
		c = complex(float(c_1[0]), float(c_1[1]));
		s12.append(c)
	time.sleep(1);
	vna.write("S21;WAIT;");
	time.sleep(1)
	res = vna.cmd("OUTPDATA;");
	for c_0_s in res:
		c_1 = c_0_s.split(',')
		c = complex(float(c_1[0]), float(c_1[1]));
		s21.append(c)
	time.sleep(1);
	vna.write("S22;WAIT;");
	time.sleep(1)
	res = vna.cmd("OUTPDATA;");
	for c_0_s in res:
		c_1 = c_0_s.split(',')
		c = complex(float(c_1[0]), float(c_1[1]));
		s22.append(c)
	diff = (float(stop) - float(start)) / 801.0
        t_data = numpy.linspace(0.0, 801 * 0.5, 801);
	i = 0
	toplot = [];
	freq = [];
	t_ = 0;
	td = numpy.fft.ifft(numpy.fft.fftshift(s11))
	
	toplot = [ abs(c) for c in td ]
	pyplot.plot(toplot)
	td = numpy.fft.ifft(numpy.fft.fftshift(s22))
	toplot = [ abs(c) for c in td ]
	pyplot.plot(toplot);
	show();	
if __name__ == "__main__":
    main()
