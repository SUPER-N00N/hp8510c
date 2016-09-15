#!/usr/bin/python

import time
import math
from matplotlib import pyplot
from pylab import *
import numpy
from numpy import arange
import skrf as rf
from hp8510c import *

def main():

	figure(figsize = (8,6), facecolor='white')
	vna = HP8510C('PROLOGIX::/dev/ttyUSB0::GPIB::16')
	vna.cmd("++spoll;");
	vna.cmd("++loc;");
	time.sleep(1);
	vna.write("POIN801; WAIT; WAIT; STAR 2.4 GHz; STOP 2.6 GHz; WAIT;");
	vna.write("S11;FORM4;WAIT;WAIT");
	time.sleep(3)
	res = vna.cmd("OUTPDATA;");
	t_data = numpy.linspace(0.0, len(res) * 0.5, len(res));
	c_data = []
	s11 = []
	s12 = []
	s21 = []
	s22 = []
	reals = []
	imags = []
	pyplot.axes(frameon = 0, aspect = 1, polar = 0)
	pyplot.grid(True)
	idx = 0
	for c_0_s in res:
		c_1 = c_0_s.split(',')
		c = complex(float(c_1[0]), float(c_1[1]));
		idx += 1
		s11.append(c)
		reals.append(c.real)
		imags.append(c.imag)

	time.sleep(1);
	vna.write("S12;WAIT;");
	time.sleep(1)
	reals = []
	imags = []
	res = vna.cmd("OUTPDATA;");
	for c_0_s in res:
		c_1 = c_0_s.split(',')
		c = complex(float(c_1[0]), float(c_1[1]));
		s12.append(c)
		reals.append(c.real)
		imags.append(c.imag)
	time.sleep(1);
	vna.write("S21;WAIT;");
	time.sleep(1)
	reals = []
	imags = []
	res = vna.cmd("OUTPDATA;");
	for c_0_s in res:
		c_1 = c_0_s.split(',')
		c = complex(float(c_1[0]), float(c_1[1]));
		s21.append(c)
		reals.append(c.real)
		imags.append(c.imag)
	time.sleep(1);
	vna.write("S22;WAIT;");
	time.sleep(1)
	reals = []
	imags = []
	res = vna.cmd("OUTPDATA;");
	for c_0_s in res:
		c_1 = c_0_s.split(',')
		c = complex(float(c_1[0]), float(c_1[1]));
		s22.append(c)
		reals.append(c.real)
		imags.append(c.imag)
	title("Just a Penis");
	ntwk = rf.Network(s=s11)
	ntwk.plot_s_smith(label="S11")
	ntwk = rf.Network(s=s12)
	ntwk.plot_s_smith(label="S12")
	ntwk = rf.Network(s=s21)
	ntwk.plot_s_smith(label="S21")
	ntwk = rf.Network(s=s22)
	ntwk.plot_s_smith(label="S22")
	show();
if __name__ == "__main__":
    main()
