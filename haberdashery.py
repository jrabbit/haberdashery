# INSTALL THAT SUCKER
#  --or--
# Haberdashery - the smart (mac) package manager front end.
# GPL v3 or later. (c) Jrabbit 2010.

import os
from subprocess import *

managers = ["fink", "brew", "port"]
paths = []

# lets find where you have your pack-mans installed
for x in managers:
	rawpath = Popen(["which", x], stdout=PIPE).communicate()[0]
	rootpath = os.path.split(os.path.split(rawpath)[0])[0] #nasty, but it gets us the prefixes
	if len(rootpath) != 0:
		print "Found a " + x + " install at " + rootpath
		paths.append(x)
	else:
		paths.append(None) 
		#this may seem redundant but if brew isn't installed and then port is, calling the 2nd key would give the macports path.

def install(pac):
	"""Try and install a package"""

def search_fink(pac):
	""" Searches fink for a package"""
	things = Popen(["fink", "list", pac], stdout=PIPE).communicate()
	if things[0] = 0:
		return
	else
		theone = things[0]
		print("found " + len(theone.split("\n") + " results for " + pac + " in your Fink")
		print theone
		return theone
# TODO: add a way to list the installed/uninstalled status using indices. Growl support?

def search(pac):
	"""Find a package in fink/brew/ports then run whohas"""


def edit(pac, man):
	"""open a package description in $EDITOR"""
	#fink has no edit function
	if man = fink:
		#fink dumpinfo -finfofile pac | cut -d: -f2 | xargs $editor
		rawdump = Popen(["fink", "dumpinfo", "-finfofile", pac], stdout=PIPE).communicate()[0]
		os.system("open " + rawdump.split(":")[1])
	
	elif man = brew:
		os.system("brew edit" + pac)
	
	elif man = port:
		os.system("port edit" + pac)
	

