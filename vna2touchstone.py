#!/usr/bin/python

import sys
import time
import math
from hp8510c import *

def main():

	numoffreqs = 801
	suff = sys.argv[2]
	start = sys.argv[1]
	stop = sys.argv[3]
	touchstonev2 = True;
	if len(sys.argv) > 4:
		if sys.argv[5].upper() == "V1":
			touchstonev2 = False;
	if len(sys.argv) > 5:
		numoffreqs = int(sys.argv[6])
	vna = HP8510C('PROLOGIX::/dev/ttyUSB0::GPIB::16')
	vna.cmd("++spoll;");
	vna.cmd("++loc;");
	time.sleep(1);
	s11 = []
	s12 = []
	s21 = []
	s22 = []
	fac = numoffreqs / 801
	offset = 0.0
	tick = 0.0001
	step = (float(stop) - float(start))/fac
	step_start = float(start)
	for k in range(fac):
		step_stop = step_start + step;
		vna.write("POIN801; WAIT; WAIT;" +  "STAR " + str(step_start) + suff + ";" +"STOP " + str(step_stop) + suff + ";" + "WAIT; WAIT");
		vna.write("S11;FORM4;WAIT;WAIT;WAIT;WAIT;");
		time.sleep(4)
		res = vna.cmd("OUTPDATA;");
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
		step_start = step_stop
		vna.write("STAR 0.1 GHz;" + "STOP 8.1 GHz;" + "WAIT; WAIT");
	diff = (float(stop) - float(start)) / numoffreqs
	if touchstonev2 == True :
		print "!2-port S-parameter file"
		print "[Version] 2.0"
		print "# " + suff + " S RI R 50.0"
		print "!freq RelS11 ImS11 RelS12 ImS12 RelS21 ImS21 RelS22 ImS22"
		print "[Number of Ports] 2"
		print "[Number of Frequencies] " + str(numoffreqs)
		i = 0
		for i in range(len(s11)):
			print "% f" % (float(start) + diff * i) + " " + "% f" % s11[i].real + " " + "% f" % s11[i].imag + " " +  "% f" % s12[i].real + " " + "% f" % s12[i].imag + " " +  "% f" % s21[i].real + " " + "% f" % s21[i].imag + " " +  "% f" % s22[i].real + " " + "% f" % s22[i].imag
	else:
		print "!2-port S-parameter file"
		print "# " + suff + " S RI R 50.0"
		print "!freq RelS11 ImS11 RelS12 ImS12 RelS21 ImS21 RelS22 ImS22"
	
		i = 0
		for i in range(len(s11)):
			print "% .4f" % (float(start) + diff * i) + " " + "% .4f" % s11[i].real + " " + "% .4f" % s11[i].imag + " " +  "% .4f" % s12[i].real + " " + "% .4f" % s12[i].imag + " " +  "% .4f" % s21[i].real + " " + "% .4f" % s21[i].imag + " " +  "% .4f" % s22[i].real + " " + "% .4f" % s22[i].imag
	
if __name__ == "__main__":
    main()
