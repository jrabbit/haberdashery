#!/usr/bin/env python
# INSTALL THAT SUCKER
#  --or--
# Haberdashery - the smart (mac) package manager front end.
# GPL v3 or later. (c) Jrabbit 2010.

import os
import sys
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
	if len(paths) == 0:
		print "Sorry found no package managers. Is your $PATH setup correctly?"

def install(pac, man='all'):
	"""Try and install a package"""
	pass

def search_fink(pac):
	""" Searches fink for a package, returns a list of packages line by line"""
	things = Popen(["fink", "list", pac], stdout=PIPE).communicate()[0]
	if things == 0:
		return
	else:
		print("found " + len(things.split("\n")) + " results for " + pac + " in your Fink:")
		print things
		return things
# TODO: add a way to list the installed/uninstalled status using indices. Growl support?

def search_brew(pac):
	"""search homebrew for a package"""
	things = Popen(["brew", "search", pac], stdout=PIPE).communicate()[0]
	things = things.split("\n").pop()
	if len(things) == 0:
		return
	else:
		print("found " + len(things) + " results for " + pac + " in your homebrew:")
		print things
		return things

def search_port(pac):
	"""Search macports for a package, returns a list of package lines"""
	things = Popen(["port", "search", pac], stdout=PIPE).communicate()[0]
	if things == 0:
		return
	else:
		print("found " + len(things.split("\n")) + " results for " + pac + " in your MacPorts:")
		print things
		return things

def search(arguements):
	"""Find a package in fink/brew/ports then run whohas"""

def edit(pac, man):
	"""open a package description in $EDITOR"""
	#TODO: take editor from commandline
	#fink has no edit function
	if man == "fink":
		#fink dumpinfo -finfofile pac | cut -d: -f2 | xargs $editor
		rawdump = Popen(["fink", "dumpinfo", "-finfofile", pac], stdout=PIPE).communicate()[0]
		os.system("open " + rawdump.split(":")[1])
		#this might need adjustments based on if .info files are asociated
	elif man == "brew":
		os.system("brew edit" + pac)
	elif man == "port":
		os.system("port edit" + pac)

def maint_fink():
	os.system("fink selfupdate")
	os.system("fink cleanp")

def maint_brew():
	"""I don't know what else brew needs."""
	os.system("brew update")

def maint_port():
	os.system("port selfupdate")
	os.system("port clean")

def maint(man="all"):
	if man == all:
		if managers[0] != 0:
			print "running maintince on all your package managers"
			maint_fink()
		if managers[1] != 0:
			maint_brew()
		if managers[2] != 0:
			maint_port()
	elif man == "fink":
		maint_fink()
	elif man == "port":
		maint_port()
	elif man == "brew"	:
		maint_brew()

if __name__ == "__main__":
	print sys.argv
	if sys.argv[1] == "search":
		search(sys.argv[2])
		#package (defaults to all)
	elif sys.argv[1] == "edit":
		edit(sys.argv[2], sys.argv[3]) 
		# package , manager
	elif sys.argv[1] == "install":
		install(sys.argv[2], sys.argv[3]) 
		# package , manager
	elif sys.argv[1] == "maint":
		maint(sys.argv[2])

