# INSTALL THAT SUCKER
#  --or--
# Haberdashery - the smart package manager front end.
# GPL v3 or later. (c) Jrabbit 2010.

import os
from subprocess import *
managers = ["fink", "brew", "port"]

# lets find where you have your pack-mans installed
for x in managers:
	rawpath = Popen(["which", x], stdout=PIPE).communicate()[0]
	rootpath = os.path.split(os.path.split(rawpath)[0])[0]
	if len(rootpath) != 0:
		print "Found a " + x + " install at " + rootpath
