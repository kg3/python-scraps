#!/usr/env/python
# Create onetimepad files with rtl_entropy
#
# range,while, times
# rtl_entropy -s 24.4M -f 68.99M -e |rngtest -c 4096 -p > high_test2.bin
#
# breaks at 9.8M
# cat * >> bigfile
# 105 times for 1024
import os, subprocess
from subprocess import PIPE

#### main ####

for i in range(1,3):
	filename = "pyTestPool_%d.bin" % i
	print "Creating %s ..." % (filename) 
	
	fileout = open(filename,"w")
	
	p1=subprocess.Popen(["rtl_entropy","-s","2.4M","-f","69.85M","-e"], stdout=PIPE)
	p2=subprocess.Popen(["rngtest","-c","1024"], shell=True,
	stdin=p1.stdout,stdout=fileout)
	p1.wait()
	p1.stdout.close()	
	p2.wait()
	
	fileout.flush()
	fileout.close()

	# output = p2.communicate()[0]
	## |rngtest -c 4096 > pyTestPool%d.bin"%i,shell=True)
	
	# print output
